from django.urls import path, include
from . import views

app_name = 'account_app'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('api/v1/', include('account_app.api.v1.urls')),
]
