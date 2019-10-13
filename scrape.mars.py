#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars

# # Step 1 - Scraping 

# In[6]:


# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time


# In[7]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[8]:


nasa_scraped_data = {}


# ## NASA Mars News

# In[9]:


news_url = 'https://mars.nasa.gov/news/'
browser.visit(news_url)


# In[10]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')

latest_mars_news = soup.find('li', class_='slide')

title = latest_mars_news.find('div', class_='content_title').text.strip()

nasa_scraped_data['news_title'] = title
   
print(title)
print("-----------------------------------------------------")
    
paragraph = latest_mars_news.find('div', class_='article_teaser_body').text.strip()

nasa_scraped_data['news_p'] = paragraph
   
print(paragraph)
   


# # JPL Mars Space Images - Featured Image

# In[11]:


featured_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(featured_url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

image = soup.find('article')['style'].strip("background-image: url('").strip("');")
print(image)

featured_image_url = "https://www.jpl.nasa.gov" + image

nasa_scraped_data['featured_image_url'] = featured_image_url

featured_image_url


# # Mars Weather

# In[12]:


weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weather_url)


# In[13]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')

latest_mars_weather = soup.find('div', class_='js-tweet-text-container')

mars_weather = latest_mars_weather.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').get_text()

mars_weather_a = latest_mars_weather.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').find('a').get_text()

mars_weather = mars_weather.replace(mars_weather_a, "")

nasa_scraped_data['mars_weather'] = mars_weather
   
mars_weather


# # Mars Facts

# In[14]:


facts_url = 'https://space-facts.com/mars/'
facts_df = pd.read_html(facts_url)[1]
facts_df


# In[15]:


facts_df


# In[16]:


facts_df.columns=["description", "value"]


# In[17]:


facts_df.set_index("description", inplace=True)


# In[18]:


facts_df


# In[19]:


html_facts_table = facts_df.to_html()
html_facts_table


# In[20]:


html_facts_table.replace('\n', '').replace('border="1" class="dataframe"', 'class="table table-striped"')


# In[21]:


nasa_scraped_data['html_facts_table'] = html_facts_table


# In[22]:


facts_df.to_html('mars_planet_profile.html')


# # Mars Hemispheres

# In[23]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
hemisphere_image_urls = []
# First, get a list of all of the hemispheres
links = browser.find_by_css("a.product-item h3")
# Next, loop through those links, click the link, find the sample anchor, return the href
for i in range(len(links)):
    hemisphere = {}
    
    # We have to find the elements on each loop to avoid a stale element exception
    browser.find_by_css("a.product-item h3")[i].click()
    
    # Get Hemisphere title
    hemisphere['title'] = browser.find_by_css("h2.title").text
    
    # Next, we find the Sample image anchor tag and extract the href
    sample_elem = browser.find_link_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']
    
    # Append hemisphere object to list
    hemisphere_image_urls.append(hemisphere)
    
    # Finally, we navigate backwards
    browser.back()


# In[24]:


nasa_scraped_data['hemisphere_image_urls'] = hemisphere_image_urls


# In[25]:


hemisphere_image_urls


# In[26]:


nasa_scraped_data

