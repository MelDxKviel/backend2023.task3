from datetime import datetime
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from Blog.fields import PNGField


class Category(models.Model):
    category_name = models.CharField(max_length=120)

    def __str__(self):
        return self.category_name


class Tag(models.Model):
    tag_name = models.CharField(max_length=120)

    def __str__(self):
        return self.tag_name


class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")
    content = models.TextField()
    image = PNGField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
    tags = models.ManyToManyField(Tag, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})

    def get_tags(self):
        return ', '.join([tag.tag_name for tag in self.tags.all()])

    get_tags.short_description = "Admin Names"

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.text[:25]} ({self.author}) - {self.post.title}"

    class Meta:
        ordering = ['created_at']
