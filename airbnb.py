#import packages
import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

#load data
df=pd.read_csv("C:/Users/lenovo/Desktop/New folder/airbnb_data.csv")

# Streamlit application
st.set_page_config(layout= "wide")

option = st.sidebar.radio(":blue[Choose your page]", ["Home", "Data Visualization","Insights"])
    
if option == "Home":
    st.title(':rainbow[AirBnB Data Analysis]')

    st.subheader(":green[Introduction]")

    st.markdown('''Airbnb began in 2008 when two designers who had space to share hosted three travellers looking for a place to stay.
                Now, millions of Hosts and guests have created free Airbnb accounts to enjoy each other's unique view of the world.
                From cozy cottages to elegant penthouses,Hosts are happy to share their places. Whether its a work trip, weekend getaway, family vacation,
                or a longer stay, there are millions of amazing places to visit.''')

    st.markdown(''' On the business front, Airbnb for Work has everything needed to do your job on the road,
                from top-rated places and collaborative spaces to team-building experiences and administrative tools 
                that make managing travel easier than ever.''')

    st.subheader(":green[Project views]")

    st.markdown('''This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, 
                develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations,
                availability patterns, and location-based trends.''')

    st.subheader(':green[Technologies used in this project]')

    st.markdown('''Python scripting, MongoDB Atlas, Exporting CSV file, Handling large dataset, Data Preprocessing,
                Exploratory data analysis, Visualization using Plotly, Streamlit Web Application, Dashboard creation
                using PowerBI. ''')

    col1, col2 = st.columns(2)
    with col2:
        st.image("C:/Users/lenovo/Desktop/New folder/airbnb.jpg",width=600)

if option == 'Data Visualization':
    st.markdown("<h1 style='text-align: center; color: black;'>Airbnb Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: blue;'>Airbnb Property Type Visualization</h2>", unsafe_allow_html=True)

     # Add interactive components for filtering
    selected_country = st.selectbox("Select a country", df['country'].unique())
    price_range = st.slider("Select price range", 0, 3000, (0, 3000))

    # Filter the DataFrame based on the user's selections
    filtered_df = df[(df['country'] == selected_country) &
                     (df['price'] >= price_range[0]) &
                     (df['price'] <= price_range[1])]

    st.subheader('Property Type Visualization')
    
    # Plot the count of property types by number of reviews
    property_reviews = filtered_df.groupby('property_type')['number_of_reviews'].sum().reset_index()
    top_10_property_reviews = property_reviews.nlargest(10, 'number_of_reviews')
    fig1 = px.bar(top_10_property_reviews, x='property_type', y='number_of_reviews')
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("**Top Property Types by Number of Reviews**")

    # Plot the top 5 property types with highest review scores for cleanliness
    property_cleanliness = filtered_df.groupby('property_type')['review_scores_cleanliness'].mean().nlargest(5).reset_index()
    fig2 = px.pie(property_cleanliness, values='review_scores_cleanliness', names='property_type')
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("**Top 5 Property Types with Highest Review Scores for Cleanliness**")

    st.subheader('Price Analysis and Location Distribution')
    
    # Plot the average price by property type for the top 15 property types
    df_avg_price = filtered_df.groupby('property_type')['price'].mean().nlargest(15).reset_index()
    fig3 = px.bar(df_avg_price, x='property_type', y='price', color='price', color_continuous_scale='viridis')
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("**Average Price by Property Type (Top 15)**")

    # Create a choropleth map for the average price by country
    country_agg = df.groupby('country').agg({'price': 'mean'}).reset_index()
    fig4 = px.choropleth(country_agg, locations='country', locationmode='country names', color='price', range_color=[0, 500], color_continuous_scale='Viridis', title='Average Price by Country')
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("**Average Price by Country**")

    st.subheader('Dynamic Filtering and Top Apartment Names')
    
    # Add interactive components for additional filtering
    selected_beds = st.selectbox("Number of beds", sorted(filtered_df['beds'].unique()))
    selected_bedrooms = st.selectbox("Number of bedrooms", sorted(filtered_df['bedrooms'].unique()))
    selected_cancellation_policy = st.selectbox("Cancellation policy", filtered_df['cancellation_policy'].unique())

    # Filter the DataFrame based on the user's selections
    filtered_df = filtered_df[(filtered_df['beds'] == selected_beds) &
                              (filtered_df['bedrooms'] == selected_bedrooms) &
                              (filtered_df['cancellation_policy'] == selected_cancellation_policy)]

    # Ensure there are top 10 apartment names based on the filtered DataFrame
    if len(filtered_df) > 0:
        top_10_names = filtered_df['name'].value_counts().head(10).index
        filtered_top_10_df = filtered_df[filtered_df['name'].isin(top_10_names)]
        fig5 = px.bar(filtered_top_10_df, x='name', y='price', title='Top 10 Apartment Names within Selected Filters')
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown("**Top 10 Apartment Names within Selected Filters**")
    else:
        st.warning("No data available for the selected criteria")


        # Add more sections and visualizations

    st.subheader('Additional Visualizations')

    # Add a line plot showing the trend of prices over time by month
    df['last_scraped'] = pd.to_datetime(df['last_scraped'])
    df['month_year'] = df['last_scraped'].dt.to_period('M').astype(str)

    avg_price_by_month = df.groupby('month_year')['price'].mean().reset_index()
    fig6 = px.line(avg_price_by_month, x='month_year', y='price', title='Average Price Trend Over Time', labels={'price': 'Average Price', 'month_year': 'Month'})
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("**Average Price Trend Over Time**")

