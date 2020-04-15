from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:to_user_id>/', views.room, name='room'),
]
