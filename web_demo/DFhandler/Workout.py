from DFhandler.handler_base import BaseHandler
import pandas as pd
from utils.utils import create_dataframe_with_initial_columns
import streamlit as st
import altair as alt
class Workout(BaseHandler):

    def load_from_csv(self, df):
        _df = create_dataframe_with_initial_columns(df)
        empty_date = _df.groupby("date").max().reset_index()
        r = pd.date_range(start=empty_date.date.min(), end=empty_date.date.max())
        empty_date = empty_date.set_index('date').reindex(r).fillna(0.0).rename_axis('date').reset_index()
        empty_date = empty_date[~empty_date.date.isin(_df.date)]
        frames = [_df, empty_date]
        _df = pd.concat(frames)
        return _df

    def preproc(self, Workout):

        def normalize(df, col):
            result = df.copy()
            for feature_name in df.columns:
                max_value = df[col].max()
                min_value = df[col].min()
                result['norm_counts'] = (df[col] - min_value) / (max_value - min_value)
            return result

        cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        """
        요일별 운동횟수를 기록

        """
        weekdayCount = Workout.groupby(['weekday']).size().reset_index(name='counts')
        weekdayCount = normalize(weekdayCount, 'counts')


        """
        축구
        """
        Soccer_play_time = Workout.query('workoutActivityType =="HKWorkoutActivityTypeSoccer"')
        Soccer_play_time = Soccer_play_time.groupby('date')[['duration', 'durationUnit', 'totalDistance', 'totalEnergyBurned']].sum().reset_index()
        Soccer_play_time['intensity'] = Soccer_play_time['totalEnergyBurned'] / Soccer_play_time['duration'] * 10


        # 유산소 운동
        CardioWorkout = Workout.query('totalDistance > 0')
        CardioWorkout = CardioWorkout.groupby('date')[['duration', 'totalDistance', 'totalEnergyBurned']].sum().reset_index()
        CardioWorkout['intensity'] = CardioWorkout['totalEnergyBurned'] / CardioWorkout['duration'] * 10

        """
        헬스
        """
        StrengthTraining = Workout.query('workoutActivityType =="HKWorkoutActivityTypeTraditionalStrengthTraining"')
        StrengthTraining = StrengthTraining.groupby(['date', 'weekday'])[['duration', 'totalEnergyBurned']].sum().reset_index()
        StrengthTraining = StrengthTraining.drop_duplicates(['date'], keep='last')
        StrengthTraining['avg_duration'] = StrengthTraining["duration"].mean()
        StrengthTraining['duration_indicator'] = StrengthTraining["duration"] / StrengthTraining["avg_duration"]
        StrengthTraining['intensity'] = StrengthTraining['duration_indicator'] * StrengthTraining['totalEnergyBurned']/StrengthTraining['duration']

        StrengthTraining_week = StrengthTraining.groupby(by=['weekday'], as_index=False).mean()

        # 무산소 운동
        weight_trainig_mask = Workout['totalDistance'] == 0
        weight_training = Workout[weight_trainig_mask]
        # 운동강도 추가
        weight_training['ExerciseIntensity'] = round(weight_training['totalEnergyBurned'] / weight_training['duration'])

        gymTraining = weight_training
        gymTraining['date'] = pd.to_datetime(weight_training['date'])
        gymTraining = gymTraining[['date', 'weekday', 'duration', 'totalEnergyBurned', 'ExerciseIntensity']]
        gymTraining = gymTraining.set_index('date')

        # 요일별 운동량을 측정한다.
        gymTrainingPerWeekday = gymTraining[['duration', 'totalEnergyBurned', 'ExerciseIntensity']].groupby(gymTraining['weekday'])
        gymTrainingPerWeekday = gymTrainingPerWeekday.mean().reindex(cats)
        # 인덱스를 일반 컬럼으로 이동
        gymTrainingPerWeekday = gymTrainingPerWeekday.reset_index()

        return weekdayCount, StrengthTraining, StrengthTraining_week, Soccer_play_time, CardioWorkout, gymTraining, gymTrainingPerWeekday

    def analysis_with_model(self):
        pass

    def visualize(self, weekdayCount, StrengthTraining, StrengthTraining_week, Soccer_play_time, CardioWorkout, gymTraining, gymTrainingPerWeekday):
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
        soccer play time
        """
        Soccer_play_time_chart = alt.Chart(Soccer_play_time).mark_point().encode(x='date:T', y='duration')

        # Chart = alt.Chart(HKWorkoutActivityTypeSoccer).mark_line().encode(x='date', y='duration')
        Soccer_play_time_chart.title = "플레이타임"
        Soccer_play_time_chart.encoding.x.title = "timeline"
        Soccer_play_time_chart.encoding.y.title = "duration(min)"


        """
        soccer play distance
        """
        Soccer_play_distance = alt.Chart(Soccer_play_time.query("totalDistance > 0")).\
            mark_area(line={'color': 'darkgreen'},color=alt.Gradient(gradient='linear',stops=[alt.GradientStop(color='white',offset=0), alt.GradientStop(color='darkgreen',offset=1)])).encode(x='date', y='totalDistance')

        Soccer_play_distance.title = "풋살 뛴 거리"
        Soccer_play_distance.encoding.x.title = "timeline"
        Soccer_play_distance.encoding.y.title = "Distance(km)"

        """
        soccer play intensity
        """
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

        StrengthTraining_week_duration = alt.Chart(StrengthTraining_week.query('totalEnergyBurned>0')).mark_bar(opacity=1.0).encode(
            x=alt.X('weekday', sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
            y=alt.Y('duration:Q', stack=None),
            color="duration"
        )

        StrengthTraining_week_duration.title = "요일별 평균 운동지속시간"
        StrengthTraining_week_duration.encoding.x.title = "요일"
        StrengthTraining_week_duration.encoding.y.title = "운동시간(min)"

        StrengthTraining_week_intensity = alt.Chart(StrengthTraining_week.query('totalEnergyBurned>0')).mark_bar(opacity=1.0).encode(
            x=alt.X('weekday', sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
            y=alt.Y('intensity:Q', stack=None),
            color="intensity"
        )
        StrengthTraining_week_intensity.title = "요일별 평균 운동 강도"
        StrengthTraining_week_intensity.encoding.x.title = "요일"
        StrengthTraining_week_intensity.encoding.y.title = "강도"

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

        gymTrainingPerWeekdayChart = alt.Chart(gymTrainingPerWeekday, title="요일별 운동 Overview"). \
            mark_circle(). \
            encode(
            x=alt.X('weekday', sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
            y='ExerciseIntensity',
            size='ExerciseIntensity',
            color=alt.condition(alt.datum.ExerciseIntensity > 8,
                                alt.value('red'),
                                alt.value('greed'))). \
            configure_axis(grid=False, titleFontSize=20). \
            configure_view(strokeWidth=0).configure_title(fontSize=24).interactive()


        #
        # st.altair_chart(CardioWorkoutChart, use_container_width=True)
        # st.altair_chart(CardioWorkout_intensity_Chart, use_container_width=True)
        # st.altair_chart(weekdayCount_Chart, use_container_width=True)
        # st.altair_chart(Soccer_play_distance, use_container_width=True)
        # st.altair_chart(StrengthTraining_week_duration, use_container_width=True)
        # st.altair_chart(StrengthTraining_intensity, use_container_width=True)
        # st.altair_chart(Soccer_play_time_chart, use_container_width=True)

        st.markdown("")

        st.markdown("")
        show_lst = list()

        show_lst.append(StrengthTraining_intensity)
        show_lst.append(weekdayCount_Chart)
        show_lst.append(Soccer_play_time_chart)
        show_lst.append(Soccer_play_distance)
        show_lst.append(Soccer_play_intensity)
        show_lst.append(StrengthTraining_week_intensity)
        show_lst.append(StrengthTraining_week_duration)
        show_lst.append(CardioWorkoutChart)


        cnt = 0
        for i in range(4):
            cols = st.beta_columns(2)
            cols[0].altair_chart(show_lst[cnt], use_container_width=True)
            cols[1].altair_chart(show_lst[cnt+1], use_container_width=True)
            cnt += 2
