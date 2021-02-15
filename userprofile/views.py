from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from userprofile.models import Profile, FollowRelation, Favorite
from userprofile.forms import ProfileForm, FavoriteForm
from article.models import Article

def profile_detail(request, id):
  page_num = request.GET.get('page',1)
  profile_user = User.objects.get(id=id)
  if Profile.objects.filter(user_id=id).exists():
    profile = Profile.objects.get(user_id=id)
  else:
    profile = Profile.objects.create(user=profile_user)
  context = { 'profile': profile, 'profile_user': profile_user }

  # 用户文章
  user_articles = Article.objects.filter(author=profile_user)
  context['user_articles'] = user_articles

  return render(request, 'userprofile/profile_detail.html', context)

@login_required
def profile_edit(request, id):
  user = User.objects.get(id=id)
  if Profile.objects.filter(user_id=id).exists():
    profile = Profile.objects.get(user_id=id)
  else:
    profile = Profile.objects.create(user=user)

  if request.method == 'POST':
    if request.user != user:
      return HttpResponse("你没有权限修改此用户信息。")
    profile_form = ProfileForm(request.POST,request.FILES)
    if profile_form.is_valid():
      # 取得清洗后的合法数据
      profile_cd = profile_form.cleaned_data
      profile.title = profile_cd['title']
      profile.website = profile_cd['website']
      profile.bio = profile_cd['bio']
      if 'avatar' in request.FILES:
        profile.avatar = profile_cd["avatar"]
      profile.save()
      # 带参数的 redirect()
      return redirect("userprofile:profile_detail", id=id)
    else:
      return HttpResponse("注册表单输入有误。请重新输入~")
  else:
    if request.user != user:
      return profile_detail(request, id)
    profile_form = ProfileForm()
    context = { 'profile_form': profile_form, 'profile': profile, 'user': user }
    return render(request, 'userprofile/profile_edit.html', context)

@login_required
def user_delete(request, id):
  if request.method == 'POST':
    user = User.objects.get(id=id)
    # 验证登录用户、待删除用户是否相同
    if request.user == user:
      #退出登录，删除数据并返回博客列表
      logout(request)
      user.delete()
      return HttpResponse("感谢您对我们的支持，江湖再见")
    else:
      return HttpResponse("你没有删除操作的权限。")
  else:
    return HttpResponse("仅接受post请求。")

 # 关注
@login_required
def set_following(request):
  if request.is_ajax():
    user_id = request.POST['userID']
    try:
      followed = User.objects.get(id=user_id)
      following = request.user
    except Exception:
      return None
    if followed.id != following.id:
      friendship,created = FollowRelation.objects.get_or_create(
                             followed = followed,
                             following = following
                           )
      friendship.save()
      return HttpResponse('success')
    else:
      return HttpResponse(status=400)
  else:
    return HttpResponse("关注无效")
  
 # 取消关注
@login_required
def unfollow(request):
  if request.is_ajax():
    user_id = request.POST['followingID']
    try:
      followed = User.objects.get(id=user_id)
      following = request.user
    except Exception:
      return None
    friendship = FollowRelation.objects.get(
                           followed = followed,
                           following = following
                         )
    friendship.delete()
    return HttpResponse('success')
  else:
    return HttpResponse("操作无效")

# 收藏
@login_required
def add_favorite(request):
  data={"status": "ERROR"}
  if request.is_ajax():
    favorite_form = FavoriteForm(request.POST)
    if favorite_form.is_valid():
      favorite_cd = favorite_form.cleaned_data
      favorite, created = Favorite.objects.get_or_create(
                            user = request.user,
                            content_type = favorite_cd['content_type'],
                            object_id = favorite_cd['object_id']
                          )
      favorite.save()
      data["status"] = 'SUCCESS'
  else:
    data["status"] = 'Cannot used for query!'
  return JsonResponse(data)

# 取消收藏
@login_required
def del_favorite(request):
  if request.is_ajax():
    fav_id = request.POST['favID']
    favorite = Favorite.objects.get(id=fav_id)
    if request.user != favorite.user:
      return HttpResponse("无权操作")
    favorite.delete()
    return HttpResponse('success')
  else:
    return HttpResponse("操作无效")
