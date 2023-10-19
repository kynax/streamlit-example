import streamlit as st
st.set_page_config(layout="wide")

from datetime import datetime, timezone
import pytz
import os
import json
from sports_streams import get_json_output

def pretty_print_json(json_data):
    for sport in json_data:
        with st.expander(sport):
            for game in json_data[sport]:
                st.write(game)
                i = 1
                for url in json_data[sport][game]:
                    st.link_button(f"Stream {i}", url)
                    i += 1
                if i == 1:
                    st.write('No stream available yet.')

try:
    today = datetime.now()
    today = today.astimezone(pytz.timezone("US/Eastern"))
    today_file = today.strftime("%Y-%m-%d") + '.json'
    if os.path.isfile(today_file):
        with open(today_file, 'r') as f:
            dd = json.load(f)
    
        #st.write('Found a stream listing file for ' + str(today))
        st.write('Streams data was gathered on ' + dd['fileinfo']['date'])
        
        if st.button('Delete cache file and reload'):
            os.remove(today_file)
            st.rerun()

        pretty_print_json(dd['streams'])
    else:
        #st.write('No cache file available, searching for streams...')

        with st.spinner('Looking for streams...'):
            dd = json.loads( get_json_output())   #['nhl']))
            with open(today_file, 'w') as f:
                json.dump(dd, f)
            st.rerun()

except Exception as ex:
    st.write( str(ex))
    if st.button('Delete cache file and reload'):
        os.remove(today_file)
        st.rerun()

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
