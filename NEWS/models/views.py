from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
import random
from hitcount.views import HitCountDetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class OnlyLogedSuperUser(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


def homePageView(request):
    foods = Food.objects.all()[:4]
    cheif = Cheifs.objects.all()[:3]
    context = {
        'foods':foods,
        'cheif':cheif
    }
    return render(request, 'index.html', context)


def menuPageView(request):
    foods = Food.objects.all()[:4]
    cheif = Cheifs.objects.all()[:3]
    context = {
        'foods':foods,
        'cheif':cheif
    }
    return render(request, 'shop.html', context)

def aboutPageView(request):
    foods = Food.objects.all()[:4]
    cheif = Cheifs.objects.all()[:3]
    context = {
        'foods':foods,
        'cheif':cheif
    }
    return render(request, 'about.html', context)


def SinglePageView(request, slug):
    
    food = get_object_or_404(Food, slug=slug)
    foods = Food.objects.all()[:4]
    cheif = Cheifs.objects.all()[:3]

    context = {
        'foods':foods,
        'cheif':cheif,
        'food':food,
    }
    return render(request, 'spage.html', context)

def not_found(request):
    return render(request, '404.html', {})
# x = random.choice(News.slug)
# print(x)

def single_page(request, slug):
    new = get_object_or_404(News, slug=slug, status=News.Status.Published)
    slider_news = News.published.all().order_by('-publish_time')[:5]
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(new)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['hits'] = hits


    new_comment = None
    
    context = {
        'new': new,
        'slider_news': slider_news,
        'comments': comments,
        "new_comment": new_comment,
    }
    return render(request, 'single.pg.html', context)


def contact_page(request):
    form = ContactForm(request.POST or None)
    posts = Contact.objects.all()[:6]
    if request.method == 'POST' and form.is_valid():
        form.save()
    return render(request, 'contact.html', {'form': form, 'posts': posts})


# ***** CATEGORIES *****
def NationalNews(request):
    national_news = News.published.all().filter(category__name='National')
    slider_news = News.published.all().order_by('-publish_time')[:10]
    context = {
        'national_news': national_news,
        'slider_news': slider_news
    }
    return render(request, 'national.html', context)


def InterNational_News(req):
    international_news = News.published.all().filter(category__name='International')
    slider_news = News.published.all().order_by('-publish_time')[:10]

    context = {
        'international_news': international_news,
        'slider_news': slider_news
    }

    return render(req, 'international.html', context)

def SocietyNews(request):
    society_news = News.published.all().filter(category__name='Society')
    slider_news = News.published.all().order_by('-publish_time')[:10]
    context = {
        'society_news': society_news,
        'slider_news': slider_news
    }
    return render(request, 'Society.html', context)

def SportNews(request):
    sport_news = News.published.all().filter(category__name='Sport')
    slider_news = News.published.all().order_by('-publish_time')[:10]
    context = {
        'sport_news': sport_news,
        'slider_news': slider_news
    }
    return render(request, 'Sport.html', context)


def TechnologyNews(request):
    technology_news = News.published.all().filter(category__name='Technology')
    slider_news = News.published.all().order_by('-publish_time')[:10]
    context = {
        "technology_news": technology_news,
        'slider_news': slider_news
    }
    return render(request, 'technology.html', context)


def FinancialNews(request):
    financial_news = News.published.all().filter(category__name='Fianacial')
    slider_news = News.published.all().order_by('-publish_time')[:10]
    context = {
        'financial_news': financial_news,
        'slider_news': slider_news
    }
    return render(request, 'financial.html', context)



# *** CRUD ****
class NewsUpdateView(OnlyLogedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'status', 'category')
    template_name = 'edit.html'
    success_url = reverse_lazy('home')

class NewsDeleteView(OnlyLogedSuperUser, DeleteView):
    model = News
    template_name = 'delete.html'
    success_url = reverse_lazy('home')

class NewsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = News
    template_name = 'create.html'
    fields = ('title', 'slug', 'body', 'image', 'status', 'category', 'publish_time')
    success_url = reverse_lazy('home')
    def test_func(self):
        return self.request.user.is_superuser


def admin_page(request):
    admin_user = User.objects.filter(is_superuser=True)
    context = {
        'admin_user': admin_user
    }

    return render(request, 'admin.html', context)



class Search_View(ListView):
    model = News
    template_name = 'search.html'
    context_object_name = 'all_news'
    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))