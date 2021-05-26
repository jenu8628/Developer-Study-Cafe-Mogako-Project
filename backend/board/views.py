from django.db import models
from rest_framework import response
from groups.serializers import StudySerializer
from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets
from rest_framework import status, generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Board, Article, Comment
from .serializers import BoardSerializer, ArticleSerializer, CommentSerializer
from accounts.models import User
from groups.models import Study, Apply
# Create your views here.


class BoardViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    스터디에 1대1로 대응되는 게시판들의 목록과 각 게시판이 가진 글들을 확인할 수 있습니다.
    GET 요청을 통해 list, retrieve 함수만 기능합니다.
    '''
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def list(self, request):
        '''
        모든 게시판들을 확인할 수 있습니다.
        '''
        queryset = Board.objects.all()
        serialzer = BoardSerializer(queryset, many=True)
        return Response(serialzer.data)

    def retrieve(self, request, pk=None):
        '''
        pk값을 통해 각 게시판의 글들을 확인할 수 있습니다.
        '''
        target_study = Study.objects.get(id=pk)
        board = Board.objects.get(study=target_study)
        articles = Article.objects.filter(board=board)
        # serializer = ArticleSerializer(articles, many=True)
        res = [
            {
                'board': board.id,
                'articles': [ ArticleSerializer(single_article).data for single_article in articles ]
            }
        ]
        
        return Response(res)


# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer

#     def list(self, request, board):
#         target_board = Board.objects.get(id=board)
#         queryset = Article.objects.filter(board=target_board)
#         serializer = ArticleSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, board, pk=None):
#         target_board = Board.objects.get(id=board)
#         target_article = Article.objects.get(id=pk)
#         target_article.viewed_num += 1
#         target_article.save()
#         serializer = ArticleSerializer(target_article)
#         return Response(serializer.data)

#     def create(self, request, board):
#         writer = request.user
#         data = request.data
#         target_board = Board.objects.get(id=board)

#         new_article = Article.objects.create(
#             board=target_board, title=data['title'], content=data['content'], writer=writer
#         )

#         return Response(ArticleSerializer(new_article).data)


class ArticleView(APIView):
    '''
    GET 요청을 통해 게시판 내의 전체 글 목록을 불러오고,
    POST 요청을 통해 게시판에 글을 작성할 수 있습니다.
    필수 입력 값은 title, content입니다.
    {
        "title" : "input title",
        "content": "input content"
    }
    '''
    def get(self, request, board):
        target_board = Board.objects.get(id=board)
        queryset = Article.objects.filter(board=target_board)
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, board):
        writer = request.user
        data = request.data
        target_board = Board.objects.get(id=board)
        target_study = Study.objects.get(id=target_board.study.id)
        member_check = Apply.objects.filter(study=target_study, apply_user=request.user)

        if not member_check:
            return Response({"해당 스터디 회원이 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

        new_article = Article.objects.create(
            title=data['title'], content=data['content'], board=target_board, writer=writer
        )

        serializer = ArticleSerializer(new_article)
        return Response(serializer.data)


class ArticleDetailView(APIView):
    '''
    GET 요청을 통해 pk번째 글의 상세 내용을 보여줍니다.
    PUT 요청을 통해 pk번째 글을 수정할 수 있습니다.
    DELETE 요청을 통해 pk번째 글을 삭제할 수 있습니다.
    수정, 삭제의 경우 현재 로그인된 사용자가 글 작성자와 다른 경우 오류가 발생합니다. 
    '''
    def get(self, request, board, pk):
        article = Article.objects.get(id=pk)
        serializer = ArticleSerializer(article)
        
        article.viewed_num += 1
        article.save()

        return Response(serializer.data)

    def put(self, request, board, pk):
        article = Article.objects.get(id=pk)
        data = request.data

        if article.writer != request.user:
            return Response({"access denied"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ArticleSerializer(article, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, board, pk):
        article = Article.objects.get(id=pk)

        if article.writer != request.user:
            return Response({"access denied"}, status=status.HTTP_400_BAD_REQUEST)       

        article.delete()
        return Response({"Successfully Deleted"})


class CommentView(APIView):
    '''
    GET 요청을 통해 게시판 내의 전체 댓글 목록을 불러오고,
    POST 요청을 통해 글에 댓글을 작성할 수 있습니다.
    필수 입력 값은 title, content입니다.
    {
        "title" : "input title",
        "content": "input content"
    }
    '''
    def get(self, request, board, article):
        target_board = Board.objects.get(id=board)
        target_article = Article.objects.get(id=article)
        queryset = Comment.objects.filter(board=target_board, article=target_article)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, board, article):
        writer = request.user
        data = request.data
        target_board = Board.objects.get(id=board)
        target_article = Article.objects.get(id=article)
        target_study = Study.objects.get(id=target_board.study.id)
        member_check = Apply.objects.filter(study=target_study, apply_user=request.user)

        if not member_check:
            return Response({"해당 스터디 회원이 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

        new_comment = Comment.objects.create(
            title=data['title'], content=data['content'], board=target_board, article=target_article, writer=writer
        )

        serializer = CommentSerializer(new_comment)
        return Response(serializer.data)


class CommentDetailView(APIView):
    '''
    GET 요청을 통해 pk번째 댓글의 상세 내용을 보여줍니다.
    PUT 요청을 통해 pk번째 댓글을 수정할 수 있습니다.
    DELETE 요청을 통해 pk번째 댓글을 삭제할 수 있습니다.
    수정, 삭제의 경우 현재 로그인된 사용자가 댓글 작성자와 다른 경우 오류가 발생합니다. 
    '''
    def get(self, request, board, article, pk):
        comment = Comment.objects.get(id=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, board, article, pk):
        comment = Comment.objects.get(id=pk)
        data = request.data

        if comment.writer != request.user:
            return Response({"access denied"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(comment, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, board, article, pk):
        comment = Comment.objects.get(id=pk)

        if comment.writer != request.user:
            return Response({"access denied"}, status=status.HTTP_400_BAD_REQUEST)       

        comment.delete()
        return Response({"Successfully Deleted"}, status=status.HTTP_204_NO_CONTENT)
