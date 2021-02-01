from django.apps import AppConfig


class ArticleConfig(AppConfig):
    name = 'article'

    def ready(self):
        super(ArticleConfig, self).ready()
        from . import signals
