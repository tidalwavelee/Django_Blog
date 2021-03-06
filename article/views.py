from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.views import View
from article.models import Category,Article,ReadNum,LikeNum
from article.forms import CategoryForm,ArticleForm
from datetime import datetime
import markdown

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

    response = render(request, 'article/index.html',context)
    return response

def category(request, category_slug):
  page_num = request.GET.get('page',1)
  context = {}
  try:
    category = Category.objects.get(slug=category_slug)
    context['category'] = category
    articles = Article.objects.filter(category=category)
    context['articles'] = articles
  except Category.DoesNotExist:
    raise Http404("Category does not exist")

  return render(request, 'article/category.html', context)

def article_detail(request, category_slug, article_pk):
  context = {}
  article = get_object_or_404(Article, pk=article_pk)
  md = markdown.Markdown(
         extensions=['markdown.extensions.extra',
                     'markdown.extensions.codehilite',
                     'markdown.extensions.toc']
       )
  article.md = md.convert(article.body)
  article.toc = md.toc
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
def category_edit(request, id):
  if not request.user.is_staff:
    return HttpResponse("无权限操作")
  a_cate = Category.objects.get(id=id)
  if request.method == 'POST':
    form = CategoryForm(request.POST,request.FILES,instance=a_cate)
    if form.is_valid():
      form_cd = form.cleaned_data
      a_cate.name = form_cd['name']
      a_cate.bio = form_cd['bio']
      a_cate.article_content = form_cd['article_content']
      if 'emblem' in request.FILES:
        a_cate.emblem = form.cleaned_data['emblem']
      a_cate.save()
      return redirect("article:category",a_cate.slug)
    else:
      return HttpResponse(form.errors)
  else:
    form = CategoryForm(instance=a_cate)

  return render(request, 'article/category_edit.html', {'form':form})

@login_required
def article_edit(request, id=0):
  if request.method == 'POST':
    form = ArticleForm(request.POST)
    if form.is_valid():
      if id > 0:
        article = Article.objects.get(id=id)
        article.title = request.POST['title']
        category = Category.objects.get(id=request.POST['category'])
        article.category = category
        article.body = request.POST['body']
      else:
        article = form.save(commit=False)
        article.author = request.user
      article.save()
      return article_detail(request, "", article.pk)
    else:
      return HttpResponse(form.errors)
  else:
    if id > 0:
      article = Article.objects.get(id=id)
      if request.user != article.author:
        return article_detail(request, "", article.pk)
      form = ArticleForm(instance=article)
    else:
      form = ArticleForm()
  return render(request, 'article/article_edit.html', {'form':form})

def article_delete(request, id):
  if request.method == "POST":
    article = Article.objects.get(id=id)
    article.delete()
    return redirect("article:index")
  else:
    return HttpResponse("无效删除操作")

 # 点赞数 +1
def increase_likes(request):
  if request.is_ajax():
    article_id = request.POST['articleID']
    article = Article.objects.get(id=article_id)
    if article.like_num.first():
      like = article.like_num.first()
    else:
      like = LikeNum(content_object=article,number=0)
    like.number += 1
    like.save()
    return HttpResponse('success')
  else:
    return HttpResponse("无效点赞操作")
