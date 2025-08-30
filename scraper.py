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

    def scrape(self, max_posts_per_keyword, keywords, sorting_type = "relevance"):
        """Scrape PESU subreddit and return list of text doc objs"""

        assert sorting_type in ["relevance", "top", "new", "hot", "comments"], "Sorting type must be chosen from: relevance, top, new, hot, comments"

        docs = []
        submissions = []
        
        print("Retrieving posts from subreddit.")

        for keyword in keywords:
            new_submissions = self.rd.subreddit("PESU").search(keyword, sort=sorting_type, limit = max_posts_per_keyword)
            submissions.extend(new_submissions)

            print(f"Total posts retrieved: {len(submissions)}")

        print("Finished retrieving posts from subreddit.")
        print("Starting to process posts.")

        for i, submission in enumerate(submissions):
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
                    "nsfw": str(submission.over_18)
                }

                docs.append({
                    "content": content,
                    "metadata": metadata
                })

            print(f"Finished process post {i + 1}")

        print("Processed all posts")

        return docs