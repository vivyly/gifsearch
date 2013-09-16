from django.conf.urls import patterns

urlpatterns = patterns('gifsearch.game.views',
   (r'/(?P<gifid>(\w+{6}))/?$', 'gifgame'),
   (r'/?$', 'gifgamelist'),
)
