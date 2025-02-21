from django.urls import path
from .views import *

urlpatterns = [
    path('', articles, name='index'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('about/', about, name='about'),
    path('contact/', ContactPage.as_view(), name='contact'),
    path('logout/', logout_user, name='logout'),
    path('articles/', ArticlesListView.as_view()),
    path('articles/<int:pk>/', ArticlesDetailView.as_view()),
    path('myarticle/', userarticle, name='userarticle'),
    path('article/<slug:slug>/', singleblog, name='singleblog'),
]