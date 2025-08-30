import praw as pw

class PESURedditScraper:
    def __init__(self, client_id, client_secret, user_agent):
        """Init Reddit API conn"""

        self.rd = pw.Reddit(
            client_id = client_id,
            client_secret = client_secret,
            user_agent = user_agent
        )

        print("Initialised PESU Reddit Scraper")

    def scrape(self, max_posts, listing = "hot"):
        """Scrape PESU subreddit and return list of text doc objs"""

        # Mapping each type of ranking/listing to its api func
        listing_to_api_call = {
            "hot": self.rd.subreddit("PESU").hot,
            "new": self.rd.subreddit("PESU").new,
            "top": self.rd.subreddit("PESU").top,
            "rising": self.rd.subreddit("PESU").rising,
            "controversial": self.rd.subreddit("PESU").controversial
        }

        api_call = listing_to_api_call.get(listing, None)

        assert api_call, "The listing supplied does not exist. Please choose between: hot, new, top, rising, controversial"

        docs = []

        print("Starting scraping process")

        for i, submission in enumerate(api_call(limit=max_posts)):

            print(f"Processing post {i + 1}")

            for comment_thread in submission.comments:
                content = (
                    f"TITLE: {submission.title}\n"
                    f"CONTENT: {submission.selftext.strip()}\n"
                    f"PARENT COMMENT: {getattr(comment_thread, 'body', '').strip()}"
                )
                for reply in getattr(comment_thread, "replies", []):
                    try:
                        content += f"\nREPLY: {reply.body.strip()}"
                    except Exception:
                        continue

                metadata = {
                    "id": str(submission.id),
                    "author": submission.author.name if submission.author else "[deleted]",
                    "url": submission.url,
                    "permalink": submission.permalink,
                    "score": int(submission.score),
                    "upvote_ratio": float(submission.upvote_ratio),
                    "created_utc": float(submission.created_utc),
                    "flair": submission.link_flair_text or "",
                    "nsfw": bool(submission.over_18)
                }

                docs.append({
                    "content": content,
                    "metadata": metadata
                })

            print(f"Finished process post {i + 1}")

        print("Processed all posts")

        return docs