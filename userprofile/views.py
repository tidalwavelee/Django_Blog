from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from userprofile.models import Profile
from userprofile.forms import ProfileForm

def profile_detail(request, id):
  profile_user = User.objects.get(id=id)
  if Profile.objects.filter(user_id=id).exists():
    profile = Profile.objects.get(user_id=id)
  else:
    profile = Profile.objects.create(user=profile_user)
  context = { 'profile': profile, 'profile_user': profile_user }
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
