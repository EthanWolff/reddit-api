import praw
import urllib.request
import time

# Small program to backup saved posts or backup from a subreddit

class Reddit(object):
    def __init__(self, client_id, client_secret, username, password, user_agent):
        self.reddit = praw.Reddit(client_id = client_id, client_secret = client_secret, username = username, password = password, user_agent = user_agent)
        self.me = self.reddit.user.me()

    def save_submission(self, submission, file_types, folders):
        # Removes all non-alphanumeric characters from the title
        title = ''.join(i for i in submission.title if (ord(i) < 128 and i.isalnum()) or i == " ")
        print(title)
        url = submission.url
        # Checks if the file is an image
        if url[-3:] in file_types:
            # Takes a folders key is in the title, the file will be stored in that folder.
            for key in folders:
                if key in title.lower():
                    file_path = folders[key]
                    break
            urllib.request.urlretrieve(url, file_path + title + "." + url[-3:])

    def save_submissions(self, submissions, file_types, folders):
        for submission in submissions:
            self.save_submission(submission, file_types, folders)
            
    def download_saved(self, file_types = ["jpg", "png"], folders = { "": "" }):
        self.save_submissions(self.me.saved(limit=None), file_types, folders)

    def download_hot(self, subreddit_name, file_types = ["jpg", "png"], folders = { "": "" }, limit = None, min_score = 0):
        # Saves all the submissions with more upvotes than min_score
        self.save_submissions(filter(lambda submission: submission.ups > min_score, self.reddit.subreddit(subreddit).hot(limit=limit)), file_types, folders)

    def stream_hot(self, subreddit_name, ticks = 100, tick_limit = 20, file_types = ["jpg", "png"], folders = { "": "" }, min_score = 0):
        # Streams submissions from a subreddit and stores the submissions with more upvotes than min_score
        subreddit = self.reddit.subreddit(subreddit_name)
        seen_submissions = set()
        while ticks > 0:
            for submission in subreddit.hot(limit = tick_limit):
                # Checks if the post has not been seen before
                if (not (submission.id in seen_submissions)) and submission.score > min_score:
                    seen_submissions.add(submission.id)
                    save_submission(submission, file_types, folders)
            ticks -= 1
            sleep(60)
