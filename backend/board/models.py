from django.db import models
from accounts.models import User
from groups.models import Study, Group
# Create your models here.


class Board(models.Model):
    study = models.OneToOneField(Study, on_delete=models.CASCADE, related_name='board_study')


class Article(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='article_board')
    title = models.CharField(max_length=100)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_writer')
    viewed_num = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='comment_board')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment_article')
    title = models.CharField(max_length=100)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_writer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)