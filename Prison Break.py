#!/usr/bin/env python
# coding: utf-8

# # Prison Breaks

# Import helper function

# In[15]:


from helper import*


# Obtain the dataset from the source URL

# In[35]:


url ='https://en.wikipedia.org/wiki/List_of_helicopter_prison_escapes'
data=data_from_url(url)


# In[42]:


print(url)


# Iterate through the dataset 

# In[36]:


for row in data[:3]:
    print(row)


# Initialize a variable called a index and assign it to zero.
# Iterate through the url and assign it to data variable. 
# Increment index by one. 

# In[37]:


index = 0
for row in data:
    data[index] = row[:-1]
    index += 1


# Print the resulting dataset

# In[38]:


print(data[:3])


# Modify the date column to only include the year information. 
# To achieve this,utilize the helper function fetch_year().

# In[40]:


for row in data:
    date=fetch_year(row[0])
    row[0]=date


# Print the result

# In[41]:


print(data[:3]) 


# Initialize two new varialbles min_year and max_year.
# Create a list with elements in the format[,0]

# In[43]:


min_year = min(data, key=lambda x: x[0])[0]
max_year = max(data, key=lambda x: x[0])[0]


# In[44]:


years = []
for year in range(min_year, max_year + 1):
    years.append(year)


# Print the year in which minimum attempts were taken and the year in which maximum attempts were taken.

# In[45]:


print(min_year)


# In[46]:


print(max_year)


# In[47]:


attempts_per_year = []
for year in years:
    attempts_per_year.append([year, 0])


# And finally increment the second entry (the one on index 1 which starts out as being 0) by 1 each time a year appears in the data.

# In[48]:


for row in data:
    for year_attempt in attempts_per_year:
        year = year_attempt[0]
        if row[0] == year:
            year_attempt[1] += 1
            
print(attempts_per_year)


# Use matplotlib to print a bar graph to visualize attempts per year 

# In[59]:


get_ipython().run_line_magic('matplotlib', 'inline')
barplot(attempts_per_year)


# In[57]:


countries_frequency = df["Country"].value_counts()


# Visualize the number of prison breaks frequency by each country

# In[58]:


print_pretty_table(countries_frequency)


# # The country with the most helicopter prison escape attempts is France.

# In[ ]:




