from django.conf.urls import patterns

urlpatterns = patterns('gifsearch.game.views',
   (r'/$', 'gifgamelist'),
   (r'/(?P<gifid>[\w]+)$', 'gifgame'),
)
