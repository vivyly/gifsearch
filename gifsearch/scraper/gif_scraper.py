import praw, nltk
from .models import GifObject, GifMeta

SUBREDDIT = "gif"
REDDIT_PAGINATE = 25
REDDIT_USER_AGENT = 'neat_gif_library'
NLTK_REDDIT_FLAGS = ['NN', 'NNS'] #NNP?

class RedditParser(object):

    def __init__(self, **kwargs):
        self.subreddit_list = []
        self.subreddit = kwargs.get('subreddit', SUBREDDIT)
        self.praw_obj = praw.Reddit(user_agent=REDDIT_USER_AGENT)

    def get_subreddit_list(self):
        self.subreddit_list = list(self.praw_obj.get_subreddit(
                                self.subreddit).get_hot(limit=REDDIT_PAGINATE))
        return self.subreddit_list

    def save_gifs(self):
        subreddit_links = self.get_subreddit_list()
        for link in subreddit_links:
            try:
                gif = GifObject.objects.get(src_id=link.id)
            except GifObject.DoesNotExist:
                gmeta = self.create_meta(self.parse_comments(link))
                gif = GifObject()
                gif.src_id = link.id
                gif.src = link.url
                gif.title = link.title
                gif.meta = gmeta
                gif.save()

    def create_meta(self, meta_data):
        gmeta = GifMeta()
        gmeta.data = dict.fromkeys(meta_data, 0)
        gmeta.save()
        return gmeta

    def nltk_tag_nouns(self, comments):
        tokens = nltk.word_tokenize(comments)
        tagged = nltk.pos_tag(tokens)
        word_data = [x for x, y in tagged if y in NLTK_REDDIT_FLAGS]
        return word_data

    def parse_comments(self, link):
        #depth first for now. TODO: needs switch for breadth first)
        comment_blocks = self.read_children(link)
        word_data = self.nltk_tag_nouns(comment_blocks)
        return word_data

    #depth first search
    def read_children(self, parent_node):
        meta_block = ''
        replies = getattr(parent_node, 'comments', None)
        if replies:
            for child_node in replies:
                meta_block += self.read_children_helper(child_node)
        return meta_block

    def read_children_helper(self, parent_node):
        meta_block = ''
        replies = getattr(parent_node, 'replies', None)
        if replies:
            for child_node in replies:
                meta_block += self.read_children_helper(child_node)
            return meta_block + ' '
        return parent_node.body + ' '


    #trying breath-first traversal option, to collect top level comments first
    def read_children_breadth(self, parent_node):
        replies = getattr(parent_node, 'comments', None)
        return self.read_children_breadth_helper(replies)

    #make sure this is not 30.000 deep or else python assumes it's trapped in a loop
    def read_children_breadth_helper(self, node_list):
        meta_block = ''
        children_list = []
        for node in node_list:
            node_children = getattr(node, 'replies', None)
            if node_children:
                children_list.append(node_children)
            meta_block += (node.body + ' ')
        if node_children:
            meta_block += self.read_children_breadth_helper(children_list)
        return meta_block + ' '
