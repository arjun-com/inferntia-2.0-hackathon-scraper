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

        for submission in self.rd.subreddit("PESU").hot(limit=max_posts):
            new_docs = []

            for comment_thread in submission.comments:
                doc = ""

                doc += f"ID: {submission.id}"
                doc += f"\nAUTHOR: {submission.author.name if submission.author else '[deleted]'}"
                doc += f"\nURL: {submission.url}"
                doc += f"\nPERMALINK: {submission.permalink}"
                doc += f"\nSCORE: {submission.score}"
                doc += f"\nUPVOTE RATIO: {submission.upvote_ratio}"
                doc += f"\nCREATED_UTC_TIME: {submission.created_utc}"
                doc += f"\nFLAIR: {submission.link_flair_text}"
                doc += f"\nNSFW: {submission.over_18}"
                doc += f"\nTITLE: {submission.title}"
                doc += f"\nCONTENT: {submission.selftext.strip()}"
                doc += f"\nPARENT COMMENT: {comment_thread.body.strip()}"
                
                for reply in comment_thread.replies.list():
                    doc += f"\nREPLY: {reply.body.strip()}"

                docs.append(doc)

            docs.extend(new_docs)

        return docs