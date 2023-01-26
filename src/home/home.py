import streamlit as st
import pandas as pd
import numpy as np

st.title('Number check')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# @st.cache
def convert_meter_to_python():
    pyeong = (float(st.session_state['msg'])*121)/400
    # st.write(pyeong)
    # st.write(st.session_state.msg)
    # print(st.session_state.msg)
    return pyeong, round(pyeong)

# squaree_meter = st.number_input(label="Message", key="msg", on_change = convert_meter_to_python)
input = st.text_input(label="Message")
input
# pyeong, pyg = convert_meter_to_python(squaree_meter)
# st.write('The current number is ', pyeong)
# st.write('The number is ', pyg)
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)