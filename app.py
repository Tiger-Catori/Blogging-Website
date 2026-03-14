from flask import Flask, render_template
from datetime import datetime
import os
import markdown

app = Flask(__name__)

POST_FOLDER = "content"


# LOAD POSTS FROM MARKDOWN FILES
def load_posts():

    posts = []

    for filename in os.listdir(POST_FOLDER):

        if filename.endswith(".md"):

            filepath = os.path.join(POST_FOLDER, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            slug = filename.replace(".md", "")

            # Extract date from filename
            date = datetime.strptime(slug[:10], "%Y-%m-%d")

            # Create title from filename
            title = slug[11:].replace("-", " ").title()

            posts.append({
                "slug": slug,
                "title": title,
                "date": date,
                "summary": content[:200],   # ADD THIS LINE
                "content": markdown.markdown(content)
            })

    # Sort newest first
    posts.sort(key=lambda x: x["date"], reverse=True)

    return posts

# BASIC PAGES
@app.route('/')
def home():
    return render_template(
        'index.html',
        current_year=datetime.now().year
    )


@app.route('/about')
def about():
    return render_template(
        'about.html',
        current_year=datetime.now().year
    )


@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        current_year=datetime.now().year
    )


@app.route('/terms')
def terms():
    return render_template(
        'terms.html',
        current_year=datetime.now().year
    )


@app.route('/privacy')
def privacy():
    return render_template(
        'privacy.html',
        current_year=datetime.now().year
    )


# ARTICLES LIST PAGE
@app.route('/article')
def article():

    posts = load_posts()

    return render_template(
        "article.html",
        articles=posts,
        current_year=datetime.now().year
    )

# SINGLE ARTICLE PAGE
@app.route('/article/<slug>')
def single_article(slug):

    posts = load_posts()

    article = next((p for p in posts if p["slug"] == slug), None)

    if article is None:
        return render_template(
            "404.html",
            current_year=datetime.now().year
        ), 404

    return render_template(
        "post.html",
        article=article,
        current_year=datetime.now().year
    )



# ERROR HANDLER
@app.errorhandler(404)
def page_not_found(e):

    return render_template(
        "404.html",
        current_year=datetime.now().year
    ), 404


# RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)
