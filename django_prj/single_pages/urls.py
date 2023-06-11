from django.urls import path
from . import views
from blog import views as blog_view

urlpatterns = [
    path('', views.main),
    path('single/', blog_view.PostList.as_view())
]

