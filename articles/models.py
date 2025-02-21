from datetime import datetime

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
import qrcode
from django.utils.text import slugify
from autoslug import AutoSlugField


class Articles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    subtitle = models.CharField(max_length=200, verbose_name='Подзаголовок')
    content = RichTextUploadingField(verbose_name="Текст статьи")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Тема статьи', null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    qr_code = models.ImageField(upload_to='qrcodes', blank=True)
    slug = models.SlugField(max_length=250, db_index=True, blank=True, null=True, verbose_name='URL')
    image_preview = models.ImageField(upload_to="images/")
    image1 = models.ImageField(upload_to="images/", blank=True)
    image2 = models.ImageField(upload_to="images/", blank=True)
    image3 = models.ImageField(upload_to="images/", blank=True)
    image4 = models.ImageField(upload_to="images/", blank=True)


    def __str__(self):
        return self.title


class Category(models.Model):
    category = models.CharField(max_length=40, verbose_name='Тема статьи')

    def __str__(self):
        return self.category


class Contact(models.Model):
    topic = models.CharField(max_length=200, verbose_name='Тема сообщения')
    message = models.TextField(verbose_name='Сообщение')
    name = models.CharField(max_length=20, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')

    def __str__(self):
        return self.topic


class Review(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='reviews')
    email = models.EmailField(verbose_name='Email')
    name = models.CharField(max_length=200, verbose_name='Имя')
    text = models.TextField(max_length=2000, verbose_name='Комментарий')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=20, verbose_name='Имя')
    text = models.TextField(verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return self.name