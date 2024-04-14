import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout='wide', page_title='Zomato Data Analysis', page_icon='📊')

st.markdown(""" <style>
             div.block-container{
             padding-top:1rem;
             }
             </style>""",unsafe_allow_html= True)

st.markdown(
    f"""
    <h1 style='text-align: center; font-family: Arial, sans-serif;'>Zomato Bangalore Restaurant Analysis</h1>
    """,
    unsafe_allow_html=True
)

st.subheader('Original Dataset')
st.link_button(label='Go', url= 'https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants')

st.subheader('Data Cleaning on Kaggle')
st.link_button(label='Go' , url = 'https://www.kaggle.com/code/rajeevnayantripathi/data-cleaning-eda-on-zomato-bangalore-dataset')

st.subheader('Cleaned Dataset')
df = pd.read_csv('zomato_cleaned.csv')
st.dataframe(df)

st.download_button(label='Download', data=df.to_csv(), file_name='zomato_data.csv')

st.subheader('Objective')

objective_text = """
This Zomato data aims at analyzing the demography of the location. 

- **Theme:** It will help new restaurants in deciding their theme, menus, cuisine, cost, etc. for a particular location.
- **Similarity between Neighborhoods:** It aims at finding similarities between neighborhoods of Bengaluru based on food.
- **Reviews:** The dataset also contains reviews for each restaurant, which will help in finding the overall rating for the place.
"""

st.markdown(objective_text)

st.subheader('Key Analysis Points')

analysis_points_text = """
- **Popularity of different cuisines:** Analyze the popularity of different cuisines in specific locations.
- **Correlation between demographics and food preferences:** Explore the correlation between demographics and food preferences.
- **Competition among restaurants:** Investigate the competition among restaurants in various categories.
- **Consumer needs and preferences:** Identify the needs and preferences of consumers in different neighborhoods.
- **Location of the restaurant:** Determine the location of the restaurant.
- **Approx Price of food:** Analyze the approximate price of food.
- **Locality with maximum number of restaurants:** Identify which locality of the city serves specific cuisines with the maximum number of restaurants.
- **Famous neighborhoods for specific food:** Determine if a particular neighborhood is famous for its own kind of food.
- **Overall Analysis:** Provide valuable insights for restaurant owners and investors to make informed decisions about opening new restaurants or expanding existing ones.
"""
st.markdown(analysis_points_text)

# Basic Feature Engineering

# 1.
num_cuisines = df['cuisines'].str.split(',').str.len()
avg_cost_per_plate = round(df['cost2plates']/num_cuisines).astype('int')
df.insert(9,'avg_cost_per_plate',avg_cost_per_plate )

# 2.
lower = df['rate'].quantile(0.25)
upper = df['rate'].quantile(0.75)

def categorize_rate(x):
  if x < lower:
    return 'low'
  elif lower<= x <=upper:
    return 'mid'
  else:
     return 'high'

rate_category = df['rate'].apply(categorize_rate)
df.insert(4,'rate_category',rate_category )

# 3.
lower = df['votes'].quantile(0.25)
upper = df['votes'].quantile(0.75)

def categorize_vote(x):
  if x < lower:
    return 'low'
  elif lower<= x <=upper:
    return 'mid'
  else:
     return 'high'


vote_category = df['votes'].apply(categorize_vote)
df.insert(6,'vote_category',vote_category )

# 4.
lower = df['avg_cost_per_plate'].quantile(0.25)
upper = df['avg_cost_per_plate'].quantile(0.75)

def categorize_avg_cost_per_plate(x):
  if x < lower:
    return 'low'
  elif lower<= x <=upper:
    return 'mid'
  else:
     return 'high'


cost_category = df['avg_cost_per_plate'].apply(categorize_avg_cost_per_plate)
df.insert(12,'cost_category',cost_category)

df.drop(columns = 'cost2plates',inplace= True)

st.markdown(
    f"""
    <h1 style='text-align: center; font-family: Arial, sans-serif;'> Few Basic Insights</h1>
    """,
    unsafe_allow_html=True
)

col1,col2 = st.columns(2)

