
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
import sqlite3
import folium
from geopy.geocoders import Nominatim
from matplotlib.colors import LinearSegmentedColormap
from IPython.display import display
import warnings

warnings.filterwarnings('ignore')


#creating database connection
conn = sqlite3.connect('yelp.db')

tables = pd.read_sql_query("SELECT name from sqlite_master where type = 'table'" , conn)

tables

for table in tables['name'] :
    display(pd.read_sql_query(f"select * from {table} limit 5" , conn))

    business_id = pd.read_sql_query("""select business_id , review_count 
                                  from business 
                                  where lower(categories) like '%restaurant%' and is_open = 1""" ,
                                conn)
business_id

business_id = pd.read_sql_query("""select business_id , review_count 
                                  from business 
                                  where lower(categories) like '%restaurant%' and is_open = 1""" ,
                                conn)
business_id

# What is the descriptive stats for review count and star rating for businesses?
# avg, min, max, median

query = f"""
SELECT 
    AVG(review_count) AS average_review_count,
    MIN(review_count) AS min_review_count,
    MAX(review_count) AS max_review_count,
    (SELECT review_count  FROM business ORDER BY review_count LIMIT 1 OFFSET (SELECT COUNT(*) FROM business ) / 2 ) AS median_review_count ,

    AVG(stars) AS average_star_rating,
    MIN(stars) AS min_star_rating,
    MAX(stars) AS max_star_rating,
    (SELECT stars FROM business ORDER BY stars LIMIT 1 OFFSET (SELECT COUNT(*) FROM business ) / 2 ) AS median_star_rating


FROM business
WHERE business_id IN {tuple(business_id['business_id'].tolist())} ;
"""

result_df = pd.read_sql_query(query, conn)
display(result_df.transpose())



# Which restaurants have the highest number of reviews?
pd.read_sql_query(f"""
select name, sum(review_count) as review_count, avg(stars) as avg_rating
from business
where business_id in {tuple(business_id['business_id'].tolist())}
group by name
order by review_count desc
limit 10
""", conn)


# Which restaurants have the highest rating ?
pd.read_sql_query(f"""
select name, sum(review_count) as review_count, avg(stars) as avg_rating
from business
where business_id in {tuple(business_id['business_id'].tolist())}
group by name
order by avg_rating desc
limit 10
""", conn)

# Do restaurants with higher engagement tend to have higher ratings?

pd.read_sql_query("""
select business_id, 
sum(length(date) - length(replace(date, ',', '')) + 1) as checkin_count
from checkin
group by business_id
""", conn)


pd.read_sql_query("""
select business_id, count(*) as tip_count
from tip
group by business_id
""", conn)



review_count_df = pd.read_sql(f"""
SELECT total.avg_rating as rating,
    AVG(total.review_count) as avg_review_count,
    AVG(total.checkin_count) as avg_checkin_count,
    AVG(total.tip_count) as avg_tip_count
FROM (
    SELECT 
        b.business_id,
        SUM(b.review_count) AS review_count,
        AVG(b.stars) AS avg_rating,
        SUM(LENGTH(cc.date) - LENGTH(REPLACE(cc.date, ',', '')) + 1) AS checkin_count,
        SUM(tip.tip_count) as tip_count
    FROM business b
    LEFT JOIN checkin cc ON b.business_id = cc.business_id
    LEFT JOIN (
        SELECT business_id, COUNT(business_id) AS tip_count 
        FROM tip 
        GROUP BY business_id 
        ORDER BY tip_count
    ) AS tip ON b.business_id = tip.business_id
    WHERE b.business_id IN {tuple(business_id['business_id'].tolist())}
    GROUP BY b.business_id
) AS total
GROUP BY total.avg_rating
""" , conn)

review_count_df

plt.figure(figsize=(15,5))
plt.title('AVG Engagement based on Rating\n\n')
plt.yticks([])
plt.xticks([])
plt.subplot(1,3,1)
plt.title('Review Count')
plt.barh(review_count_df['rating'].astype('str'), review_count_df['avg_review_count'], edgecolor='k', color='#CB7548')
plt.gca().spines['right'].set_visible(False)
for i, value in enumerate(review_count_df['avg_review_count']):
    plt.text(value + 3, i, str(round(value)), color='black', va='center')


