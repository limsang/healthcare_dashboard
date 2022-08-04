from DFhandler.handler_base import BaseHandler
import pandas as pd
from utils.utils import create_dataframe_with_initial_columns, HeadphoneAudioExposure_splitter, dbspl_norm
import streamlit as st
import altair as alt
import os


def gen_file_path(dir):
    parent = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))  # 상위 디렉토리
    file_name = f"rawdata/{dir}.csv"
    res = os.path.join(parent, file_name)
    print("res", res)
    return os.path.join(parent, file_name)

class BodySpec(BaseHandler):

    @st.cache(allow_output_mutation=True)
    def load_from_csv(self, csv_list):
        BodyMass, Height, V02Max, BasalEnergyBurned, HeadphoneAudioExposure = None, None, None, None, None

        for csv in csv_list:
            try:
                file = gen_file_path(csv)
                df = pd.read_csv(file)
            except Exception as e:
                st.error("file not exists...", e)

            if csv == "BodyMass":
                BodyMass = create_dataframe_with_initial_columns(df)

            elif csv == "Height":
                """
                최신 신장만 가져온다
                """
                Height = create_dataframe_with_initial_columns(df)
                Height = Height[Height.dttm == Height.dttm.max()]
                Height = Height.iloc[0]['value']

            elif csv == "VO2Max":
                V02Max = create_dataframe_with_initial_columns(df)

            elif csv == "HeadphoneAudioExposure":
                HeadphoneAudioExposure = create_dataframe_with_initial_columns(df)
                HeadphoneAudioExposure['device_name'] = HeadphoneAudioExposure.apply(lambda x: HeadphoneAudioExposure_splitter(x["device"], 1),axis=1)
                HeadphoneAudioExposure = HeadphoneAudioExposure[['value', 'dttm', 'device_name', 'weekday']]
                HeadphoneAudioExposure = HeadphoneAudioExposure.groupby(["dttm", "device_name", "weekday"]).max(['value']).reset_index()
                HeadphoneAudioExposure = HeadphoneAudioExposure.fillna(0)

                week_HeadphoneAudioExposure = HeadphoneAudioExposure.groupby(['device_name', 'weekday']).mean().reset_index()

            elif csv == "BasalEnergyBurned":
                BasalEnergyBurned = create_dataframe_with_initial_columns(df)
                BasalEnergyBurned = BasalEnergyBurned[['value', 'date', 'dttm', 'weekday']]
                BasalEnergyBurned = BasalEnergyBurned.groupby("dttm").max().reset_index()

            else:
                pass

        return BodyMass, Height, V02Max, BasalEnergyBurned, HeadphoneAudioExposure, week_HeadphoneAudioExposure

    def preproc(self):
        pass

    def analysis_with_model(self):
        pass

    def visualize(self, BodyMass, Height, V02Max, BasalEnergyBurned, HeadphoneAudioExposure, week_HeadphoneAudioExposure):

        """
        :param BodyMass: 체중
        :param Height: 신장
        :param V02Max: 산소포화도
        :param BasalEnergyBurned: 기초대사량
        :return:
        """
        st.title("Profile")
        st.markdown("***")
        valBodyMass = BodyMass[BodyMass.dttm == BodyMass.dttm.max()]
        valBodyMass = valBodyMass.iloc[0]['value']
        valBodyMass = int(valBodyMass)
        Height = int(Height)
        BMI = valBodyMass / (Height * Height / 10000)
        st.title(f'몸무게: {valBodyMass}')
        st.title(f'키: {Height}')

        barometer = Height - 110 # BMI기준 평균 몸무게

        BMI = round(BMI, 1)
        # 결과 출력 20미만이면 저체중, 20~24 사이면 정상, 25~29는 과체중, 30 이상이면 비만
        if BMI < 20:
            st.title(f'BMI: {BMI} 저체중')

        elif (20 <= BMI or BMI < 25):
            st.title(f'BMI: {BMI} 정상')

        elif (25 <= BMI or BMI < 30):
            st.title(f'BMI: {BMI} 과체중')

        else:
            st.title(f'BMI: {BMI} ?????? 금식하세요')

        st.markdown("***")

        cols = st.columns(2)

        chartBodyMass = alt.Chart(BodyMass.query('type=="BodyMass"')).mark_circle(opacity=0.9).encode(
            x='date',
            y='value',
            size='value',
            color=alt.condition(alt.datum.value > barometer,
                                alt.value('red'),
                                alt.value('black'))
        )

        chartBodyMass.title = "Body Weight"
        chartBodyMass.encoding.x.title = "timeline"
        chartBodyMass.encoding.y.title = "Weight(kg)"
        cols[0].title("Weight")
        cols[0].altair_chart(chartBodyMass, use_container_width=True)


        """
        headphone devices
        """
        brush = alt.selection_interval(encodings=['x'])
        week_HeadphoneAudioExposure_chart = alt.Chart(week_HeadphoneAudioExposure).mark_bar().encode(
            x='device_name',
            y='value:Q',
            color='device_name:N',
            column=alt.Column('weekday:N', sort=alt.SortField("weekday", order="descending")),
        ).properties(width=50, height=250).add_selection(brush)


        cols[0].title("Audio Volume")
        moving_average_value = cols[0].slider("이동평균값", 0, 100, 10)
        HeadphoneAudioExposure['mv_avg'] = HeadphoneAudioExposure['value'].rolling(window=moving_average_value).mean()
        HeadphoneAudioExposure['dbspl_norm'] = HeadphoneAudioExposure.apply(lambda x: dbspl_norm(x["mv_avg"]),axis=1)
        HeadphoneAudioExposure = HeadphoneAudioExposure.fillna(0)

        HeadphoneAudioExposure_chart = alt.Chart(HeadphoneAudioExposure).mark_circle(opacity=0.9).encode(
            x='dttm:T',
            y='mv_avg',
            color="dbspl_norm"
        )

        cols[0].altair_chart(HeadphoneAudioExposure_chart, use_container_width=True)
        cols[0].title("요일별 평균 음량")
        cols[0].altair_chart(week_HeadphoneAudioExposure_chart, use_container_width=False)
