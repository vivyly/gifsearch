import urllib, praw, datetime, re
from collection import Counter
from models import GifObject

SUBREDDIT="gif"
REDDIT_PAGINATE = 25
REDDIT_USER_AGENT = 'neat_gif_library'



class RedditParser():
    praw_obj = None
    subreddit_list = []

    def __init__(self, *args, **kwargs):
        subreddit = kwargs.get('subreddit', SUBREDDIT)
        self.praw_obj = praw.Reddit(user_agent=REDDIT_USER_AGENT)

    def read_subreddit(self, url):
        self.subreddit_list = self.praw_obj.get_subreddit(
                                'gif').get_hot(limit=REDDIT_PAGINATE)

    def save_gifs(self):
        for link in self.subreddit_list:
            try:
                gif = GifObject.objects.get(reddit_id=link.id)
            except GifObject.DoesNotExist:
                gif = GifObject()
                gif.reddit_id = link.id
                gif.src = link.url
                gif.created = datetime.datetime.now()
                gif.updated = datetime.datetime.now()
                gif.save()

    def parse_meta(link)
        comment_blocks = meta_collection(link)
        word_list = re.findall(r'\w+', comment_blocks.strip())
        word_counted = Counter(word_list)
        

    
    def read_children(parent_node, meta_block=''):
        replies = parent_node.replies
        if replies:
            for r in replies:
                if r.ups > r.downs:
                    meta_block += read_children(r)
            return meta_block
        else:
            return parent_node.body

    def meta_collection( link):
        meta_block = ''
        for c in link.comments:
            meta_block += read_children(c, '')
            meta_block += c.body
        return meta_block