plt.xticks([])
plt.subplot(1,3,2)
plt.title('Checkin Count')
plt.barh(review_count_df['rating'].astype('str'), review_count_df['avg_checkin_count'], edgecolor='k', color='#F8862C')
plt.gca().spines['right'].set_visible(False)
for i, value in enumerate(review_count_df['avg_checkin_count']):
    plt.text(value + 3, i, str(round(value)), color='black', va='center')

plt.xticks([])
plt.subplot(1,3,3)
plt.title('Tip Count')
plt.barh(review_count_df['rating'].astype('str'), review_count_df['avg_tip_count'], edgecolor='k', color='#E54F29')
for i, value in enumerate(review_count_df['avg_tip_count']):
    plt.text(value + 0.5, i, str(round(value)), color='black', va='center')

plt.xticks([])
plt.show()


# Is there a correlation between the number of reviews, tips, and check-ins for a business?
engagement_df  = pd.read_sql_query(f"""
SELECT 
    b.business_id,
    SUM(b.review_count) AS review_count,
    AVG(b.stars) AS avg_rating,
    SUM(LENGTH(cc.date) - LENGTH(REPLACE(cc.date, ',', '')) + 1) AS checkin_count,
    SUM(tip.tip_count) AS tip_count,
    (CASE WHEN b.stars >= 3.5 THEN 'High-Rated' ELSE 'Low-Rated' END) AS category
FROM 
   business b
LEFT JOIN 
  checkin cc ON b.business_id = cc.business_id
LEFT JOIN (
    select business_id, count(business_id) as tip_count 
    from tip 
    GROUP BY business_id 
    ORDER BY tip_count
) as tip on b.business_id = tip.business_id
    WHERE b.business_id IN {tuple(business_id['business_id'].tolist())}
GROUP BY 
    b.business_id
""", conn).dropna()


engagement_df[['review_count', 'checkin_count', 'tip_count']].corr()


colors = ["#FFF1E5", "#F8862C", "#CB754B"]
custom_cmap = LinearSegmentedColormap.from_list("mycmap", colors)
sns.heatmap(
    engagement_df[['review_count', 'checkin_count', 'tip_count']].corr(),
    cmap=custom_cmap,
    annot=True,
    linewidths=0.5,
    linecolor='w'
)

# Is there a difference in the user engagement (reviews, tips, and check-ins) between high-rated and low-rated businesses?
engagement_df.groupby("category")[['review_count', 'tip_count', 'checkin_count']].mean()


# function to calculate the success score based on the avg rating and total review count
def calculate_success_metric(df):
    success_score = []
    for index, row in df.iterrows():
        score = row['avg_rating'] * np.log(row['review_count'] + 1)
        success_score.append(score)
    return success_score

# How do the success metrics (review_count or avg_rating) of restaurants vary across different states and cities?
city_df = pd.read_sql_query(f"""
select city, state, latitude, longitude, 
    AVG(stars) as avg_rating, 
    SUM(review_count) as review_count, 
    count(*) as restaurant_count
from business
WHERE business_id IN {tuple(business_id['business_id'].tolist())}
group by state, city
order by review_count desc
limit 10
""", conn)

city_df['success_score'] = calculate_success_metric(city_df)

# Create a base map
m = folium.Map(location=[city_df['latitude'].mean(), city_df['longitude'].mean()], zoom_start=4)

# Define a color scale
color_scale = folium.LinearColormap(
    colors=['green', 'yellow', '#E54F29'],
    vmin=city_df['success_score'].min(),
    vmax=city_df['success_score'].max()
)

# Add markers to the map
for index, row in city_df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color=color_scale(row['success_score']),
        fill=True,
        fill_color=color_scale(row['success_score']),
        fill_opacity=0.7,
        popup=f"Success Score: {row['success_score']}"
    ).add_to(m)

#Add color scale to the map 
m.add_child(color_scale)
high_rated_engagement = pd.read_sql_query(f"""
SELECT review.month_year, review.review_count, tip.tip_count FROM
(
    SELECT strftime('%m-%Y', date) AS month_year, COUNT(*) AS review_count
    FROM review
    WHERE business_id IN {tuple(business_id['business_id'])} AND stars >= 3.5
    GROUP BY month_year
    ORDER BY month_year
) as review
JOIN
(
    SELECT AVG(b.stars), strftime('%m-%Y', tip.date) AS month_year, COUNT(*) AS tip_count
    FROM tip
    JOIN business as b ON tip.business_id = b.business_id
    WHERE tip.business_id IN {tuple(business_id['business_id'])} AND b.stars >= 3.5
    GROUP BY month_year
    ORDER BY month_year
) as tip
ON review.month_year = tip.month_year
""", conn)

low_rated_engagement = pd.read_sql_query(f"""
SELECT review.month_year, review.review_count, tip.tip_count FROM
(
    SELECT strftime('%m-%Y', date) AS month_year, COUNT(*) AS review_count
    FROM review
    WHERE business_id IN {tuple(business_id['business_id'])} AND stars < 3.5
    GROUP BY month_year
    ORDER BY month_year
) as review
JOIN
(
    SELECT AVG(b.stars), strftime('%m-%Y', tip.date) AS month_year, COUNT(*) AS tip_count
    FROM tip
    JOIN business as b ON tip.business_id = b.business_id
    WHERE tip.business_id IN {tuple(business_id['business_id'])} AND b.stars < 3.5
    GROUP BY month_year
    ORDER BY month_year
) as tip
ON review.month_year = tip.month_year
""", conn)

high_rated_engagement
low_rated_engagement
time_rating = pd.read_sql_query(f"""
SELECT strftime('%m-%Y', date) AS month_year, AVG(stars) as avg_rating
FROM review
WHERE business_id IN {tuple(business_id['business_id'])}
GROUP BY month_year
ORDER BY month_year
""", conn)
time_rating['month_year'] = pd.to_datetime(time_rating['month_year'])
time_rating.sort_values('month_year', inplace=True)
time_rating = time_rating[time_rating['month_year'] > '2017']

high_rated_engagement['month_year'] = pd.to_datetime(high_rated_engagement['month_year'])
high_rated_engagement.sort_values('month_year', inplace=True)
high_rated_engagement = high_rated_engagement[high_rated_engagement['month_year'] > '2017']

low_rated_engagement['month_year'] = pd.to_datetime(low_rated_engagement['month_year'])
low_rated_engagement.sort_values('month_year', inplace=True)
low_rated_engagement = low_rated_engagement[low_rated_engagement['month_year'] > '2017']

high_rated_engagement['avg_rating'] = time_rating['avg_rating'].values
plt.figure(figsize=(15,8))

plt.subplot(3,1,1)
plt.title('Tip Engagement Over Time')
plt.plot(high_rated_engagement['month_year'], high_rated_engagement['tip_count'], label='High Rated', color='#E54F29')
plt.plot(low_rated_engagement['month_year'], low_rated_engagement['tip_count'], label='Low Rated', color='#F8862C')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.subplot(3,1,2)
plt.title('Review Engagement Over Time')
plt.plot(high_rated_engagement['month_year'], high_rated_engagement['review_count'], label='High Rated', color='#E54F29')
plt.plot(low_rated_engagement['month_year'], low_rated_engagement['review_count'], label='Low Rated', color='#F8862C')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.subplot(3,1,3)
plt.title('Avg Rating Over Time')
plt.plot(time_rating['month_year'], time_rating['avg_rating'], color='#E54F29')

plt.tight_layout()
plt.show()

tip_high_rated = high_rated_engagement[['month_year', 'tip_count']].set_index('month_year')
review_high_rated = high_rated_engagement[['month_year', 'review_count']].set_index('month_year')
rating_df = time_rating[['month_year', 'avg_rating']].set_index('month_year')
from statsmodels.tsa.seasonal import seasonal_decompose
multiplicative_decomposition = seasonal_decompose(tip_high_rated, model="multiplicative", period=12)

plt.rcParams.update({'figure.figsize': (16, 12)})
multiplicative_decomposition.plot()
plt.show()

