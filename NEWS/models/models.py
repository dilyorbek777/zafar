from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=News.Status.Published)


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class News(models.Model):
    class Status(models.TextChoices):
        Draft = "DF", "Draft"
        Published = "PB", "Published"

    title = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    body = models.TextField()
    image = models.ImageField(upload_to="news/images")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.Draft
    )
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-publish_time"]

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('single', args=[self.slug])


class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    message = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return self.message


class Food(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="foods/images")
    price = models.FloatField(max_length=30)
    slug = models.CharField(max_length=250)
    text = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return self.name


class Cheifs(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='foods/cheif')
    objects = models.Manager()
    
    def __str__(self):
        return self.name