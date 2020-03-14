from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Category,Article

def index(request):
    context = {'boldmessage': "товарищ"}
    category_list = Category.objects.order_by('-name')[:5]
    context['categories'] = category_list
    article_list = Article.objects
    context['articles'] = article_list
    return render(request, 'blog/index.html',context)

def category(request, category_name_slug):
    context = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context['category_name'] = category.name

        articles = Article.objects.filter(category=category)
        context['articles'] = articles

        context['category'] = category
    except Category.DoesNotExist:
        pass

    return render(request, 'blog/category.html', context)

def about(request):
    return HttpResponse("opencads is dedicated to open source CAD tools")
