import streamlit as st
import pandas as pd
import plotly.express as px

city_coordinates = {
    'Warszawa': {'latitude': 52.2297, 'longitude': 21.0122},
    'Łódź': {'latitude': 51.7592, 'longitude': 19.4560},
    'Kraków': {'latitude': 50.0647, 'longitude': 19.9450},
    'Wrocław': {'latitude': 51.1079, 'longitude': 17.0385},
    'Poznań': {'latitude': 52.4064, 'longitude': 16.9252},
    'Gdańsk': {'latitude': 54.3520, 'longitude': 18.6466},
    'Lublin': {'latitude': 51.2465, 'longitude': 22.5684},
    'Szczecin': {'latitude': 53.4285, 'longitude': 14.5528},
    'Bydgoszcz': {'latitude': 53.1235, 'longitude': 18.0084},
    'Białystok': {'latitude': 53.1325, 'longitude': 23.1688},
    'Katowice': {'latitude': 50.2649, 'longitude': 19.0238},
    'Rzeszów': {'latitude': 50.0412, 'longitude': 21.9991},
    'Gdynia': {'latitude': 54.5189, 'longitude': 18.5305},
    'Radom': {'latitude': 51.4027, 'longitude': 21.1471},
    'Kielce': {'latitude': 50.8661, 'longitude': 20.6286},
    'Zamość': {'latitude': 50.7231, 'longitude': 23.2518},
    'Legionowo': {'latitude': 52.4041, 'longitude': 20.9262},
    'Sopot': {'latitude': 54.4416, 'longitude': 18.5601},
    'Olsztyn': {'latitude': 53.7784, 'longitude': 20.4801}
}

st.title("Analysis of Apartment Prices")
st.subheader(body = '''In this project, you can see an analysis of apartment prices in different Polish cities. The data was scraped from the OLX website using the Beautiful Soup library. Then, using Streamlit, I created easy-to-read visualizations. Finally, you can find a model that predicts the price of an apartment based on key features.''')

st.divider()
st.markdown('Below you can see the DataFrame with the scraped data.')
df = pd.read_csv('apartments.csv')
st.dataframe(df)

############################################### PLOTS #######################################################

# Scatter plot
st.divider()
st.markdown('The dependency between the area of the apartment and its price for the chosen city.')
city = st.selectbox("Show plot for:", df['city'].unique())
scatter_fig = px.scatter(df[df['city']==city], 'area', 'price', range_y= (0, max(df['price'][df['city']==city]*1.2)), labels=dict(area='Area, m2', price='Price, PLN'))
st.plotly_chart(scatter_fig)

# Map plot
map_fig = px.scatter_geo(df, lat=city_coordinates[df['city']]['latitude'],
                         lon=city_coordinates[df['city']]['longitude'],
                     size="price"
                     )
st.plotly_chart(map_fig)