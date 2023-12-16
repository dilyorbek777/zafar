from django.urls import path
from .views import *
urlpatterns = [
    path('', homePageView, name='home'),
    path('menu/', menuPageView, name='menu'),
    path('about/', aboutPageView, name='about'),
    path('food/<slug:slug>/', SinglePageView, name='singlepage'),
    path('404/', not_found, name='pg404'),

]