from statsmodels.tsa.seasonal import seasonal_decompose
multiplicative_decomposition = seasonal_decompose(review_high_rated, model="multiplicative", period=12)

plt.rcParams.update({'figure.figsize': (16, 12)})
multiplicative_decomposition.plot()
plt.show()

from statsmodels.tsa.seasonal import seasonal_decompose
multiplicative_decomposition = seasonal_decompose(rating_df, model="multiplicative", period=12)

plt.rcParams.update({'figure.figsize': (16, 12)})
multiplicative_decomposition.plot()
plt.show()

# How does the sentiment of reviews and tips (useful, funny, cool) correlate with the success metrics of restaurants?
sentiment_df = pd.read_sql_query(f"""
SELECT b.business_id, 
       AVG(b.stars) as avg_rating, 
       SUM(b.review_count) as review_count,
       SUM(s.useful_count) as useful_count,
       SUM(s.funny_count) as funny_count,
       SUM(s.cool_count) as cool_count
FROM (
    SELECT business_id, 
           SUM(useful) as useful_count, 
           SUM(funny) as funny_count, 
           SUM(cool) as cool_count
    FROM review
    GROUP BY business_id
) as s
JOIN business as b ON b.business_id = s.business_id
WHERE b.business_id IN {tuple(business_id['business_id'])}
GROUP BY b.business_id
ORDER BY review_count
""", conn)

sentiment_df = remove_outliers(sentiment_df, 'review_count')
sentiment_df = remove_outliers(sentiment_df, 'useful_count')
sentiment_df = remove_outliers(sentiment_df, 'funny_count')
sentiment_df = remove_outliers(sentiment_df, 'cool_count')

sns.heatmap(sentiment_df.iloc[:,2:].corr(), cmap=custom_cmap, annot=True, linewidths=0.5, linecolor='black')
plt.show()

# Is there any difference in engagement of elite users and non elite users?
elite_df = pd.read_sql_query("""
SELECT 
    elite,
    COUNT(*) AS num_users,
    SUM(review_count) AS total_review_count
FROM (
    SELECT 
        CASE 
            WHEN elite = '' THEN 'Not Elite'
            ELSE 'Elite'
        END AS elite,
        u.review_count
    FROM user u
) AS user_elite
GROUP BY
elite;
""", conn)
elite_df
plt.figure(figsize=(10,6))

plt.subplot(1,2,1)
plt.title('User Distribution')
plt.pie(elite_df['num_users'], labels=elite_df['elite'], autopct='%.2f', startangle=180, colors=['#E54F29', '#F8862C'])

plt.subplot(1,2,2)
plt.title('Review Distribution')
plt.pie(elite_df['total_review_count'], labels=elite_df['elite'], autopct='%.2f', startangle=90, colors=['#E54F29', '#F8862C'])

plt.show()

# What are the busiest hours for restaurants?

review_engagement = pd.read_sql_query("""
SELECT 
    cast(strftime('%H', date) as integer) as hour,
    COUNT(*) AS review_count
FROM review
GROUP BY hour
""", conn)

tip_engagement = pd.read_sql_query("""
SELECT 
    cast(strftime('%H', date) as integer) as hour,
    COUNT(*) AS tip_count
FROM tip
GROUP BY hour
""", conn)

checkin = pd.read_sql_query("""SELECT date FROM checkin""", conn)
checkin_engagement = []
for i in checkin['date']:
    checkin_engagement.extend([datetime.strptime(j.strip(), "%Y-%m-%d %H:%M:%S").strftime("%H") for j in i.split(',')])

checkin_engagement = pd.DataFrame(checkin_engagement).astype('int').groupby(0)[0].count()

review_engagement

plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.title('Tip Engagement')
plt.bar(tip_engagement['hour'], tip_engagement['tip_count'], color='#E54F29')

plt.subplot(3, 1, 2)
plt.title('Review Engagement')
plt.bar(review_engagement['hour'], review_engagement['review_count'], color='#F8862C')

plt.subplot(3, 1, 3)
plt.title('Checkin Engagement')
plt.bar(checkin_engagement.index, checkin_engagement[0], color='#CB7548')

plt.tight_layout()
plt.show()

elite_df


