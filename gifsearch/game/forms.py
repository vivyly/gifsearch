from collections import Counter

from django.shortcuts import get_object_or_404

from django import forms
from .models import GifMetaGame
from gifsearch.scraper.models import GifObject

WORDLIMIT = 10

class GameMetaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        gifobj = kwargs.pop('gifobj', None)
        gifid = kwargs.pop('gifid', None)
        word_limit = kwargs.pop('wordlimit', WORDLIMIT)
        super(GameMetaForm, self).__init__(*args, **kwargs)
        self.word_limit = word_limit
        if isinstance(gifobj, GifObject):
            self.gif = gifobj
        elif isinstance(gifid, str):
            self.gif = get_object_or_404(GifObject, guid=gifid)
        #word_list = forms.CharField()
        for word_idx in range(0, self.word_limit):
            self.fields['word_%s' % word_idx] = forms.CharField()


    def clean(self):
        data = self.cleaned_data
        word_list = []
        for idx in range(0, self.word_limit):
            word_list.append(data.get('word_%s' %idx))
        data['word_list'] = word_list
        return data

    def save(self):
        data = self.cleaned_data
        word_list = data.get('word_list')
        gm = GifMetaGame()
        gm.gif = self.gif
        gm.data = dict.fromkeys(word_list, 0)
        gm.save()
        #increment or add to meta
        gif_meta = self.gif.meta
        game_counter = Counter(gm.data)
        gif_counter = Counter(gif_meta.data)
        counter_sum = game_counter + gif_counter
        gif_meta.data = counter_sum
        gif_meta.save()


