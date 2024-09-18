from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.utils.html import format_html
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class ArticleManager(models.Manager):
    def get_active_articles(self):
        return self.filter(is_active=True)


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='blog/%Y/%m/%d', null=True, blank=True)
    image_alt = models.CharField(max_length=255)
    categories = models.ManyToManyField('Category', related_name='article_categories', blank=True)
    tags = models.ManyToManyField('tag', related_name='article_tags', blank=True)
    description = RichTextUploadingField()
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = ArticleManager()

    def __str__(self):
        return self.title

    def get_absolute_api_url(self):
        return 'http://127.0.0.1:8000' + reverse('blog_app:blog_app_api_v1:article_detail', args=[self.pk])
    # def get_absolute_url(self):
    #     return reverse('blog:blog_detail', args=[self.slug])

    # def image_tag(self):
    #     return format_html(
    #         '<img width=100 height=100 loading="lazy" style="border-radius: 10px;" src="{}">'.format(
    #             self.image.url))
    #
    # image_tag.short_description = 'image'


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('blog:blog_category_list', args=[self.slug])


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('blog:blog_tag_list', args=[self.slug])


class Seo(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='seo')
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    follow = models.CharField(max_length=100, default='index, follow')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comments', null=True, blank=True)
    # reply_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_reply_to', blank=True,
    #                              null=True, verbose_name='در پاسخ به')
    is_reply = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
