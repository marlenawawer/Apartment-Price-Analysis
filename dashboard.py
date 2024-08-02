import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Analysis of Apartment Prices")
st.subheader('In this project, you can see an analysis of apartment prices in different Polish cities. The data was scraped from the OLX website using the Beautiful Soup library. Then, using Streamlit, I created easy-to-read visualizations. Finally, you can find a model that predicts the price of an apartment based on key features.')
st.subheader('All prices are in PLN, and the area is measured in m².')

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
avg_price = merge_df.groupby(['city', 'latitude', 'longitude'])['price_per_m2'].mean().reset_index()
avg_price['price_per_m2'] = round(avg_price['price_per_m2'], 0)
map_fig = px.scatter_mapbox(avg_price, lat='latitude',
                            lon = 'longitude', mapbox_style=styles[1],
                            zoom=4.2, color='price_per_m2', size='price_per_m2', text='city', color_continuous_scale='bluered',
                            title="Average Apartment Price per m2 in Major Polish Cities", hover_name='city'
)
map_fig.update_traces(textfont=dict(color='black', size=10))
st.plotly_chart(map_fig)
st.dataframe(avg_price[['city', 'price_per_m2']].sort_values('price_per_m2', ascending=False), hide_index=True)
st.markdown('Based on the average price per m², the most expensive apartments are in Warsaw, Sopot, and Kraków, while the cheapest ones are in Bydgoszcz, Radom, and Zamość.')

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
y = st.selectbox("Y:", ['price', 'area', 'price_per_m2'])
color = st.selectbox("Color by:", df.columns.drop([x,y]))
scatter_fig = px.scatter(df, x=x, y=y, color=color, color_continuous_scale='bluered')
st.plotly_chart(scatter_fig)
st.markdown('The majority of apartments on lower levels are located in tenements. The most expensive apartment is a 148 m² unit located in Warsaw, Śródmieście, in a tenement building, priced at 3.34 million PLN. One-room apartments cost less than one million PLN.')

# Calculation
st.divider()
st.markdown('Calculate the average price per m² or the overall price based on chosen parameters.')
param = st.multiselect("Parameters:", ['level', 'building', 'num_of_rooms', 'city', 'district'], default=['city', 'district'])
show = st.multiselect("Show:", ['price', 'price_per_m2'], default='price_per_m2')
calc_df = df.groupby(param)[show].mean().reset_index()
st.dataframe(calc_df.round(0).sort_values('city'), hide_index=True)
calc_df['params'] = calc_df[param].agg(', '.join, axis=1)

st.markdown('To make it easier, you can see a visualization of the table above.')
bar_fig = px.bar(calc_df.sort_values('city'), 'params', show)
st.plotly_chart(bar_fig)

# Model
st.divider()