from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.conf import settings
from django.core.paginator import Paginator
from django.views import View
from article.models import Category,ReadNum,LikeNum
from news.models import News
from article.forms import CategoryForm
from news.forms import NewsForm
from datetime import datetime
import markdown

ARTICLE_PER_PAGE = settings.ARTICLE_PER_PAGE
def index(request):

    context = {}
    category_list = Category.objects.order_by('-name')[:5]
    context['categories'] = category_list

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

    response = render(request, 'news/index.html',context)
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
    news = News.objects.filter(category=category)
    context['newss'] = news

    paginator = Paginator(news,ARTICLE_PER_PAGE)
    news_page = paginator.get_page(page_num)
    context['news_page'] = news_page
    page_range = _page_range(news_page.number, paginator.page_range) 
    context['page_range'] = page_range
  except Category.DoesNotExist:
    raise Http404("Category does not exist")

  return render(request, 'news/category.html', context)

def news_detail(request, category_slug, news_pk):
  context = {}
  news = get_object_or_404(News, pk=news_pk)
  md = markdown.Markdown(
         extensions=['markdown.extensions.extra',
                     'markdown.extensions.codehilite',
                     'markdown.extensions.toc']
       )
  news.md = md.convert(news.body)
  news.toc = md.toc
  next_news = News.objects.filter(created_at__gt=news.created_at).last()
  previous_news = News.objects.filter(created_at__lt=news.created_at).first()
  context['news'] = news
  context['next_news'] = next_news
  context['previous_news'] = previous_news
  if not request.COOKIES.get(f"news_{news.pk}_visited"):
    if news.read_num.first():
      rn = news.read_num.first()
    else:
      rn = ReadNum(content_object=news,number=0)
    rn.number += 1
    rn.save()

  response = render(request, 'news/news.html', context)
  response.set_cookie(f"news_{news.pk}_visited",'true')
  return response

@login_required
def news_edit(request, id=0):
  if request.method == 'POST':
    form = NewsForm(request.POST)
    if form.is_valid():
      if id > 0:
        news = News.objects.get(id=id)
        news.title = request.POST['title']
        category = Category.objects.get(id=request.POST['category'])
        news.category = category
        news.body = request.POST['body']
      else:
        news = form.save(commit=False)
        news.author = request.user
      news.save()
      return news_detail(request, "", news.pk)
    else:
      return HttpResponse(form.errors)
  else:
    if id > 0:
      news = News.objects.get(id=id)
      if request.user != news.author:
        return news_detail(request, "", news.pk)
      form = NewsForm(instance=news)
    else:
      form = NewsForm()
  return render(request, 'news/news_edit.html', {'form':form})

def news_delete(request, id):
  if request.method == "POST":
    news = News.objects.get(id=id)
    news.delete()
    return redirect("news:index")
  else:
    return HttpResponse("无效删除操作")

 # 点赞数 +1
def increase_likes(request):
  if request.is_ajax():
    news_id = request.POST['newsID']
    news = News.objects.get(id=news_id)
    if news.like_num.first():
      like = news.like_num.first()
    else:
      like = LikeNum(content_object=news,number=0)
    like.number += 1
    like.save()
    return HttpResponse('success')
  else:
    return HttpResponse("无效点赞操作")
