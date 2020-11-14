from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from article.models import Category,Article
from article.forms import CategoryForm,ArticleForm
from datetime import datetime

def index(request):

    context = {'boldmessage': "товарищ"}
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

    response = render(request, 'article/index.html',context)
    return response

def category(request, category_slug):
    context = {}

    try:
        category = Category.objects.get(slug=category_slug)
        context['category_name'] = category.name

        articles = Article.objects.filter(category=category)
        context['articles'] = articles

        context['category'] = category
    except Category.DoesNotExist:
        raise Http404("Category does not exist")

    return render(request, 'article/category.html', context)

def article(request, article_slug):
    context = {}

    article = get_object_or_404(Article,slug=article_slug)
    context['article'] = article
    article.read += 1
    article.save()
    return render(request, 'article/article.html', context)

def about(request):
    return HttpResponse("opencads is dedicated to open source CAD tools")

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render(request, 'article/add_category.html', {'form':form})

@login_required
def add_article(request):

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save(commit=True)
            return article(request,new_article.slug)
        else:
            print(form.errors)
    else:
        form = ArticleForm()

    return render(request, 'article/add_article.html', {'form':form})
