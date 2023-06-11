from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_account_diary_data),
    path('create/', views.DiaryCreate.as_view()),

]

