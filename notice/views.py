from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class NoticeListView(LoginRequiredMixin, ListView):
    """通知列表"""
    # 上下文的名称
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice/notices.html'
    # 登录重定向
    login_url = '/accounts/login/'

    # 未读通知的查询集
    def get_queryset(self):
        return self.request.user.notifications.unread()
