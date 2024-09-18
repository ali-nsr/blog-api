from django.urls import path, include

app_name = 'blog_app'

urlpatterns = [
    path('api/v1/', include('blog_app.api.v1.urls')),
]
