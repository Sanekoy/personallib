from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_collection, name='choose_collection'),
    path('collection/<int:collection_id>/', views.view_collection, name='view_collection'),  # Добавим URL для просмотра коллекции
    path('create_collection/', views.choose_collection, name='create_collection'),  # Используем тот же view для создания
    path('collection/<int:collection_id>/add_book/', views.add_book, name='add_book'),
    path('book/<int:book_id>/', views.view_book, name='view_book'),
]