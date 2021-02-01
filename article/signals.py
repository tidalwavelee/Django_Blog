from django.db.models.signals import post_save
from django.dispatch import receiver
from article.models import Article
import markdown

@receiver(post_save, sender=Article)
def update_category_content(sender, instance, **kwargs):
  md = markdown.Markdown(
         extensions=['markdown.extensions.extra',
                     'markdown.extensions.codehilite',
                     'markdown.extensions.toc']
       )
  article_md = md.convert(instance.body)
  article_toc = md.toc

  title_link = f"<a href=\"{instance.id}/\">{instance.title}</a>"
  title_line = title_link
  category = instance.category
  category.article_content += title_line
  article_toc = article_toc.replace("#",f"{instance.id}/#")
  category.article_content += article_toc
  category.save()