if option == 'Insights':
    st.markdown("<h1 style='text-align: center; color: black;'>Airbnb Insights</h1>", unsafe_allow_html=True)

    # Insights based on the data visualization
    st.subheader("Key Insights:")
    st.markdown("1. The top property types by number of reviews are Apartment, House, and Condominium, indicating their popularity among Airbnb users.")
    st.markdown("2. The top 5 property types with the highest review scores for cleanliness are Loft, Tiny House, Bungalow, Cabin, and Cottage, suggesting that these property types are well-maintained and provide a clean experience for guests.")
    st.markdown("3. The average price by property type shows that Penthouse, Villa, and Townhouse have the highest average prices, while Private room, Shared room, and Dorm have the lowest average prices.")
    st.markdown("4. The choropleth map of average price by country reveals that countries like Switzerland, Iceland, and Norway have the highest average prices, while countries like India, Thailand, and Vietnam have the lowest average prices.")
    st.markdown("5. The dynamic filtering and top apartment names section allows users to explore the top 10 apartment names within their selected criteria, providing insights into the most popular and highly-priced listings.")
    st.markdown("6. The average price trend over time shows a seasonal pattern, with prices generally higher during the summer months and lower during the winter months, indicating the impact of travel demand on pricing.")

    st.subheader("Recommendations:")
    st.markdown("1. Hosts should consider offering property types with high review scores for cleanliness, such as Loft, Tiny House, and Bungalow, to attract more guests and maintain a positive reputation.")
    st.markdown("2. Hosts in countries with high average prices, like Switzerland and Iceland, can consider pricing their listings accordingly to maximize revenue, while hosts in countries with lower average prices may need to adjust their pricing to remain competitive.")
    st.markdown("3. Hosts should monitor the seasonal trends in pricing and adjust their listing prices accordingly to capitalize on high-demand periods and remain attractive to guests during low-demand seasons.")
    st.markdown("4. Hosts with top-performing apartment names within the selected filters can analyze the features and amenities of these listings to understand what makes them popular and try to replicate those elements in their own offerings.")

    st.subheader("Future Considerations:")
    st.markdown("1. Analyze the impact of additional factors, such as host ratings, superhost status, and amenities, on pricing and popularity to provide more comprehensive insights.")
    st.markdown("2. Explore the relationship between property type, location, and pricing to identify potential opportunities for hosts to differentiate their listings and optimize their pricing strategies.")
    st.markdown("3. Investigate the impact of external factors, like local events, holidays, and economic conditions, on Airbnb pricing and demand to help hosts make more informed decisions about their listings.")
    st.markdown("4. Expand the analysis to include data from multiple cities or countries to identify global trends and best practices that can be applied across different Airbnb markets.")







    