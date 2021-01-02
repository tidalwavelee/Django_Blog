from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from article.models import Category,Article
from datetime import datetime

def home(request):

    context = {}
    category_list = Category.objects.order_by('-name')[:5]
    context['categories'] = category_list
    article_list = Article.objects
    context['articles'] = article_list

    # cookie of visiting
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7],"%Y-%m-%d %H:%M:%S")
        if (datetime.now()-last_visit_time).days > 0:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context['visit'] = visits

    response = render(request, 'home.html',context)
    return response


def about(request):
    return HttpResponse("opencads is dedicated to open source CAD tools")
