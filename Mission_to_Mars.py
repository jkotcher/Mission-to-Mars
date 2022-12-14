


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import pandas as pd


# This is the scraping python file but has been 
# left named as Mission_to_Mars.py


def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hemispheres(browser)
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres": hemisphere_image_urls,
      "last_modified": dt.datetime.now()
}

    browser.quit()

    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    html = browser.html
    news_soup = soup(html, 'html.parser')


    # Add try/except block
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as news_title
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_= 'article_teaser_body').get_text()
    except AttributeError:
        return None, None
    

    return news_title, news_p


def featured_image(browser):
# Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button

    full_image_elem = browser.find_by_tag('button')[1]

    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
    # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'


    return img_url

def mars_facts():
# Scraping the entire table and creating a new df to house the facts
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    


    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    df




    return df.to_html()


def hemispheres(browser):
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    hemisphere_image_urls = []

    imgs_links= browser.find_by_css("a.product-item h3")

    for x in range(len(imgs_links)):
        hemisphere={}

        # Find elements going to click link 
        browser.find_by_css("a.product-item h3")[x].click()

        # Find sample Image link
        sample_img= browser.find_link_by_text("Sample").first
        hemisphere['img_url']=sample_img['href']

        # Get hemisphere Title
        hemisphere['title']=browser.find_by_css("h2.title").text

        #Add Objects to hemisphere_img_urls list
        hemisphere_image_urls.append(hemisphere)

        # Go Back
        browser.back()
    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

    







