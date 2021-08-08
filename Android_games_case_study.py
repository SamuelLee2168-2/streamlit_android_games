import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.subplots as ps
from PIL import Image








games = pd.read_csv("android-games.csv")

st.markdown("In this article, we will be looking at a dataset of the top rated games in the google play store, asking questions about them to find some interesting observations, and analyzing the data.")

st.markdown("Let's first look at which games have the highest rating in the dataset, and look at their attributes to see if there are any patterns.")
top_rated_games = games.sort_values('average rating',ascending=False).head(10).reset_index()[['title', 'average rating','total ratings', 'installs', 
       'growth (30 days)', 'growth (60 days)', 'price', 'category',
       '5 star ratings', '4 star ratings', '3 star ratings', '2 star ratings',
       '1 star ratings', 'paid']]
st.dataframe(top_rated_games)

st.markdown("All of the top rated games are free, and the games have a pretty low amount of installs compared to games that have billions of installs. ")
st.markdown("If we look at the amount of 1 star ratings, we can see that some games only have a few hundred 1 star ratings. The amount of 1 star ratings are too small and could easily bounce up and down.")

st.image("coin_flip.png",width=400,output_format='png')

st.markdown("For example, if we flip a coin one time, there is a 50% chance for coin to land on it's head, and 50% chance for the coin to land on it's tail. ")
st.markdown("If we flip a coin twice, there is a 25% chance that both times the coin lands head, and 25% chance that both times the coin lands tail. ")
st.markdown("If we flip a coin 100 times, the chance of the coin landing 100 heads in a row is extremely low.")
st.markdown("So the more times we flip the coin, the less extreme the result is.")
st.markdown("In the case of the rating of the games, the higher amount of ratings, the less extreme the ratings can be.")
st.markdown("This is likely why the ratings are really high for these 10 games, because the amount of ratings is too low, and the rating can easily be very high or very low.")


def string_to_float_installs(string):
    if 'k' in string:
        return float(string.replace(' k',''))*1000
    elif 'M' in string:
        return float(string.replace(' M',''))*1000000 
games['float installs'] = games['installs'].apply(string_to_float_installs)

st.markdown("So, let's look at the games that have the highest amount of installs then.")

games.sort_values('float installs',ascending=False).head(10).reset_index()[['title', 'average rating','total ratings', 'installs', 
       'growth (30 days)', 'growth (60 days)', 'price', 'category',
       '5 star ratings', '4 star ratings', '3 star ratings', '2 star ratings',
       '1 star ratings', 'paid']]

st.markdown("These games look much more familiar.")
st.markdown("All of these games are free.")
st.markdown("These games have low ratings compared to the games with the highest ratings.")
st.markdown("The highest downloaded games don't seem to have any common categories. To find the most successful categories, let's plot the average amount of installs for each category!")

attribute = 'float installs'
category_installs = games.sort_values(attribute,ascending=False).groupby('category').mean().reset_index().sort_values(attribute,ascending=False)
category_total_installs_chart = px.bar(category_installs,x='category',y=attribute)
st.plotly_chart(category_total_installs_chart)

st.markdown("GAME ARCADE, GAME CASUAL, and GAME ACTION have the most installs, while GAME TRIVIA and GAME CASINO have the least installs.")

st.markdown("Now let's plot the average amount of percent growth in 30 days for each category to see which categories grow the fastest.")
attribute2 = 'growth (30 days)'
category_growth = games.sort_values(attribute2,ascending=False).groupby('category').mean().reset_index().sort_values(attribute2,ascending=False)
category_growth_chart = px.bar(category_growth,x='category',y=attribute2) 
st.plotly_chart(category_growth_chart)

st.markdown("GAME ACTION and GAME WORD have extremely rapid growth, while the other categories barely grow for the first 30 days.")
st.markdown("There is a pretty extreme difference between the growth of the categories. Let's plot a sunburst plot to see the specific games.")

