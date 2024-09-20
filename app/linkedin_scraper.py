# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import time
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Load environment variables
load_dotenv()

def get_latest_posts(profile_urls):
    print("Starting get_latest_posts function")
    # Initialize Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Run in headless mode

    # LinkedIn Credentials from environment variables
    username = os.getenv("LINKEDIN_UNAME")
    password = os.getenv("LINKEDIN_PW")

    # Initialize WebDriver for Chrome
    browser = webdriver.Chrome(options=chrome_options)

    # Login to LinkedIn
    browser.get('https://www.linkedin.com/login')
    browser.find_element(By.ID, "username").send_keys(username)
    browser.find_element(By.ID, "password").send_keys(password)
    browser.find_element(By.ID, "password").submit()
    time.sleep(5)

    all_posts = []

    for profile_url in profile_urls:
        print(f"Processing profile: {profile_url}")
        browser.get(profile_url.strip())
        time.sleep(5)

        # Extract profile name
        try:
            wait = WebDriverWait(browser, 10)
            name_element = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words")
                )
            )
            profile_name = name_element.text
            print(f"Name extracted: {profile_name}")
        except TimeoutException:
            print("Name element not found. Using URL as fallback.")
            profile_name = profile_url

        # Navigate to recent activity
        browser.get(profile_url.strip() + '/recent-activity')
        time.sleep(5)

        # Parse the page source with BeautifulSoup
        linkedin_soup = bs(browser.page_source, "html.parser")

        # Extract post containers from the HTML
        containers = linkedin_soup.find_all("div", class_="feed-shared-update-v2__description-wrapper")

        # Extract post content, time, and URL
        for container in containers[:5]:  # Limit to 5 most recent posts
            text_content = container.find("div", class_="update-components-text")
            time_span = container.find_previous("span", class_="update-components-actor__sub-description")
            post_url = extract_post_url(container)

            if text_content:
                content = text_content.text.strip()
                draft_reply_url = f"https://www.perplexity.ai/search?q=Come up with a short reply to this post: {content}"
                all_posts.append({
                    'profile': profile_name,
                    'content': content,
                    'time': time_span.find("span").text.strip() if time_span else "Time not found",
                    'url': post_url,
                    'draft_reply': draft_reply_url
                })

    print(f"Finished processing. Total posts: {len(all_posts)}")
    browser.quit()
    return all_posts

def extract_post_url(container):
    try:
        link_element = container.find_previous("div", class_="update-components-actor__container").find("a", class_="app-aware-link")
        if link_element:
            return link_element['href']
        return "URL not found"
    except Exception:
        return "URL not found"