with col1:
    temp = df['name'].value_counts().head(20).reset_index()
    fig = px.bar(temp,x='name',y='count',color = 'name',hover_name = 'name',text_auto = True,
             title = 'Top 20 Most Popular Restaurants in Bangalore')
    fig.update_layout(xaxis = dict(title ='restaurant'))
    st.plotly_chart(fig)

with col2:
    temp = df['location'].value_counts().reset_index()
    temp.drop(index=temp[temp['location'] == 'others'].index, inplace=True)
    temp = temp.reset_index(drop=True)
    fig = px.bar(temp, x='location', y='count', color='location', hover_name='location', title='Top Crowded Restaurants Location in Banglore')
    st.plotly_chart(fig)

col1, col2 = st.columns(2)

# Online Order Analysis
with col1:

    temp = df['online_order'].value_counts().reset_index()
    fig1 = px.pie(temp, values='count', names='online_order', hole=0.5,
                  hover_name='online_order', title='Restaurants Providing Online/Offline Facility')
    st.plotly_chart(fig1)

    st.markdown("""
    - **59% of restaurants provide online order facility.**
    - **41% of restaurants do not provide online order facility.**
    - Modern lifestyles favor convenience, prompting a shift towards online food ordering. 
      Factors like traffic congestion and long work hours make dining out less feasible.
    - Online ordering and delivery services offer a solution by providing restaurant-quality meals at home.
    - To stay competitive, the majority of restaurants now offer online ordering facilities. 
      This trend reflects an adaptation to changing consumer behaviors and preferences.
    """)

# Book Table Analysis
with col2:

    temp = df['book_table'].value_counts().reset_index()
    fig2 = px.pie(temp, values='count', names='book_table', hole=0.5,
                  hover_name='book_table', title='Book Table Facility Distribution')
    st.plotly_chart(fig2)

    st.markdown("""
    - **Majority (87.5%) of restaurants do not offer table booking facilities.**
    - **A small percentage (12.5%) of restaurants provide table booking options.**
    - This suggests varying levels of demand for reservation services among customers.
    """)

st.markdown(
    f"""
    <h1 style='text-align: center; font-family: Arial, sans-serif;'>Insights for Opening New Restaurant</h1>
    """,
    unsafe_allow_html=True
)

st.subheader('1. Online Ordering and Table Booking facilities for optimal customer engagement')
st.markdown("""- This title underscores the importance of incorporating both online ordering and table booking facilities for
            enhancing customer engagement and provides valuable insights for prospective restaurant owners aiming to open a new establishment.""")

col1, col2 = st.columns(2)

with col1:
  indexing = df[df['location'].str.contains('others')].index
  temp= df.copy()
  temp.drop(index = indexing,inplace = True)
  temp_df = pd.crosstab(temp['location'],temp['online_order'])
  fig = px.bar(temp_df,x=temp_df.index,y=temp_df.columns,barmode='group',title = 'Online/Offline Orders vs Location',color_discrete_map={'Yes':'Red','No':'Blue'})
  st.plotly_chart(fig)

with col2:
    st.markdown(""" 
    1. Restaurants in locality of **(Church Street ,Electronic City, Lavelle Road, MG Road, Residency Road)** has 
    less number of online ordering restaurants.
    2. This statement simply explains that there are fewer restaurants offering online ordering services in the mentioned areas.
    3. Recognizing areas with lower availability of online ordering restaurants highlights potential market gaps""")

st.divider()


temp = (df.groupby('online_order').agg({'rate':'mean','votes':'mean','avg_cost_per_plate':'mean'})).round(2)
st.dataframe(temp)

fig = px.treemap(df, path=[px.Constant('Online Order Facility'), 'online_order', 'location'],
                     color='avg_cost_per_plate', color_continuous_scale='plasma',
                    title = 'Average Cost per plate based on Online/Offline Order facility')

fig.update_layout(height = 500, width = 1200)
st.plotly_chart(fig)

col1,col2 = st.columns(2)

