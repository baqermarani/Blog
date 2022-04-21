from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from .models import Article, Category, UserProfile


# Create your views here.
class IndexPage(TemplateView):

    def get(self, request, *args, **kwargs):
        article_data = []
        all_Articles = Article.objects.order_by('-created_at').all()[:3]

        for article in all_Articles:
            article_data.append({
                'title': article.title,
                'cover': article.cover.url,
                'category': article.category.title,
                'created_at': article.created_at.date(),
            })

        all_promoted_Articles = Article.objects.filter(promote=True)
        promoted_data = []
        for article in all_promoted_Articles:
            promoted_data.append({
                'title': article.title,
                'cover': article.cover.url if article.cover else None,
                'category': article.category.title,
                'Author': article.author.user.first_name + ' ' + article.author.user.last_name,
                'Avatar': article.author.avatar.url if article.author.avatar else None,
                'created_at': article.created_at.date(),
            })

        context = {
            'article_data': article_data,
            'promoted_article_data': promoted_data,
        }

        return render(request, 'index.html', context)


class ContactPage(TemplateView):
    template_name = 'page-contact.html'

class AllArticleAPIViwe(APIView):
    def get(self , request , format=None):
        try:
            all_Articles = Article.objects.all().order_by('-created_at')[:10]
            article_data = []
            for article in all_Articles:
                article_data.append({
                    'title': article.title,
                    'cover': article.cover.url if article.cover else None,
                    'category': article.category.title,
                    'created_at': article.created_at.date(),
                })
            return Response( {'data': article_data} , status = status.HTTP_200_OK )




        except:

            return Response({'status': "Internal Server Error, We'll Check It Later"},

                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleArticle(APIView):
    def get(self , request , format=None):
        try:
            article_title = request.GET['article_title']
            article = Article.objects.filter(title__contains=article_title)
            serialize_data =serializers.ArticleSerializer(article , many=True)
            return Response({'data': serialize_data.data} , status = status.HTTP_200_OK )
        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchArticleAPIViwe(APIView):
    def get(self , request , format=None):
        try:
            from django.db.models import Q
            search_keyword = request.GET['search_keyword']
            articles = Article.objects.filter(Q(content__icontains=search_keyword))
            serialize_data = serializers.ArticleSerializer(articles , many=True)
            return Response({'data': serialize_data.data} , status = status.HTTP_200_OK )
        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubmitArticleAPIView(APIView):

    def post(self, request, format=None):

        try:
            serializer = serializers.SubmitArticleSerializer(data=request.data)
            if serializer.is_valid():
                title = serializer.data.get('title')
                cover = request.FILES['cover']
                content = serializer.data.get('content')
                category_id = serializer.data.get('category_id')
                author_id = serializer.data.get('author_id')
                promote = serializer.data.get('promote')
            else:
                return Response({'status':'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(id=author_id)
            author = UserProfile.objects.get(user=user)
            category = Category.objects.get(id=category_id)

            article = Article()
            article.title = title
            article.cover = cover
            article.content = content
            article.category = category
            article.author = author
            article.promote = promote
            article.save()

            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateArticleAPIView(APIView):

    def post(self, request, format=None):

        try:
            serializer = serializers.UpdateArticleSerializer(data=request.data)

            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
                cover = request.FILES['cover']

            else:
                return Response({'status':'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

            Article.objects.filter(id=article_id).update(cover=cover)

            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        except:

            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteArticleAPIView(APIView):

    def post(self, request, format=None):

        try:
            serializer = serializers.DeleteArticleSerializer(data=request.data)

            if serializer.is_valid():
                article_id = serializer.data.get('article_id')

            else:
                return Response({'status':'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

            Article.objects.filter(id=article_id).delete()

            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        except:

            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)