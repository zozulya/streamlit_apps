import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from vega_datasets import data

# Since these data are each more than 5,000 rows we'll import from the URLs
airports = data.airports.url
flights_airport = data.flights_airport.url

states = alt.topo_feature(data.us_10m.url, feature="states")

# Create pointerover selection
select_city = alt.selection_point(
    on="pointerover", nearest=True, fields=["origin"], empty=False
)

# Define which attributes to lookup from airports.csv
lookup_data = alt.LookupData(
    airports, key="iata", fields=["state", "latitude", "longitude"]
)

background = alt.Chart(states).mark_geoshape(
    fill="lightgray",
    stroke="white"
).properties(
    width=750,
    height=500
).project("albersUsa")

connections = alt.Chart(flights_airport).mark_rule(opacity=0.35).encode(
    latitude="latitude:Q",
    longitude="longitude:Q",
    latitude2="lat2:Q",
    longitude2="lon2:Q"
).transform_lookup(
    lookup="origin",
    from_=lookup_data
).transform_lookup(
    lookup="destination",
    from_=lookup_data,
    as_=["state", "lat2", "lon2"]
).transform_filter(
    select_city
)

points = alt.Chart(flights_airport).mark_circle().encode(
    latitude="latitude:Q",
    longitude="longitude:Q",
    size=alt.Size("routes:Q").legend(None).scale(range=[0, 1000]),
    order=alt.Order("routes:Q").sort("descending"),
    tooltip=["origin:N", "routes:Q"]
).transform_aggregate(
    routes="count()",
    groupby=["origin"]
).transform_lookup(
    lookup="origin",
    from_=lookup_data
).transform_filter(
    (alt.datum.state != "PR") & (alt.datum.state != "VI")
).add_params(
    select_city
)

st.write(background + connections + points)
# st.header('st.button')

# if st.button('Say hello'):
#      st.write('Why hello there')
# else:
#      st.write('Goodbye')

# st.header('st.write')
# # Example 1
# st.write('Hello, *World!* :sunglasses:')
# # Example 2
# st.write(1234)

# # Example 3
# df = pd.DataFrame({
#         'first column': [1, 2, 3, 4],
#         'second column': [10, 20, 30, 40]
#         })
# st.write(df)

# # Example 4
# st.write('Below is a DataFrame:', df, 'Above is a dataframe.')

# # Example 5
# df2 = pd.DataFrame(
#         np.random.randn(200, 3),
#         columns=['a', 'b', 'c'])
# c = alt.Chart(df2).mark_circle().encode(
#         x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
# st.write(c)   

# add_sidebar = st.sidebar.selectbox("Options", ["Add", "Subtract"])

# if add_sidebar == "Add":
#     st.write(f"The result is {2 + 2}")  
# else:
#      st.selectbox("Videos", ("funny", "cat", "dog"))