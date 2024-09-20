## LinkedCraft - LinkedIn Post Reply Generator

This Python Flask application helps you get the latest posts from specified LinkedIn profiles and draft replies using AI. It's designed for users who want to stay engaged with their network and respond thoughtfully and efficiently to shared content.

### How it Works

1. **Provide LinkedIn Profile URLs:** Input the LinkedIn profile URLs of the connections whose latest posts you want to see.  You can enter them one per line in the provided text area.
2. **Get Latest Posts:** Click the "Get Latest Posts" button to trigger the scraper.
3. **View Posts and Draft Replies:** The application retrieves the most recent posts (up to 5) from each profile and displays them in a table. Each post includes the content, time posted, the original post URL, and a link to generate a draft reply using Perplexity AI.

### Features

- **Headless Scraper:** The scraper runs in the background, so you don't have to see a browser window.
- **Post Information:** Provides a concise view of each post, including the time it was shared.
- **Draft Replies with Perplexity AI:**  The Perplexity AI link allows you to get AI-generated replies that can help you craft thoughtful and engaging responses.

### Installation and Setup

1. **Clone the repository:** `git clone https://github.com/PlutoniaX/linkedcraft.git`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Create a .env file:** Copy the `.env.example` file and rename it to `.env`. Add your LinkedIn username and password as `LINKEDIN_UNAME` and `LINKEDIN_PW` respectively.
4. **Run the application:** `python run.py`

### Usage

1. **Access the application:** Open your web browser and visit `http://127.0.0.1:5000/`
2. **Enter Profile URLs:** Paste the LinkedIn profile URLs you want to check.
3. **Get Latest Posts:** Click the "Get Latest Posts" button.
4. **Review Posts:** Look at the table to see the latest posts from your connections.
5. **Draft Replies:**  Use the "Draft Reply" link to get AI-generated replies from Perplexity AI.

### Notes

- This application requires a valid LinkedIn account to scrape data.
-  The scraper is limited to retrieving a maximum of 5 posts from each profile.
-  The Perplexity AI link will open in a new tab, where you can use the AI to help you draft a reply.


### Input

- **LinkedIn Profile URLs:**  A list of URLs for LinkedIn profiles (one per line).  Each URL should look something like this:  `https://www.linkedin.com/in/yourusername`.

### Output

- **Table of Latest Posts:** A table containing the following information for each post:
    - Profile: The name of the LinkedIn profile
    - Content: The content of the post
    - Time Posted: The timestamp when the post was shared
    - Post URL: A link to the original post on LinkedIn
    - Draft Reply: A link to Perplexity AI that will help you generate a reply based on the post content.
