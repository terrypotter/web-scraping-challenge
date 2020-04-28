from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    # return Browser("chrome", **executable_path, headless=False)
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    scrape_data={}

    # Scrape NASA Mars News

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    # Delay
    time.sleep(1)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_news = soup.find('li', class_='slide')
    news_title = mars_news.find('div', class_="content_title").text
    news_p = mars_news.find('div', class_="article_teaser_body").text
    # news_p
    # print(news_title)
    # print('-' * 25)
    # print(news_p)
    scrape_data['Article Title']=news_title
    scrape_data['Article Desc']=news_p

    # Scrape JPL Mars Space Images

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Delay
    time.sleep(1)

    # Click on "Full Image"
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Click on "More Info"
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')

    jpl_image = jpl_soup.select_one('figure.lede a img').get('src')

    # Append previous result to main url
    featured_image_url = f'https://www.jpl.nasa.gov{jpl_image}'

    scrape_data['JPL Image']=featured_image_url

    # Scrape Mars Weather

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Delay
    time.sleep(1)

    # Request information from Mars' twitter page
    twitter_response = requests.get('https://twitter.com/marswxreport?lang=en')

    # Create BeautifulSoup object; parse with 'html.parser'
    twitter_soup = BeautifulSoup(twitter_response.text, "html.parser")

    # Parent container for the top weather tweet
    tweet_containers = twitter_soup.find_all("div", class_='js-tweet-text-container')

    # Parse and print most recent weather tweet
    mars_weather = tweet_containers[0].text 

    scrape_data['Mars Weather']=mars_weather

    # Scrape Mars Facts

    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # Delay
    time.sleep(1)

    # Read the tables from the webpage
    facts_tables = pd.read_html(url)
    

    # Select first table
    facts_table_df = facts_tables[0]

    # Rename dataframe columns
    facts_table_df.columns = ["Mars Facts", "Values"]

    # Reset the index
    facts_table_df.set_index("Mars Facts", inplace=True)
    
    # Convert the dataframe to html table and replace line breaks with blanks

    mars_facts = (facts_table_df.to_html()).replace('\n', '')

    scrape_data['Mars Facts']=mars_facts

    # Scrape Mars Hemisperes

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Delay
    time.sleep(2)

    # Create empty list for url's
    hemisphere_img_urls = []

    # Finding elements in the page, by selector type: css
    links = browser.find_by_css('a.product-item h3')

    # Loop through number of links to store titles and url's
    for i in range(len(links)):
    
        # Create empty dictionary for titles and url's
        hemisphere = {}
    
        # Finding elements in the page, by selector type: css
        browser.find_by_css('a.product-item h3')[i].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere['img_url']  = sample_elem['href']
        hemisphere_img_urls.append(hemisphere)
    
        # loads the previous URL in the history list (back button)
        browser.back() 
    
    scrape_data['Hemi One Title'] = hemisphere_img_urls[0]['title']
    scrape_data['Hemi One Image'] = hemisphere_img_urls[0]['img_url']

    scrape_data['Hemi Two Title'] = hemisphere_img_urls[1]['title']
    scrape_data['Hemi Two Image'] = hemisphere_img_urls[1]['img_url']

    scrape_data['Hemi Three Title'] = hemisphere_img_urls[2]['title']
    scrape_data['Hemi Three Image'] = hemisphere_img_urls[2]['img_url']

    scrape_data['Hemi Four Title'] = hemisphere_img_urls[3]['title']
    scrape_data['Hemi Four Image'] = hemisphere_img_urls[3]['img_url']

    # # news_p
    # print(hemisphere_img_urls[0]['title'])
    # print('-' * 25)
    # print(hemisphere_img_urls[0]['title'])

    # Close the browser after scraping
    browser.quit()

    return scrape_data


if __name__ == '__main__':
    print(scrape())

    