with col1:
    st.markdown("""
- **Rate:** Restaurants offering online orders (Yes) have a slightly higher average rating (3.23) compared to those without online orders (No) with a rating of 3.15.
- **Votes:** Restaurants with online orders (Yes) receive more votes on average (307.92) compared to those without (No) with an average of 251.20 votes.
- **Avg_cost_per_plate:** Restaurants with online orders (Yes) have a lower average cost per plate (₹462.10) compared to those without (No) with an average cost per plate of ₹533.25.
From this data:

- **Moderate Rate Improvement:** Restaurants offering online orders tend to have a slightly higher average rating compared to those without, though the difference is not substantial.
 - There is no significant difference in the avg. rating of restaurants that offer online ordering compared to those that don't.
 - The overall rating of a restaurant mostly depends on two things:
   - the quality of the food
   - the service provided.
 - Customers rate a restaurant based on how good the food tastes and looks, and how well they were treated by the staff.""")

with col2 :
  st.markdown("""  
 - While online ordering can be convenient, it doesn't really affect these important factors that shape the overall rating. So, while it's handy, it's not the main thing customers consider when rating a restaurant.

- **Increased Votes:** There's a noticeable difference in the number of votes between restaurants with and without online orders. Restaurants offering online orders receive more votes on average, suggesting that this service may attract more attention and engagement from customers.

- **Lower Average Cost per Plate:** Interestingly, restaurants offering online orders have a lower average cost per plate compared to those without. 
 - This suggests that there may be cost-saving benefits associated with online ordering.
 - This data underscores the **importance of optimizing online ordering** systems to enhance customer experience and capitalize on potential savings.
 - Businesses may want to consider **promoting and incentivizing** online ordering to potentially reduce costs and attract more customers.
 - This might indicate that restaurants cater to a broader demographic, including customers who are more price-conscious and prefer the convenience of ordering online.
""")


st.divider()


temp = (df.groupby('book_table').agg({'rate':'mean','votes':'sum','avg_cost_per_plate':'mean'})).round(2)
st.dataframe(temp)

fig = px.treemap(df, path=[px.Constant('Book Table Facility'), 'book_table', 'location'], color='avg_cost_per_plate'
                   , color_continuous_scale= 'plasma')
fig.update_layout(height=500, width=1200)
st.plotly_chart(fig)

st.markdown("""
  - **Rate:** Restaurants with table booking (Yes) have a higher average rating (3.76) compared to those without (No) with a rating of 3.12.
  - **Votes:** There's a slightly higher number of votes for restaurants with table booking (7,355,716) compared to those without (7,219,584).
  - **Avg_cost_per_plate:** Restaurants with table booking (Yes) have a significantly higher average cost per plate (₹1215.30) compared to those without (No) with an average cost per plate of ₹387.54.
  Based on this data:
  - **Better Service:** The higher average rating for restaurants with table booking services suggests that they may indeed provide better service, leading to increased customer satisfaction.
  - **Comparable Votes:** While there is a slight difference in the number of votes between restaurants with and without table booking, it's not a substantial difference, suggesting that the presence of table booking might not significantly influence the number of votes a restaurant receives.
  - **Wealthier Crowd:** The significantly higher average cost per plate for restaurants with table booking services implies that they may cater to a wealthier clientele who are willing to spend more on dining experiences.
  """)

st.divider()

indexing = df[df['rest_type'].str.contains('others')].index
temp= df.copy()
temp.drop(index = indexing,inplace = True)
temp_df = ((pd.crosstab(temp['online_order'],temp['rest_type'],normalize = 'index'))*100).round()


col1,col2 = st.columns(2)

with col1:
  fig = px.imshow(temp_df,text_auto = True,color_continuous_scale = 'viridis',title = 'Comparison of Online and Offline Ordering by Restaurant Type')
  st.plotly_chart(fig)

with col2:
  st.markdown("""
  - Based on the data, it's evident that **Quick Bites and Casual Dining** are the most common types of restaurants, both for those offering online ordering and those not offering it.
  - This indicates that Quick Bites and Casual Dining establishments are popular choices for customers, whether they prefer to order online or offline.
  - The distribution of restaurant types between online and offline ordering categories is quite similar. This suggests that the availability of online ordering doesn't significantly alter the distribution of restaurant types.
  - Despite the prevalence of Quick Bites and Casual Dining, there might be opportunities for other types of restaurants, such as **Cafes or Dessert Parlors, to explore and potentially expand their online ordering services** to cater to changing consumer preferences.
  """)

st.divider()

# Location

st.subheader("2. Strategic Location Analysis: Enhancing New Restaurant Success through Data-Driven Insights")
st.markdown("""- This title emphasizes the importance of choosing the right location for a new restaurant and highlights 
how analyzing location data can provide valuable insights into factors such as foot traffic, proximity to residential or commercial areas, and potential competitors""")

col1,col2 = st.columns(2)
with col1:
  indexing = df[df['location'].str.contains('others')].index
  temp= df.copy()
  temp.drop(index = indexing,inplace = True)
  temp_df = pd.crosstab(temp['location'],temp['book_table'])
  fig = px.bar(temp_df, x=temp_df.index, y=temp_df.columns, barmode='group',color_discrete_map={'Yes':'Red','No':'Blue'},
               title = 'Presence of Table Booking Facilities Across Different Locations')
  st.plotly_chart(fig)

with col2:
  st.markdown("""
  - The visualization highlights variations in the availability of table booking facilities across different locations.
  - Certain locations show a higher concentration of restaurants offering table booking, indicating potentially higher demand or preference for this service.
  - Conversely, some locations have fewer restaurants with table booking facilities, suggesting potential opportunities for new openings to cater to this demand.
  - New restaurants aiming to provide table booking services may **benefit from targeting locations where such facilities are less prevalent**, thus filling a gap in the market and potentially attracting more customers.
  - Understanding the distribution of table booking facilities across
    various locations can inform strategic decisions for restaurant owners and investors looking to optimize their offerings and target specific demographics.""")

st.divider()

col1,col2 = st.columns(2)

with col1:
  temp = (df.groupby('location')['avg_cost_per_plate'].mean()).round().sort_values(ascending = False).reset_index()
  fig = px.bar(temp,x='location',y='avg_cost_per_plate',color='location',text_auto = True,hover_name = 'avg_cost_per_plate',
               title = 'Average cost per plate on different Locations')
  fig.update_layout(yaxis=dict(title='Avgerage cost per plate'))
  st.plotly_chart(fig)

with col2:
  st.markdown("""
- The visualization displays the average cost per plate across various locations.
- It appears that certain locations tend to have higher average costs per plate compared to others.
- **Church Street tops the list with the highest average cost per plate at ₹711.**
- **This is followed by Brigade Road at ₹702 , MG Road at ₹700.**
- **Banashankri has the lowest average cost per plate at ₹336.**
- Understanding these variations can be useful for both customers and restaurant owners.
- Customers can plan their dining budgets accordingly based on the average costs in different locations.
- For restaurant owners, this information can guide pricing strategies, especially when considering opening new establishments or adjusting menu prices in existing ones.
- Additionally, it underscores the importance of considering location-specific factors when analyzing cost dynamics in the restaurant industry.""")
st.divider()

col1,col2 = st.columns(2)

with col1:
    indexing = df[df['location'].str.contains('others')].index
    temp = df.copy()
    temp.drop(index=indexing, inplace=True)

    temp_df = pd.crosstab(temp['location'], temp['cost_category'])
    fig = px.bar(temp_df, x=temp_df.index, y=temp_df.columns,
                 title='Distribution of Cost Categories Among Restaurants Across Locations')
    st.plotly_chart(fig)

with col2:
    st.markdown("""
    - It provides insights into the affordability and pricing diversity of dining options in various areas.
    - Some locations may have a higher concentration of restaurants falling into specific cost categories, indicating potential dining preferences or economic demographics.
    - Understanding these patterns can help customers make informed decisions about where to dine based on their budget and desired dining experience.
    - For restaurant owners and investors, this data can inform strategic decisions regarding pricing strategies, menu offerings, and location selection to cater to the preferences and affordability levels of the target market in each location.""")

st.divider()

col1,col2 = st.columns(2)

with col1:

    temp = (df.groupby('location')['votes'].mean()).round(2).sort_values(ascending=False).reset_index()
    temp.drop(index=temp[temp['location'] == 'others'].index, inplace=True)
    fig = px.bar(temp, x='location', y='votes', color='location', text_auto=True, hover_name= 'location',
                 title='Average Restaurant Voting on Different Location')
    st.plotly_chart(fig)

with col2:
    temp = (df.groupby('location')['rate'].mean()).round(2).sort_values(ascending=False).reset_index()
    temp.drop(index=temp[temp['location'] == 'others'].index, inplace=True)
    fig = px.bar(temp, x='location', y='rate', color='location', text_auto=True,hover_name= 'location',
                 title='Average Restaurant Rating on Different Location')
    st.plotly_chart(fig)


st.markdown("""
- Certain locations may have a higher average number of votes, indicating greater customer engagement and potentially higher levels of patronage.
- This suggests that some areas may be more popular dining destinations or have a higher density of restaurants attracting more attention from customers.
- Understanding the distribution of votes across locations can help customers in choosing dining destinations and assist restaurant owners in evaluating the performance of their establishments relative to competitors in the same area.
- Additionally, this information can inform marketing strategies, location-based promotions, and business expansion plans for restaurant owners.
- **Targeted Marketing:** Owners can tailor marketing efforts based on the popularity of their restaurant's location. If the area has a high average number of votes, they can leverage this popularity in advertising campaigns to attract more customers.
- **Expansion Opportunities:** Analyzing locations with high levels of customer engagement can inform decisions about where to open new branches or expand existing ones. Areas with a strong track record of votes may present good opportunities for business growth.
""")
st.divider()


temp = pd.crosstab(df['rest_type'], df['location'])

fig = px.imshow(temp,title='Location-wise Distribution of Restaurant types', color_continuous_scale='cividis', height=600, width=900)
fig.update_layout(yaxis = dict(title = 'restaurant type'))
st.plotly_chart(fig)
st.divider()


# Cuisines
st.subheader("3. Cuisine: Tailoring Menu Offerings to Local Tastes for New Restaurant Ventures")
st.markdown("""- This title highlights the importance of understanding popular cuisines in the area for guiding menu planning and catering to local preferences, which is essential for prospective restaurant ventures""")

col1,col2 = st.columns(2)

with col1:
  indexing = df[df['cuisines'].str.contains('others')].index
  temp= df.copy()
  temp.drop(index = indexing,inplace = True)
  temp_df = ((pd.crosstab(temp['online_order'],temp['cuisines'],normalize = 'index')*100).round())
  fig = px.imshow(temp_df, color_continuous_scale = 'viridis',title = 'Percentage Distribution of Restaurant Cuisines by Online/Offline Ordering Preference"')
  st.plotly_chart(fig)

with col2:
    st.markdown("""
- **North Indian, South Indian, and Chinese** cuisines emerge as the most commonly ordered or favored cuisines, whether through online or offline orders in Bangalore.
- These popular cuisines maintain their dominance regardless of whether the orders are placed online or offline. This suggests that customer preferences for these cuisines remain consistent across different ordering methods.
- Understanding the popularity of specific cuisines across different ordering channels can guide restaurants in adapting their menus and services to meet the demands of the market effectively.""")

st.divider()

col1,col2 = st.columns(2)

with col1:
    temp = df.copy()
    indexing = df[df['cuisines'].str.contains('others')].index
    temp.drop(index=indexing, inplace=True)
    temp_df = (pd.crosstab(temp['book_table'],temp['cuisines'],normalize = 'index')*100).round()
    fig = px.imshow(temp_df,color_continuous_scale = 'jet',title = 'Percentage Distribution of Restaurant Cuisines by Table Booking Availability')
    st.plotly_chart(fig)

with col2:
    st.markdown("""
- The data indicates that regardless of whether restaurants offer table booking facilities or not, **North Indian, South Indian, and Chinese cuisines** are consistently favored or commonly ordered.
- This suggests that the availability of table booking facilities doesn't significantly influence the popularity of these cuisines.
- Therefore, restaurants specializing in these cuisines may focus on other aspects of their operations besides table booking to attract and retain customers.
- However, a helpful tip for new restaurants is to consider offering these cuisines if they plan to provide table booking. This strategy can attract more customers and make the restaurant more competitive.""")

st.divider()

