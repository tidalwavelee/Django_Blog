from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, Http404
from blog.models import Category,Article
from blog.forms import CategoryForm,ArticleForm

def index(request):
    context = {'boldmessage': "товарищ"}
    category_list = Category.objects.order_by('-name')[:5]
    context['categories'] = category_list
    article_list = Article.objects
    context['articles'] = article_list
    return render(request, 'blog/index.html',context)

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

    return render(request, 'blog/category.html', context)

def article(request, article_slug):
    context = {}

    article = get_object_or_404(Article,slug=article_slug)
    context['article'] = article

    return render(request, 'blog/article.html', context)

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

    return render(request, 'blog/add_category.html', {'form':form})

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

    return render(request, 'blog/add_article.html', {'form':form})
