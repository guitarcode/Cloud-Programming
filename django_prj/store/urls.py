from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.StoreCreate.as_view()),
    path('', views.StoreListView.as_view()),
    path('<int:store_id>/', views.store_detail, name='store_detail'),
]
