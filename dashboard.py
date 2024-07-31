import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Analysis of Apartment Prices")
st.subheader(body = '''In this project, you can see an analysis of apartment prices in different Polish cities. The data was scraped from the OLX website using the Beautiful Soup library. Then, using Streamlit, I created easy-to-read visualizations. Finally, you can find a model that predicts the price of an apartment based on key features.''')

st.divider()
st.markdown('Below you can see the DataFrame with the scraped data.')
df = pd.read_csv('apartments.csv', thousands=' ')
st.dataframe(df, hide_index=True)

############################################### PLOTS #######################################################

# Scatter plot
st.divider()
st.markdown('The dependency between the area of the apartment and its price for the chosen city.')
city = st.selectbox("Show plot for:", df['city'].unique())
scatter_fig = px.scatter(df[df['city']==city], 'area', 'price', color='district', range_y= (0, max(df['price'][df['city']==city]*1.2)), labels=dict(area='Area, m2', price='Price, PLN'))
st.plotly_chart(scatter_fig)

# Map plot
st.divider()
styles = ['open-street-map', 'carto-positron']
city_coor = pd.read_csv('city_coordinates.csv')
merge_df = pd.merge(df, city_coor, on='city')
avg_price = merge_df.groupby(['city', 'latitude', 'longitude'])['price'].mean().reset_index()
avg_price['price'] = round(avg_price['price'], 0)
map_fig = px.scatter_mapbox(avg_price, lat='latitude',
                            lon = 'longitude', mapbox_style=styles[1],
                            zoom=4.2, color='price', size='price', text='city', color_continuous_scale='bluered',
                            title="Average Apartment Price in Major Polish Cities", hover_name='city'
)
map_fig.update_traces(textfont=dict(color='black', size=10))
st.plotly_chart(map_fig)
st.dataframe(avg_price[['city', 'price']].sort_values('price', ascending=False), hide_index=True)
st.markdown('The most expensive apartments are in Warsaw, Sopot, and Kraków, while the cheapest ones are in Łódź, Radom, and Zamość.')

# Hist plot
st.divider()
st.markdown('The number of advertisments based on a choosen category.')
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
x_hist = st.selectbox("X: ", df.select_dtypes(exclude='number').columns.drop('district'))
hist_fig = px.histogram(df, x=x_hist)
st.plotly_chart(hist_fig)
st.markdown('The majority of apartments are located between the ground floor and the fourth floor in blocks of flats. They are typically from the secondary market and usually have 2-3 rooms.')

# Scatter plot
st.divider()
st.markdown('The dependency between choosen variables.')
x = st.selectbox("X:", ['level', 'building', 'num_of_rooms', 'city'])
y = st.selectbox("Y:", ['price', 'area'])
color = st.selectbox("Color by:", df.columns.drop([x,y]))
scatter_fig = px.scatter(df, x=x, y=y, color=color)
st.plotly_chart(scatter_fig)
st.markdown('The majority of apartments on lower levels are located in tenements. The most expensive apartment is a 148 m² unit located in Warsaw, Śródmieście, in a tenement building, priced at 3.34 million PLN. One-room apartments cost less than one million PLN.')

# Calculation
st.divider()
st.markdown('Calculate the average price based on a choosen parameters.')
param = st.multiselect("Parameters:", ['level', 'building', 'num_of_rooms', 'city', 'district'], default=['city', 'district'])
show = st.multiselect("Show:", ['area', 'price'], default='price')
calc_df = df.groupby(param)[show].mean().reset_index()
st.dataframe(calc_df.round(0), hide_index=True)