# web-scraping-challenge
Web Scraping Homework by Terry Potter

Overview
1.	Created a Jupyter Notebook “mission_to_mars.ipynb” to use Beautiful Soup, Splinter, and pandas to scrape the web.  The following text, images and tables were collected:
a.	Visit the NASA Mars News site and collect the latest News Title and Paragraph Text
b.	Visit the JPL Mars Space site and collect the featured image in full size
c.	Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page.
d.	Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet
e.	Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.

2.	Created “scrape_mars.py” by copying code from “mission_to_mars.ipynb”.  Next created a function called scrape to execute the scraping code and return one Python dictionary called “scrape_data” containing all of the scraped data.

3.	In “app.py” created a root route to query the Mongo database and pass the mars data into an HTML template to display the data.


4.	Created a template HTML file called index.html to take the mars data dictionary and display all of the data in the appropriate HTML elements


