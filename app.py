import streamlit as st
import pandas as pd
import pydeck as pdk

activities = []


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i: i + 2], 16) for i in (0, 2, 4))


budapest_location = {'latitude': 47.4979, 'longitude': 19.0402}
madrid_location = {'latitude': 40.4168, 'longitude': 3.7038}

view_state = pdk.ViewState(zoom=4, **budapest_location)


def calc_path(distance: int):
    total_distance = 1456
    ratio = total_distance if distance > total_distance else distance / total_distance
    lat = budapest_location['latitude'] + (madrid_location['latitude'] - budapest_location['latitude']) * ratio
    lon = budapest_location['longitude'] + (madrid_location['longitude'] - budapest_location['longitude']) * ratio
    ret = [[budapest_location['longitude'], budapest_location['latitude']],
           [lon, lat]]
    return ret


data = pd.read_json('dummy_data.json')
data["color"] = data["color"].apply(hex_to_rgb)

layer_data = data.copy()
layer = pdk.Layer(
    type="PathLayer",
    data=layer_data,
    pickable=True,
    get_color="color",
    width_scale=20,
    width_min_pixels=5,
    get_path="path",
    get_width=5,
)


def filter_unit():
    global layer_data
    layer_data = data[data['name'] == st.session_state.radio]


col1, col2 = st.columns([8, 4])

col1.radio(options=['CO1', 'CO2', 'TA2', 'TA1', 'MS1', 'MS2'],
           label='Select Unit',
           on_change=filter_unit,
           key='unit_radio')

col2.radio(options=['Run', 'Ride', 'Walk'],
           label='Select Activtity Type',
           key='activty_radio')

col1.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{name}"}))
col2.write(data)
