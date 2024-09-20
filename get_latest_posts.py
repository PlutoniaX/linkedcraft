# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Chrome options
chrome_options = webdriver.ChromeOptions()

# LinkedIn Credentials from environment variables
username = os.getenv("LINKEDIN_UNAME")  
password = os.getenv("LINKEDIN_PW")

# Set LinkedIn page URL for scraping
page = 'https://www.linkedin.com/in/john-ho-62166667/'

# Initialize WebDriver for Chrome
browser = webdriver.Chrome(options=chrome_options)
print("Browser Initialized")

# Open LinkedIn login page
browser.get('https://www.linkedin.com/login')
print("Opened LinkedIn Login Page")

# Enter login credentials and submit
elementID = browser.find_element(By.ID, "username")
elementID.send_keys(username)
elementID = browser.find_element(By.ID, "password")
elementID.send_keys(password)
elementID.submit()
print("Logged in with provided credentials")
# time.sleep(40)
print("Waiting for profile page")
time.sleep(5)

# Function to extract text with formatting from a BeautifulSoup element
def extract_text_with_formatting(element):
    text_parts = []
    for child in element.children:
        if child.name == 'span' or child.name is None:
            text_parts.append(child.text.strip())
        elif child.name == 'a' and 'app-aware-link' in child.get('class', []):
            text_parts.append(child.text.strip())
    return ''.join(text_parts).strip()

# Function to extract post URL
def extract_post_url(container):
    try:
        # Find the anchor tag with the post URL
        link_element = container.find_previous("div", class_="update-components-actor__container").find("a", class_="app-aware-link")
        if link_element:
            return "https://www.linkedin.com" + link_element['href']
        return "URL not found"
    except Exception as e:
        print(f"Error extracting URL: {e}")
        return "URL not found"

with open('profiles.txt', 'r') as file:
    profile_pages = file.readlines()

for page in profile_pages:
# Navigate to the posts page of the connection
    post_page = page + '/recent-activity'
    post_page = post_page.replace('//recent-activity','/recent-activity')
    browser.get(post_page)

    # Wait for the page to load posts
    time.sleep(5)

    # Scroll to ensure all posts are loaded
    for _ in range(0):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # Parse the page source with BeautifulSoup
    company_page = browser.page_source
    linkedin_soup = bs(company_page.encode("utf-8"), "html.parser")

    # Extract post containers from the HTML
    containers = linkedin_soup.find_all("div", class_="feed-shared-update-v2__description-wrapper")

    # Iterate through each post container and extract content
    posts_content = []
    post_times = []
    post_urls = []
    for container in containers:
        text_content_container = container.find("div", class_="update-components-text relative update-components-update-v2__commentary")
        
        if text_content_container:
            full_post_text = extract_text_with_formatting(text_content_container)
            posts_content.append(full_post_text)
            
            # Extract time posted
            try:
                time_span = container.find_previous("span", class_="update-components-actor__sub-description")
                if time_span:
                    time_text = time_span.find("span").text.strip()
                    post_times.append(time_text)
                else:
                    post_times.append("Time not found")
            except Exception as e:
                print(f"Error extracting time: {e}")
                post_times.append("Error")
            
            # Extract post URL
            post_url = extract_post_url(container)
            post_urls.append(post_url)

    # Convert the data into a DataFrame and export to CSV
    try:
        df = pd.DataFrame({
            'Post Content': posts_content, 
            'Time Posted': post_times,
            'Post URL': post_urls
        })
        print(f"Dataframe created with {len(df)} posts.")

        csv_file = f"{username}_posts.csv"
        
        # Check if the file already exists
        if os.path.exists(csv_file):
            # Append without writing the header
            df.to_csv(csv_file, mode='a', header=False, encoding='utf-8', index=False)
            print(f"Data appended to existing {csv_file}")
        else:
            # Create a new file with the header
            df.to_csv(csv_file, encoding='utf-8', index=False)
            print(f"New file {csv_file} created with data")
    except Exception as e:
        print(f"Error processing data: {e}")

# Close the browser once done
browser.quit()
