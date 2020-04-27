from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from blog.models import Category,Article
from blog.forms import CategoryForm,ArticleForm
from blog.forms import UserForm,UserProfileForm

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

    return render(request, 'blog/add_article.html', {'form':form})

def register(request):
    # flag for registration succeed
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # save the user's form data to the database
            user = user_form.save()
            # hash the password with set_password
            user.set_password(user.password)
            # update user object
            user.save()
            # since set user attribute ourselves, use commit=False
            profile = profile_form.save(commit=False)
            profile.user = user
            # transfer picture from input form to profile object when given
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            # save profile object
            profile.save()

            # update the flag of registration
            registered = True
        else:
            print(f"{user_form.errors}\n{profile_form.errors}")
    # Not a HTTP POST, render two blank forms for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    # Render the template depending on the context
    return render( request, 'blog/register.html',
                   {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):
    if request.method == 'POST':
        # request.POST.get() would return None if not exist
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use dj machinery, a user object is returned when combination valid
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/blog/')
            else:
                return HttpResponse("Your account is not active.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    # not a HTTP POST, display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        return render(request, 'blog/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    # redirect to homepage
    return HttpResponseRedirect('/blog/')
