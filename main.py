import os
from dotenv import load_dotenv
import praw as pw

load_dotenv()

reddit = pw.Reddit(
    client_id = os.getenv("client_id"),
    client_secret = os.getenv("client_secret"),
    user_agent = os.getenv("user_agent")
)

# Subreddit to scrape
subreddit_name = "PESU"
limit_posts = 5 # number of posts to fetch

# Output file
output_file = "subreddit_data.txt"

def scrape_subreddit(subreddit_name, limit_posts=100):
    subreddit = reddit.subreddit(subreddit_name)

    with open(output_file, "w", encoding="utf-8") as f:
        for submission in subreddit.hot(limit=limit_posts):
            # Write post title
            f.write(f"TITLE:\n{submission.title.strip()}\n\n")
            
            # Write post body
            message = submission.selftext.strip()
            if message:
                f.write(f"MESSAGE:\n{message}\n\n")
            else:
                f.write("MESSAGE:\n[No text content]\n\n")
            
            # Fetch comments
            f.write("COMMENTS:\n")
            submission.comments.replace_more(limit=0)  # flatten comments
            for top_level_comment in submission.comments:
                f.write(f"- {top_level_comment.body.strip()}\n")
            
            f.write("\n" + "="*80 + "\n\n")

    print(f"Finished scraping. Data saved to {output_file}")

scrape_subreddit(subreddit_name, limit_posts)