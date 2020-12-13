from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.conf import settings
from django.core.paginator import Paginator
from article.models import Category,Article,ReadNum
from article.forms import CategoryForm,ArticleForm
from datetime import datetime
import markdown

ARTICLE_PER_PAGE = settings.ARTICLE_PER_PAGE
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

def _page_range(current_num, page_range):
  page_num = page_range[-1]
  pages = [i for i in range(current_num-2,current_num+3) if i in page_range]
  if pages[0] >= 3:
    pages.insert(0,'...')
  if pages[-1] <= page_num-2:
    pages.append('...')
  if pages[0] != 1:
    pages.insert(0,1)
  if pages[-1] != page_num:
    pages.append(page_num)
  return pages

def category(request, category_slug):
    page_num = request.GET.get('page',1)
    context = {}
    try:
        category = Category.objects.get(slug=category_slug)
        context['category'] = category
        articles = Article.objects.filter(category=category)
        context['articles'] = articles

        paginator = Paginator(articles,ARTICLE_PER_PAGE)
        article_page = paginator.get_page(page_num)
        context['article_page'] = article_page
        page_range = _page_range(article_page.number, paginator.page_range) 
        context['page_range'] = page_range
    except Category.DoesNotExist:
        raise Http404("Category does not exist")

    return render(request, 'article/category.html', context)

def article(request, article_pk):
  context = {}
  article = get_object_or_404(Article, pk=article_pk)
  article.md = markdown.markdown(article.body, extensions=[
                 'markdown.extensions.extra',
                 'markdown.extensions.codehilite',
                 'markdown.extensions.toc'])
  next_article = Article.objects.filter(created_at__gt=article.created_at).last()
  previous_article = Article.objects.filter(created_at__lt=article.created_at).first()
  context['article'] = article
  context['next_article'] = next_article
  context['previous_article'] = previous_article
  if not request.COOKIES.get(f"article_{article.pk}_visited"):
    if article.read_num.first():
      rn = article.read_num.first()
    else:
      rn = ReadNum(content_object=article,number=0)
    rn.number += 1
    rn.save()

  response = render(request, 'article/article.html', context)
  response.set_cookie(f"article_{article.pk}_visited",'true')
  return response

@login_required
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
            return article(request, new_article.pk)
        else:
            print(form.errors)
    else:
        form = ArticleForm()

    return render(request, 'article/add_article.html', {'form':form})
