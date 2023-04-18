from django.urls import path
from . import views

urlpatterns = [
    path('create-post/', views.PostCreate.as_view()),
    path('update-post/<int:pk>', views.PostUpdate.as_view()),
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),

    path('<int:pk>/add-comment', views.add_comment),
    path('category/<str:slug>/', views.categories_page),
    path('tag/<str:slug>/', views.tag_page),

    # path('category/no-categories', views.categories_page),
    # path('', views.index),
    # path('<int:pk>', views.post_detail),
]

