from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import ArticleListSerializer, ArticleDetailSerializer, CategorySerializer
from .permissions import IsArticleAuthor
from .paginations import ArticleListApiViewPagination
from blog_app.models import Article, Category


class ArticleListApiView(ListAPIView):
    """
    show list of all articles with some extra data like url
    """
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()

    # pagination
    pagination_class = ArticleListApiViewPagination

    # filters, searches and ordering. its optional
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categories', 'author']
    search_fields = ['title']
    ordering_fields = ['id']


class ArticleDetailApiView(RetrieveUpdateDestroyAPIView):
    """
    get, update and delete article with pk but with different serializer to exclude some fields like url and more if needed
    only owner of this article can access it
    """
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminUser, IsArticleAuthor]
    queryset = Article.objects.all()
    lookup_field = 'pk'


class ArticleCreateApiView(CreateAPIView):
    """
    a view to create a new article. not a particular reason but it's cleaner i think! :)
    """
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminUser]


class CategoryListApiView(ListAPIView):
    """
    list of all categories
    """
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailApiView(RetrieveUpdateDestroyAPIView):
    """
    a view for category detail, update and delete.
    """
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
