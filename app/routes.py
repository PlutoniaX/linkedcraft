from flask import render_template, request, jsonify
from app import app
from app.linkedin_scraper import get_latest_posts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_posts', methods=['POST'])
def get_posts():
    print("Received request for posts")
    profile_urls = request.json['profileUrls']
    print(f"Profile URLs: {profile_urls}")
    posts = get_latest_posts(profile_urls)
    print(f"Retrieved {len(posts)} posts")
    return jsonify(posts)