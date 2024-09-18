from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ArticleListApiViewPagination(PageNumberPagination):
    """
    custom pagination for articles
    """
    page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'total_articles_count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'articles': data
        })
