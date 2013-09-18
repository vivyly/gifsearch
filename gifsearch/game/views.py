import random

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from gifsearch.game.forms import GameMetaForm
from gifsearch.scraper.models import GifObject

GIFLIMIT = 25

def gifgamelist(request):
    gifobj = GifObject.objects.all()
    paginator = Paginator(gifobj, GIFLIMIT) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        gifs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        gifs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        gifs = paginator.page(paginator.num_pages)
    return render_to_response("gifgamelist.html",
            dict(gifs=gifs, page=page),
            context_instance=RequestContext(request))



def gifgame(request, gifid):
    gifobj = get_object_or_404(GifObject, src_id = gifid)
    gifobjlist = list(GifObject.objects.all()[:GIFLIMIT]) #need to filter by user
    random_gif = random.sample(gifobjlist, 1)
    if random_gif:
        next_url = '/game/%s' % random_gif[0].src_id
    else:
        next_url = '/'
    if request.POST:
        form = GameMetaForm(request.POST, gifobj=gifobj, wordlimit=5)
        return HttpResponseRedirect(next_url)
    else:
        form = GameMetaForm(gifobj=gifobj, wordlimit=5)
    return render_to_response('gifgame.html',
                    dict(form=form, gifobj=gifobj, next_url=next_url),
                    context_instance=RequestContext(request))