col1 , col2 = st.columns(2)
with col1:
  # Calculate less crowded and more crowded places
  temp = df['location'].value_counts().reset_index()
  temp.drop(index=1, inplace=True)
  temp = temp.reset_index(drop=True)

  less_crowded = temp[temp['count'] <= temp['count'].quantile(0.5)]['location'].tolist()
  more_crowded = temp[temp['count'] > temp['count'].quantile(0.5)]['location'].tolist()

  # Filter data for less crowded and more crowded places
  temp1 = df[df['location'].isin(less_crowded)]
  temp2 = df[df['location'].isin(more_crowded)]

  # Remove 'others' from cuisines
  indexing1 = temp1[temp1['cuisines'].str.contains('others')].index
  indexing2 = temp2[temp2['cuisines'].str.contains('others')].index

  temp1.drop(index=indexing1, inplace=True)
  temp2.drop(index=indexing2, inplace=True)

  # Calculate cross-tabulation for both subsets
  temp_df1 = pd.crosstab(temp1['location'], temp1['cuisines'])
  temp_df2 = pd.crosstab(temp2['location'], temp2['cuisines'])

  fig = px.imshow(temp_df1,color_continuous_scale='viridis')
  fig.update_layout(title='Less Crowded Places and Preferred Cuisines')
  st.plotly_chart(fig)

with col2:
  fig = px.imshow(temp_df2,color_continuous_scale='viridis')
  fig.update_layout(title='More Crowded Places and Preferred Cuisines')
  st.plotly_chart(fig)

st.divider()

temp = df.copy()
indexing = df[df['cuisines'].str.contains('others') | df['rest_type'].str.contains('others')].index
temp.drop(index=indexing, inplace=True)
temp_df = (pd.crosstab(temp['rest_type'],temp['cuisines'],normalize ='columns')*100).round()
fig = px.imshow(temp_df,color_continuous_scale = 'jet',height = 500, title = 'Distribution of Cuisines by Restaurant Type')
fig.update_layout(width=1100,height = 600)
fig.update_layout(yaxis = dict(title= 'Restaurant Type'))
st.plotly_chart(fig)
st.divider()


st.markdown("""
- Restaurants serving **North Indian ,Chinese and South Indian** cuisines are the most popular choices among customers, in different rate and vote_category.
- This indicates that diners highly appreciate these cuisines. Such restaurants have a great opportunity to attract more customers and become preferred dining spots.""")

temp = df.copy()
indexing = df[df['cuisines'].str.contains('others')].index
temp.drop(index=indexing, inplace=True)

temp_df1 = pd.crosstab(temp['rate_category'], temp['cuisines'])
temp_df2 = pd.crosstab(temp['vote_category'], temp['cuisines'])

# Create subplots
fig = make_subplots(rows=2, cols=1, subplot_titles=("Rate Category vs. Cuisine", "Vote Category vs. Cuisine"),shared_xaxes = True)

fig.add_trace(go.Heatmap(x=temp_df1.columns, y=temp_df1.index, z=temp_df1.values, colorscale='plasma'), row=1, col=1)

fig.add_trace(go.Heatmap(x=temp_df2.columns, y=temp_df2.index, z=temp_df2.values, colorscale='plasma'), row=2, col=1)

fig.update_layout(width=1000,height = 600)

st.plotly_chart(fig)

st.divider()

st.subheader("4. Rating and Votes: Harnessing Customer Feedback for Restaurant Success")
st.markdown("""
- This title emphasizes the significance of high ratings and a large number of votes in indicating customer satisfaction and popularity. It underscores how leveraging customer feedback can offer valuable insights into a restaurant's potential success""")

col1,col2 = st.columns(2)

with col1:
    fig = px.scatter(df, x='votes', y='rate', color='votes', color_continuous_scale='plasma', title=' Restaurant Rating vs Votes')
    fig.update_layout(yaxis = dict(title = 'Rating'))
    st.plotly_chart(fig)
    st.write('- As restaurants rating increases , number of votes also increases.')

with col2:
    fig = px.scatter(df, x='avg_cost_per_plate', y='rate', color='votes', color_continuous_scale='plasma', title=' Restaurant Rating vs Avg. cost per plate')
    fig.update_layout(xaxis=dict(title='avgerage cost per plate'), yaxis=dict(title='Rating'))
    st.plotly_chart(fig)
    st.write('- As restaurants rating increases , avg. cost per plate also increases')

st.divider()

