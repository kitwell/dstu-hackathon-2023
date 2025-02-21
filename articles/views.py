from datetime import timezone
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .forms import *
from .serializers import ArticlesListSerializer,  ArticlesDetailSerializer


def articles(request):
    article = Articles.objects.all()
    category = Category.objects.all()
    recentarticle = Articles.objects.order_by('-time_create')[:5]
    return render(request, 'articles/blog.html', {'article': article, 'category': category, 'recentarticle': recentarticle})


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'articles/addarticle.html'
    success_url = reverse_lazy('index')



class SearchResultsView(ListView):
    model = Articles
    template_name = 'articles/ArticlesSearch.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Articles.objects.filter(Q(title__icontains=query))
        return object_list


def about(request):
    return render(request, 'articles/about.html')

def contact(request):
    return render(request, 'articles/contact.html')


def logout_user(request):
    logout(request)
    return redirect('index')


def singleblog(request, slug):
    article = get_object_or_404(Articles, slug=slug)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
            return redirect('singleblog', slug=slug)
    else:
        comment_form = CommentForm()
    article = get_object_or_404(Articles, slug=slug)
    category = Category.objects.all()
    recentarticle = Articles.objects.order_by('-time_create')[:5]
    comment = Comment.objects.all()
    countcomment = Articles.objects.annotate(num_comments=Count('comments')).all()
    return render(request, 'articles/single-blog.html', {'article': article, 'comment_form': comment_form,
                                                         'category': category, 'recentarticle': recentarticle, 'comment': comment, 'countcomment': countcomment})


def userarticle(request):
    article = Articles.objects.filter(user=request.user)
    category = Category.objects.all()
    recentarticle = Articles.objects.order_by('-time_create')[:5]
    return render(request, 'articles/userarticle.html', {'article': article, 'category': category, 'recentarticle': recentarticle})


class ContactPage(CreateView):
    form_class = AddContactForm
    template_name = 'articles/contact.html'
    success_url = reverse_lazy('index')


class ArticlesListView(APIView):
    def get(self, request):
        articles = Articles.objects.filter()
        serializer = ArticlesListSerializer(articles, many=True)
        return Response(serializer.data)


class ArticlesDetailView(APIView):
    def get(self, request, pk):
        articles = Articles.objects.get(id=pk)
        serializer = ArticlesDetailSerializer(articles)
        return Response(serializer.data)