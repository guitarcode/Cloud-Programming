from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_account_diary_day_data),
    path('<int:pk>', views.account_diary_detail, name='account_diary_detail'),
    path('detail/', views.daily_list),
    path('others/', views.diary_others_list),
    path('account-diary/update/<int:pk>/', views.account_diary_update, name='account_diary_update'),
    path('account-diary/delete/<int:pk>/', views.account_diary_delete, name='account_diary_delete'),
    path('create/', views.DiaryCreate.as_view()),
]
