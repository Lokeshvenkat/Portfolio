#!/usr/bin/env python
# coding: utf-8

# # Predicting Bike Rentals

# Import Pandas library

# In[1]:


import pandas


# Read bike_rental_hour.csv into the dataframe bike_rentals.

# In[2]:


bike_rentals = pandas.read_csv("bike_rental_hour.csv")
bike_rentals.head()


# Here are the descriptions for the relevant columns:
# 
# instant - A unique sequential ID number for each row
# dteday - The date of the rentals
# season - The season in which the rentals occurred
# yr - The year the rentals occurred
# mnth - The month the rentals occurred
# hr - The hour the rentals occurred
# holiday - Whether or not the day was a holiday
# weekday - The day of the week (as a number, 0 to 7)
# workingday - Whether or not the day was a working day
# weathersit - The weather (as a categorical variable)
# temp - The temperature, on a 0-1 scale
# atemp - The adjusted temperature
# hum - The humidity, on a 0-1 scale
# windspeed - The wind speed, on a 0-1 scale
# casual - The number of casual riders (people who hadn't previously signed up with the bike sharing program)
# registered - The number of registered riders (people who had already signed up)
# cnt - The total number of bike rentals (casual + registered)

# Print out the first few rows of bike_rentals

# Make a histogram of the cnt column of bike_rentals, and take a look at the distribution of total rentals.

# In[3]:


get_ipython().magic('matplotlib inline')

import matplotlib.pyplot as plt

plt.hist(bike_rentals["cnt"])


# Use the corr method on the bike_rentals dataframe to explore how each column is correlated with cnt

# In[4]:


bike_rentals.corr()["cnt"]


# Write a function called assign_label that takes in a numeric value for an hour, and returns:
# 1 if the hour is from 6 to 12
# 2 if the hour is from 12 to 18
# 3 if the hour is from 18 to 24
# 4 if the hour is from 0 to 6

# Assign the result to the time_label column of bike_rentals

# In[5]:


def assign_label(hour):
    if hour >=0 and hour < 6:
        return 4
    elif hour >=6 and hour < 12:
        return 1
    elif hour >= 12 and hour < 18:
        return 2
    elif hour >= 18 and hour <=24:
        return 3

bike_rentals["time_label"] = bike_rentals["hr"].apply(assign_label)


# # Error Metric

# Select 80% of the rows in bike_rentals to be part of the training set using the sample method on bike_rentals. Assign the result to train.

# In[6]:


train = bike_rentals.sample(frac=.8)


# Select the rows that are in bike_rentals but not in train to be in the testing set. Assign the result to test.

# In[7]:


test = bike_rentals.loc[~bike_rentals.index.isin(train.index)]


# This line generates a Boolean series that's False when a row in bike_rentals isn't found in train: bike_rentals.index.isin(train.index)
# This line selects any rows in bike_rentals that aren't found in train to be in the testing set: bike_rentals.loc[~bike_rentals.index.isin(train.index)]

# In[9]:


from sklearn.linear_model import LinearRegression

predictors = list(train.columns)
predictors.remove("cnt")
predictors.remove("casual")
predictors.remove("registered")
predictors.remove("dteday")

reg = LinearRegression()

reg.fit(train[predictors], train["cnt"])


# In[10]:


import numpy
predictions = reg.predict(test[predictors])

numpy.mean((predictions - test["cnt"]) ** 2)


# # Error

# The error is very high, which may be due to the fact that the data has a few extremely high rental counts but otherwise mostly low counts. Larger errors are penalized more with MSE, which leads to a higher total error.

# In[11]:


from sklearn.tree import DecisionTreeRegressor

reg = DecisionTreeRegressor(min_samples_leaf=5)

reg.fit(train[predictors], train["cnt"])


# Use the DecisionTreeRegressor class to fit a decision tree algorithm to the train data.
# 

# Make predictions using the DecisionTreeRegressor class on test.
# Calculate the error between the predictions and the actual values.
# Experiment with various parameters of the DecisionTreeRegressor class, including min_samples_leaf, to see if it changes the error.

# In[12]:


predictions = reg.predict(test[predictors])

numpy.mean((predictions - test["cnt"]) ** 2)


# # Decision Tree Error

# By taking the nonlinear predictors into account, the decision tree regressor appears to have much higher accuracy than linear regression.

# In[13]:


from sklearn.ensemble import RandomForestRegressor

reg = RandomForestRegressor(min_samples_leaf=5)
reg.fit(train[predictors], train["cnt"])


# In[14]:


predictions = reg.predict(test[predictors])

numpy.mean((predictions - test["cnt"]) ** 2)


# # Random Forest Error

# By removing some of the sources of overfitting, the random forest accuracy is improved over the decision tree accuracy.
