from django.db.models import fields
from rest_framework import serializers
from .models import Board, Article, Comment
from accounts.models import User
from groups.models import Study


class WriterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']

class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    writer = WriterSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    writer = WriterSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

    def get_comments(self, article):
        target_comments = Comment.objects.filter(article=article)
        return [ CommentSerializer(single_comment).data for single_comment in target_comments]