temp = pd.crosstab(df['vote_category'],df['rest_type'])
fig = px.bar(temp, x= temp.index, y = temp.columns , barmode = 'group',title = 'Vote Category vs Restaurant type')
fig.update_layout(xaxis=dict(title= 'vote category'), yaxis=dict(title= 'Restaurant type'))
st.plotly_chart(fig)

st.divider()

st.subheader('5. Type of Restaurant (Rest Type)')
st.markdown(""" - The type of restaurant (e.g., Casual Dining, Quick Bites) can influence the ambiance, menu offerings, and target audience.""")

col1,col2 = st.columns(2)

with col1:
    temp = (df.groupby('rest_type')['avg_cost_per_plate'].mean()).round().sort_values(ascending=False).reset_index()
    temp.drop(index=temp[temp['rest_type'] == 'others'].index, inplace=True)
    fig = px.bar(temp, x='rest_type', y='avg_cost_per_plate', color='rest_type', text_auto=True, title='Average cost per plate on different Restaurant type')
    fig.update_layout(yaxis = dict(title = 'Average cost per plate'), xaxis = dict(title = 'Restaurant Type'))
    st.plotly_chart(fig)

with col2:
    st.markdown("""
- The analysis provides insights into the average cost per plate across different restaurant types.
- Casual Dining with a Bar has the highest average cost per plate, followed by Casual Dining and Cafe.
- Quick Bites and Bakery establishments have relatively lower average costs per plate.
- Understanding these variations can assist both customers and restaurant owners in making informed decisions.
- **Pricing Strategies:** Owners can adjust their pricing strategies based on the average cost per plate within their restaurant type category. For example, if they operate a Casual Dining establishment, they may consider setting prices in line with the average cost per plate for Casual Dining restaurants.
- **Menu Planning:** Understanding the average cost per plate for different restaurant types can guide menu planning. Owners can optimize their menu offerings to align with customer expectations and pricing norms within their restaurant category.""")


col1,col2 = st.columns(2)

with col1:
    temp = (df.groupby('rest_type')['rate'].mean()).round(2).sort_values(ascending=False).reset_index()
    temp.drop(index=temp[temp['rest_type'] == 'others'].index, inplace=True)
    fig = px.bar(temp, x='rest_type', y='rate', color='rest_type', text_auto=True,title='Average Rating of different Restaurant type')
    fig.update_layout(xaxis=dict(title='Restaurant Type'))
    st.plotly_chart(fig)

with col2:
    temp = (df.groupby('rest_type')['votes'].mean()).round(2).sort_values(ascending=False).reset_index()
    temp.drop(index=temp[temp['rest_type'] == 'others'].index, inplace=True)
    fig = px.bar(temp, x='rest_type', y='votes', color='rest_type', text_auto=True,title='Average Voting of different Restaurant type')
    fig.update_layout(xaxis=dict(title='Restaurant Type'))
    st.plotly_chart(fig)

st.divider()

st.write(
    "For more in-depth insights, visit my Kaggle notebook [here](https://www.kaggle.com/code/rajeevnayantripathi/data-cleaning-eda-on-zomato-bangalore-dataset)")

# Custom CSS for footer
footer_style = """
    <style>
        .footer {
            position: fixed;
            bottom: 20px;
            right: 20px;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            text-decoration: none;
            color: #000000;
        }
        .footer p {
            margin: 0;
            font-size: 14px;
        }
        .footer a {
            display: flex;
            align-items: center;
            text-decoration: none;
            color: #000000;
            margin-bottom: 5px;
        }
        .footer a img {
            margin-right: 5px;
        }
    </style>
"""

# Footer content
footer_content = """
    <div class="footer">
        <p>Made with ❤️ by Rajeev Nayan Tripathi</p>
        <a href="https://www.linkedin.com/in/rajeev-nayan-tripathi-1499581b7/" target="_blank">
            <img src="https://img.icons8.com/color/48/000000/linkedin.png"/>
        </a>
        <a href="mailto:rajeevnayantripathi36@gmail.com" target="_blank">
            <img src="https://img.icons8.com/color/48/000000/gmail--v1.png"/>
        </a>
    </div>
"""

# Display the footer
st.markdown(footer_style, unsafe_allow_html=True)
st.markdown(footer_content, unsafe_allow_html=True)











