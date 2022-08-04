import sys
from DFhandler.handler_base import BaseHandler
import pandas as pd
from utils.utils import create_dataframe_with_initial_columns
import streamlit as st
import altair as alt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class Workout(BaseHandler):

    @st.cache
    def load_from_csv(self, df):
        try:
            _df = create_dataframe_with_initial_columns(df)
            # 비어있는 날짜의 값을 채워넣는다
            empty_date = _df.groupby("date").max().reset_index()
            r = pd.date_range(start=empty_date.date.min(), end=empty_date.date.max())
            empty_date = empty_date.set_index('date').reindex(r).fillna(0.0).rename_axis('date').reset_index()
            empty_date = empty_date[~empty_date.date.isin(_df.date)]
            frames = [_df, empty_date]
            _df = pd.concat(frames)
            return _df

        except Exception as e:
            print("errrr@load_from_csv@Workout", e)

    def preproc(self, Workout):

        def _normalize(df, col):
            result = df.copy()
            for feature_name in df.columns:
                max_value = df[col].max()
                min_value = df[col].min()
                result['norm_counts'] = (df[col] - min_value) / (max_value - min_value)
            return result

        def _get_season(data):

            if data in [12, 1, 2]:
                return "winter"

            elif data in [3, 4, 5]:
                return "spring"

            elif data in [6, 7, 8, 9]:
                return "summer"

            else:
                return "fall"

        def gen_overall(Workout):
            """
            전체 OVERALL
            최대 최소값은 제거한다
            """
            def modify_activityType(data):
                try:
                    return data[21:]

                except Exception as e:
                    pass

            overall = Workout[['duration', 'workoutActivityType', 'totalEnergyBurned', 'date']].query('duration > 0')
            overall['date'] = pd.to_datetime(overall['date'])
            overall['date'] = overall['date'].astype(str)
            overall = overall.loc[overall['duration'] != overall['duration'].max()]
            overall = overall.loc[overall['duration'] != overall['duration'].min()]
            overall['workoutActivityType'] = overall['workoutActivityType'].map(modify_activityType)  # 이름 너무 길어 잘라
            overall = overall.reset_index()
            overall['index'] = overall.index

            return overall

        def gen_weekdayCount(Workout):
            """
            요일별 운동횟수를 기록
            """
            weekdayCount = Workout.groupby(['weekday']).size().reset_index(name='counts')
            weekdayCount = _normalize(weekdayCount, 'counts')
            return weekdayCount

        def gen_gymTraining(Workout, cats):
            gymTraining = Workout.query("totalDistance <= 0")  # Workout['totalDistance'] == 0 #
            gymTraining['ExerciseIntensity'] = round(gymTraining['totalEnergyBurned'] / gymTraining['duration'])
            gymTraining['date'] = pd.to_datetime(gymTraining['date'])
            gymTraining = gymTraining[['date', 'weekday', 'duration', 'totalEnergyBurned', 'ExerciseIntensity']]
            gymTraining = gymTraining.set_index('date')
            # 요일별 운동량을 측정한다.
            gymTrainingPerWeekday = gymTraining[['duration', 'totalEnergyBurned', 'ExerciseIntensity']].groupby(gymTraining['weekday'])
            gymTrainingPerWeekday = gymTrainingPerWeekday.mean().reindex(cats)
            # 인덱스를 일반 컬럼으로 이동
            gymTrainingPerWeekday = gymTrainingPerWeekday.reset_index()
            return gymTraining, gymTrainingPerWeekday

        def gen_HKWorkoutActivityTypeSoccer(Workout):
            """
            축구
            """
            HKWorkoutActivityTypeSoccer = Workout.query('workoutActivityType =="HKWorkoutActivityTypeSoccer" or workoutActivityType ==0')
            HKWorkoutActivityTypeSoccer = HKWorkoutActivityTypeSoccer.groupby('date')[['duration', 'durationUnit', 'totalDistance', 'totalEnergyBurned']].sum().reset_index()
            HKWorkoutActivityTypeSoccer['intensity'] = HKWorkoutActivityTypeSoccer['totalEnergyBurned'] / HKWorkoutActivityTypeSoccer['duration'] * 10
            HKWorkoutActivityTypeSoccer = HKWorkoutActivityTypeSoccer.fillna(0)
            return HKWorkoutActivityTypeSoccer

        def gen_Soccer_play_time(Workout):

            Soccer_play_time = Workout.query('workoutActivityType =="HKWorkoutActivityTypeSoccer"')
            Soccer_play_time = Soccer_play_time.groupby('date')[['duration', 'durationUnit', 'totalDistance', 'totalEnergyBurned']].sum().reset_index()
            Soccer_play_time['intensity'] = Soccer_play_time['totalEnergyBurned'] / Soccer_play_time['duration'] * 10
            return Soccer_play_time
        # 유산소 운동
        def gen_CardioWorkout(Workout):
            CardioWorkout = Workout.query('totalDistance > 0')
            CardioWorkout = CardioWorkout.groupby('date')[['duration', 'totalDistance', 'totalEnergyBurned']].sum().reset_index()
            CardioWorkout['intensity'] = CardioWorkout['totalEnergyBurned'] / CardioWorkout['duration'] * 10
            return CardioWorkout

        def gen_StrengthTraining(Workout):
            """
            헬스
            """
            StrengthTraining = Workout.query('workoutActivityType =="HKWorkoutActivityTypeTraditionalStrengthTraining" or workoutActivityType ==0')
            StrengthTraining = StrengthTraining.groupby(['date', 'weekday', 'month_only'])[['duration', 'totalEnergyBurned']].sum().reset_index()
            StrengthTraining = StrengthTraining.drop_duplicates(['date'], keep='last')
            StrengthTraining['avg_duration'] = StrengthTraining["duration"].mean()
            StrengthTraining['duration_indicator'] = StrengthTraining["duration"] / StrengthTraining["avg_duration"]
            StrengthTraining['intensity'] = StrengthTraining['duration_indicator'] * StrengthTraining['totalEnergyBurned'] / StrengthTraining['duration']
            StrengthTraining = StrengthTraining.fillna(0)
            StrengthTraining = StrengthTraining.loc[StrengthTraining['intensity'] != StrengthTraining['intensity'].max()]
            StrengthTraining['weekday'].replace({0: "NULL"}, inplace=True)
            return StrengthTraining

        def gen_SeasonWorkout(Workout):
            """
            헬스 계절별 평균 운동량, 주기
            """
            SeasonWorkout = Workout.query('workoutActivityType =="HKWorkoutActivityTypeTraditionalStrengthTraining" or workoutActivityType ==0')
            SeasonWorkout = SeasonWorkout.query('totalEnergyBurned > 0')
            SeasonWorkout = SeasonWorkout.query('duration > 0')
            SeasonWorkout['season'] = SeasonWorkout.month_only.map(_get_season)
            SeasonWorkout = SeasonWorkout.groupby(['season']).mean()
            SeasonWorkout['season'] = SeasonWorkout.index

            return SeasonWorkout
        # 주기측정용 푸리에 DF
        def gen_fft_df(StrengthTraining):
            fft = tf.signal.rfft(StrengthTraining['duration'])  # Real-valued fast Fourier transform.
            f_per_dataset = np.arange(0, len(fft))  # fft 전체길이 35045
            n_samples_h = len(StrengthTraining['duration'])
            weeks_per_dataset = n_samples_h / 7  # because we use weeks for sampling
            f_per_year = f_per_dataset / weeks_per_dataset  # sampling frequency
            fft_real_value = np.abs(fft)
            StrengthTraining_fft_duration = pd.DataFrame({'f_per_year': f_per_year, 'fft_real_value': fft_real_value})
            StrengthTraining_week = StrengthTraining.groupby(by=['weekday'], as_index=False).mean()
            return StrengthTraining_fft_duration, StrengthTraining_week

        StrengthTraining = gen_StrengthTraining(Workout)
        StrengthTraining_fft_duration, StrengthTraining_week = gen_fft_df(StrengthTraining)
        weekdayCount = gen_weekdayCount(Workout)
        Soccer_play_time = gen_Soccer_play_time(Workout)
        HKWorkoutActivityTypeSoccer = gen_HKWorkoutActivityTypeSoccer(Workout)
        gymTraining, gymTrainingPerWeekday = gen_gymTraining(Workout, cats)
        CardioWorkout = gen_CardioWorkout(Workout)
        overall = gen_overall(Workout)
        SeasonWorkout = gen_SeasonWorkout(Workout)

        return overall, weekdayCount, StrengthTraining, StrengthTraining_week, HKWorkoutActivityTypeSoccer, Soccer_play_time, CardioWorkout, gymTraining, gymTrainingPerWeekday, StrengthTraining_fft_duration, SeasonWorkout

    def analysis_with_model(self):
        pass

    def visualize(self, overall, weekdayCount, StrengthTraining, StrengthTraining_week, HKWorkoutActivityTypeSoccer, Soccer_play_time, CardioWorkout, gymTraining, gymTrainingPerWeekday, StrengthTraining_fft_duration, SeasonWorkout):

        overallChart = alt.Chart(overall).mark_line(interpolate='monotone').encode(
            x='date:T',
            y=alt.Y('duration', stack=None),
            color="workoutActivityType"
        ).configure_legend(orient='bottom') # 레전드 맨 아래

        overallChart.title = "OVERALL"
        overallChart.encoding.x.title = "timeline"
        overallChart.encoding.y.title = "duration (Minutes)"

        scaler = MinMaxScaler()
        # 스케일을 적용할 column을 정의합니다.
        scale_cols = ['duration']
        scaled = scaler.fit_transform(overall[scale_cols])
        scaled = pd.DataFrame(scaled, columns=scale_cols)
        scaled = scaled.rename(columns={'duration': 'scaled_duration'})
        overall = pd.concat([overall, scaled], axis=1)

        base = alt.Chart(overall).mark_circle(opacity=0.5).transform_fold(
            fold=['duration'],
            as_=['category', 'y']
        ).encode(
            alt.X('date:T'),
            alt.Y('y:Q'),
            alt.Color('category:N')

        )
        overall_trend_chart = base + base.transform_loess('date', 'y', groupby=['category']).mark_line(size=5)
        overall_trend_chart.title = '운동강도 추세'

        st.title("OVERALL")
        st.altair_chart(overallChart, use_container_width=True)
        st.altair_chart(overall_trend_chart, use_container_width=True)
        st.markdown("***")

        weekdayCount_Chart = alt.Chart(weekdayCount.query('weekday != 0')).mark_area(line={'color': 'darkgreen'}, color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='white', offset=0),
                   alt.GradientStop(color='darkgreen', offset=1)])).encode(
            x=alt.X('weekday', sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
            y='counts')

        weekdayCount_Chart.title = "요일별 운동 횟수"
        weekdayCount_Chart.encoding.x.title = "요일"
        weekdayCount_Chart.encoding.y.title = "횟수"


        """
        soccer
        """
        HKWorkoutActivityTypeSoccer_chart = alt.Chart(HKWorkoutActivityTypeSoccer).mark_line(point=True).encode(
            alt.X('date', scale=alt.Scale(zero=False)),
            alt.Y('duration', scale=alt.Scale(zero=False)),
            order='date')
        HKWorkoutActivityTypeSoccer_chart.title = "플레이타임"
        HKWorkoutActivityTypeSoccer_chart.encoding.x.title = "timeline"
        HKWorkoutActivityTypeSoccer_chart.encoding.y.title = "duration(min)"


        Soccer_play_time_chart = alt.Chart(Soccer_play_time).mark_line(point=True).encode(
            alt.X('date', scale=alt.Scale(zero=False)),
            alt.Y('duration', scale=alt.Scale(zero=False)),
            order='date')
        Soccer_play_time_chart.title = "플레이타임"
        Soccer_play_time_chart.encoding.x.title = "timeline"
        Soccer_play_time_chart.encoding.y.title = "duration(min)"

        CardioWorkout_intensity_Chart = alt.Chart(CardioWorkout.query("totalDistance > 0")).mark_area(
            color="lightblue",
            interpolate='step-after',
            line=True).encode(x='date:T', y='intensity')

        CardioWorkout_intensity_Chart.title = "유산소 운동 강도"
        CardioWorkout_intensity_Chart.encoding.x.title = "timeline(Y-M-D)"
        CardioWorkout_intensity_Chart.encoding.y.title = "운동강도 (시간당 칼로리 소모량)"


        Soccer_play_distance = alt.Chart(Soccer_play_time.query("totalDistance > 0")).mark_area(
            color="lightblue",
            interpolate='step-after',
            line=True).encode(x='date', y='totalDistance')

        Soccer_play_distance.title = "풋살 뛴 거리"
        Soccer_play_distance.encoding.x.title = "timeline"
        Soccer_play_distance.encoding.y.title = "Distance(km)"


        Soccer_play_intensity = alt.Chart(Soccer_play_time).mark_area(line={'color': 'darkgreen'}, color=alt.Gradient(
            gradient='linear',stops=[alt.GradientStop(color='white', offset=0), alt.GradientStop(color='darkgreen', offset=1)])).encode(x='date', y='intensity')

        Soccer_play_intensity.title = "플레이 강도"
        Soccer_play_intensity.encoding.x.title = "timeline"
        Soccer_play_intensity.encoding.y.title = "강도 (칼로리 소모/거리)"

        """
        헬스
        """

        StrengthTraining_intensity = alt.Chart(StrengthTraining).mark_bar(opacity=1.0).encode(
            x='date:T',
            y=alt.Y('intensity:Q', stack=None),
            color="intensity"
        )

        StrengthTraining_intensity.title = "헬스 강도"
        StrengthTraining_intensity.encoding.x.title = "timeline(Y-M-D)"
        StrengthTraining_intensity.encoding.y.title = "운동강도 (시간당 칼로리 소모량)"
        StrengthTraining_fft_duration = StrengthTraining_fft_duration[10:]
        StrengthTraining_fft_duration_chart = alt.Chart(StrengthTraining_fft_duration).mark_bar().encode(
            x='f_per_year',
            y=alt.Y('fft_real_value:Q', stack=None),
            color="fft_real_value"
        )
        StrengthTraining_fft_duration_chart.title = "주기"


        base = alt.Chart(StrengthTraining_week.query('duration > 0')).encode(
            x=alt.X('weekday', sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],axis=alt.Axis(title=None, labelAngle=0))
        )
        area = base.mark_line(stroke='red', interpolate='monotone').encode(alt.Y('duration', axis=alt.Axis(title='duration', titleColor='red')))
        line = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(alt.Y('intensity', axis=alt.Axis(title='intensity', titleColor='#5276A7')))
        StrengthTraining_week_duration = alt.layer(area, line).resolve_scale(y='independent')
        StrengthTraining_week_duration.title = "요일별 운동 시간 및 강도"

        base = alt.Chart(StrengthTraining).mark_circle(opacity=0.5).transform_fold(
            fold=['intensity'],
            as_=['category', 'y']
        ).encode(
            alt.X('date:T'),
            alt.Y('y:Q'),
            alt.Color('category:N')
        )
        StrengthTrainingTrend = base + base.transform_loess('date', 'y', groupby=['category']).mark_line(size=5)
        StrengthTrainingTrend.title = "운동 강도 추세"

        """
        cardio
        """
        CardioWorkoutChart = alt.Chart(CardioWorkout.query("totalDistance > 0")).mark_area(
            color="lightblue",
            interpolate='step-after',
            line=True).encode(x='date:T', y='totalEnergyBurned')

        CardioWorkoutChart.title = "유산소 칼로리 소모량 (kcal)"
        CardioWorkoutChart.encoding.x.title = "timeline(Y-M-D)"
        CardioWorkoutChart.encoding.y.title = "칼로리 소모량(kcal)"

        CardioWorkout_intensity_Chart = alt.Chart(CardioWorkout.query("totalDistance > 0")).mark_area(
            color="lightblue",
            interpolate='step-after',
            line=True).encode(x='date:T', y='intensity')

        CardioWorkout_intensity_Chart.title = "유산소 운동 강도"
        CardioWorkout_intensity_Chart.encoding.x.title = "timeline(Y-M-D)"
        CardioWorkout_intensity_Chart.encoding.y.title = "운동강도 (시간당 칼로리 소모량)"

        base = alt.Chart(CardioWorkout.query('totalDistance > 0')).encode(x=alt.X('date',axis=alt.Axis(title=None, labelAngle=0)))
        area = base.mark_line(stroke='red', interpolate='monotone').encode(alt.Y('totalEnergyBurned', axis=alt.Axis(title='totalEnergyBurned (kcal)', titleColor='red')))
        line = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(alt.Y('duration', axis=alt.Axis(title='duration(min)', titleColor='#5276A7')))
        CardioWorkout_overall = alt.layer(area, line).resolve_scale(y='independent')
        CardioWorkout_overall.title = "유산소 overall"

        gymTrainingPerWeekdayChart = alt.Chart(gymTrainingPerWeekday, title="요일별 운동강도").mark_circle().encode(
            x=alt.X('weekday', sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
            y='ExerciseIntensity',
            size='ExerciseIntensity',
            color=alt.condition(alt.datum.ExerciseIntensity > 6.6,
            alt.value('red'),
            alt.value('blue'))).configure_axis(grid=False, titleFontSize=20).configure_view(strokeWidth=0).configure_title(fontSize=24)


        """
        overall
        """
        st.title("Cardio")
        st.altair_chart(CardioWorkout_overall, use_container_width=True)
        st.altair_chart(CardioWorkout_intensity_Chart, use_container_width=True)
        st.markdown("***")

        """
        soccer/futsal
        """
        st.title("SOCCER/FUTSAL")
        cols = st.columns(2)
        st.altair_chart(Soccer_play_intensity, use_container_width=True)
        cols[0].altair_chart(Soccer_play_distance, use_container_width=True)
        cols[1].altair_chart(HKWorkoutActivityTypeSoccer_chart, use_container_width=True)

        st.markdown("***")

        """
        gym
        """
        st.title("GYM")
        cols = st.columns(2)
        cols[0].altair_chart(StrengthTraining_week_duration, use_container_width=True)
        cols[1].altair_chart(StrengthTraining_intensity, use_container_width=True)
        st.altair_chart(StrengthTraining_fft_duration_chart, use_container_width=True)

        """
        요일별 gym
        """
        base = alt.Chart(SeasonWorkout).encode(x=alt.X('season',
                                    sort=['spring', 'summer', 'fall', 'winter'],
                                    axis=alt.Axis(title=None, labelAngle=0)))
        area = base.mark_line(stroke='red', interpolate='monotone').encode(
            alt.Y('duration',
                  scale=alt.Scale(domain=[SeasonWorkout['duration'].min(),
                                          SeasonWorkout['duration'].max() + 10]),
                  axis=alt.Axis(title='duration', titleColor='red')))

        line = base.mark_line(stroke='blue', interpolate='monotone').encode(
            alt.Y('totalEnergyBurned',
                  scale=alt.Scale(domain=[SeasonWorkout['totalEnergyBurned'].min(),
                                          SeasonWorkout['totalEnergyBurned'].max() + 10]),
                  axis=alt.Axis(title='totalEnergyBurned', titleColor='blue')))

        SeasonWorkout_chart = alt.layer(area, line).resolve_scale(y='independent')
        SeasonWorkout_chart.title = "계절별 운동 시간 및 강도"
        st.altair_chart(SeasonWorkout_chart, use_container_width=True)