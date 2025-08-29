import praw as pw

class PESURedditScraper:
    def __init__(self, client_id, client_secret, user_agent):
        """Init Reddit API conn"""

        self.rd = pw.Reddit(
            client_id = client_id,
            client_secret = client_secret,
            user_agent = user_agent
        )

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

        for submission in api_call(limit=max_posts):
            new_docs = []

            for comment_thread in submission.comments:
                doc = {
                    "metadata": "",
                    "content": ""
                }

                doc["metadata"] += "ID: {submission.id}"
                doc["metadata"] += f"\nAUTHOR: {submission.author.name if submission.author else '[deleted]'}"
                doc["metadata"] += f"\nURL: {submission.url}"
                doc["metadata"] += f"\nPERMALINK: {submission.permalink}"
                doc["metadata"] += f"\nSCORE: {submission.score}"
                doc["metadata"] += f"\nUPVOTE RATIO: {submission.upvote_ratio}"
                doc["metadata"] += f"\nCREATED_UTC_TIME: {submission.created_utc}"
                doc["metadata"] += f"\nFLAIR: {submission.link_flair_text}"
                doc["metadata"] += f"\nNSFW: {submission.over_18}"
                doc["content"] += f"\nTITLE: {submission.title}"
                doc["content"] += f"\nCONTENT: {submission.selftext.strip()}"
                doc["content"] += f"\nPARENT COMMENT: {comment_thread.body.strip()}"
                
                for reply in comment_thread.replies.list(): # replies.list() returns a flattened list of replies
                    doc["content"] += f"\nREPLY: {reply.body.strip()}"

                docs.append(doc)

            docs.extend(new_docs)

        return docs