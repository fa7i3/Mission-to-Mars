#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


### Let's define this function as "scrape_all" and then initiate the browser:
# def scrape_all():
    # Initiate headless driver for deployment
    # headless=True is declared as we initiate the browser, we are telling it to run in headless mode. All of the scraping will still be accomplished, but behind the scenes.


# In[3]:


# Set Up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


# assign the url and instruct the browser to visit:
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[5]:


# set up the HTML parser and convert to a soup object::
html = browser.html
news_soup = soup(html, 'html.parser')
# assigned slide_elem as the variable to look for the <div /> tag and its descendent ( parent element):
slide_elem = news_soup.select_one('div.list_text')


# In[6]:


# scrape the article’s title
# assign the title and summary text to variables:
slide_elem.find('div', class_='content_title')


# In[7]:


# get just the text, and the extra HTML stuff isn't necessary:
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# (With this new code, we’re searching within that element for the title. We’re also stripping the additional HTML attributes and tags with the use of .get_text().)


# In[8]:


# scrape the article summary instead of the title: 
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# # Scrape Mars Data: Featured Image:
# ### Featured Images

# In[9]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[10]:


# there are only three buttons;
# we want to click the full-size image button, 
# we can go ahead and use the HTML tag in our code:
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


# parse and scrape the full-size image URL:
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image:
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image


# In[13]:


# add the base URL to our code:
# This variable holds our f-string (img_url);
# This is an f-string, a type of string formatting used for print statements in Python (f'https://spaceimages-mars.com/');
# The curly brackets hold a variable that will be inserted into the f-string when it's executed({img_url_rel})
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[14]:


#(#creating a new DataFrame from the HTML table)
# read_html() specifically searches for and returns a list of tables found in the HTML. 
# By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. 
# Then, it turns the table into a DataFrame.
df = pd.read_html('https://galaxyfacts-mars.com')[0] 
# assign columns to the new DataFrame for additional clarity.
df.columns=['description', 'Mars', 'Earth']
# using the .set_index() function, we're turning the Description column into the DataFrame's index. 
# inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
df.set_index('description', inplace=True)
df


# In[15]:


# convert our DataFrame back into HTML-ready code using .to_html()
df.to_html()

# result is a slightly confusing-looking set of HTML code—it's a <table /> element with a lot of nested elements.


# In[16]:


# 10.4.1 Store the Data
# db.collectionName.insertOne({key:value}). Its components do the following:

# db refers to the active database, practicedb.
# collectionName is the name of the new collection we're creating (we'll customize it when we practice).
# .insertOne({ }) is how MongoDB knows we're inserting data into the collection.
# key:value is the format into which we're inserting our data; its construction is very similar to a Python dictionary.
# for example: db.zoo.insertOne({name: 'Cleo', species: 'jaguar', age: 12, hobbies: ['sleeping', 'eating', 'climbing']})
# type "show collections" we'll actually see a result: zoo.
# view what's inside a collection with the find() command.
# Documents can also be deleted or dropped. The syntax to do so follows: db.collectionName.deleteOne({}).
# empty the collection at once:  db.zoo.remove({})
# remove a collection all together, we would use db.zoo.drop().
# to remove the test database, we will use this line of code: db.dropDatabase().
# quit the Mongo shell by using keyboard commands: CTRL + C for Windows. 


# Visit the NASA Mars News Site

# In[17]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# Hemispheres

# In[18]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[19]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for hemis in range (4):
    # Browse through the article
    browser.links.find_by_partial_text('Hemisphere')[hemis].click()
    
    # Parse the HTML
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    # Scraping
    title = hemi_soup.find('h2', class_='title').text
    img_url = hemi_soup.find('li').a.get('href')
    
    hemispheres = {}
    hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
    hemispheres['title'] = title
    hemisphere_image_urls.append(hemispheres)
    
    browser.back()
    


# In[20]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[21]:


# 5. Quit the browser
browser.quit()


# In[ ]:




