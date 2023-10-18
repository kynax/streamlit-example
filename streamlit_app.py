from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

from datetime import date
import os
import json
from sports_streams import get_json_output

def pretty_print_json(json_data):
    st.write(json_data)

try:
    today = date.today()
    today_file = today.strftime("%Y-%m-%d") + '.json'
    if os.path.isfile(today_file):
        st.write('Found a stream listing file for ' + str(today))
        
        if st.button('Delete cache file and reload'):
            os.remove(today_file)
            st.rerun()

        with open(today_file, 'r') as f:
            dd = json.load(f)
    else:
        #st.write('No cache file available, searching for streams...')

        try:
            with st.spinner('Looking for streams...'):
                dd = json.loads( get_json_output())   #['nhl']))
                with open(today_file, 'w') as f:
                    json.dump(dd, f)
        except Exception as ex:
            st.write( str(ex))

    pretty_print_json(dd)
except Exception as ex:
    st.write( str(ex))

if False:
    with st.echo(code_location='below'):
        total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
        num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

        Point = namedtuple('Point', 'x y')
        data = []

        points_per_turn = total_points / num_turns

        for curr_point_num in range(total_points):
            curr_turn, i = divmod(curr_point_num, points_per_turn)
            angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
            radius = curr_point_num / total_points
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            data.append(Point(x, y))

        st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
            .mark_circle(color='#0068c9', opacity=0.5)
            .encode(x='x:Q', y='y:Q'))