category_browth_sunburst = px.sunburst(games[['category','title','growth (30 days)']],path=['category','title'],values='growth (30 days)')
sunburst_checkbox = st.checkbox("Click this checkbox to load the Sunburst plot.", value=False)
if sunburst_checkbox:
    st.plotly_chart(category_browth_sunburst)

st.markdown("The first ring of the plot make up the growth of the categories. The larger area that category takes up, the higher the growth of that category. We can see that GAME ACTION and GAME WORD have much more growth compared to the other categories.")
st.markdown("The second ring of the plot are the specific games of each categories. The area the games take up also depend on the growth. ")
st.markdown("You can click on one of the categories to only see the games in that category. If we click into GAME WORD and GAME ACTION, we can see that the games 'Fill-The-Words - word search puzzle', and 'Garena AOV: Link Start' take up almost all of the growth of the category. So there was just 2 games that have high growth in the categories. This means that if you make an action game or word game, your game won't necessarily grow faster than other games.")
st.markdown("This is often a problem when you take the average of something. One value will pull the average up by a bunch, which will give us a wrong idea of the overall picture.")
st.markdown("To solve this problem, we can plot the median of the growth of each category instead of the average.")

attribute3 = 'growth (30 days)'
category_growth = games.sort_values(attribute2,ascending=False).groupby('category').median().reset_index().sort_values(attribute2,ascending=False)
category_median_growth = px.bar(category_growth,x='category',y=attribute2)
st.plotly_chart(category_median_growth)

st.markdown("Now we can see that education games have the highest growth, and the difference between categories are less extreme than before.")

st.markdown("Let's see which types of stars are most commonly rated")
star_chart = px.bar(games[['1 star ratings','2 star ratings','3 star ratings','4 star ratings','5 star ratings',]].sum().reset_index(),x='index',y=0)
st.plotly_chart(star_chart)

st.markdown("5 stars, 4 stars and 1 stars are rated the most, while 2 stars and 3 stars aren't rated too often. This is because only if you love a game very much or hate a game very much you would have an incentive to the rate a game.")

st.markdown("Let's look at the percentage of people who rate a game they installed.")
rated_percentage = sum(games['total ratings'])/sum(games['float installs'])*100
rated_dict ={'Rated':rated_percentage,'Not rated':100-rated_percentage}
rated = pd.DataFrame(list(rated_dict.items()),columns=['Type','Percentage'])
rated_chart = px.pie(rated,values='Percentage',names='Type')
rated_chart
st.markdown("Only 4% of people who install a game rate the game, so people will need to have a strong incentive to rate a game!")

st.markdown("Let's plot the amount of 5 star ratings for each game compared to the amount of 1 star ratings for each game.")
star_correlation_chart = px.scatter(games,x='5 star ratings',y='1 star ratings')
st.plotly_chart(star_correlation_chart)

st.markdown("It seems like the more 1 star ratings there are, the more 5 star ratings. Does this mean that people rating a game 1 star will cause more people to rate the game 5 star?")
st.markdown("No, this graph only proves positive correlation between the amount of 1 star ratings and 5 star ratings, but not causality. This is simply because the more installs a game has, the 1 star AND 5 star ratings a game has.")

st.markdown("It seems like all of the top games in this dataset are free, let's look at the percentage of games that need to be bought.")
paid_percentage = sum(games['paid'])/len(games['paid'])*100
paid_dict ={'Paid':paid_percentage,'Free':100-paid_percentage}
paid = pd.DataFrame(list(paid_dict.items()),columns=['Type','Percentage'])
paid_chart = px.pie(paid,values='Percentage',names='Type')
st.plotly_chart(paid_chart)

st.markdown("Wow! Only 0.405% of the top google play store games need to be bought. However, note that the 'free' games are only free for downloading the game. The game can make money buy selling in game items to players. This makes sense that most games are free to download but charge for in game items, since this way more players will download the game if it is free.")
