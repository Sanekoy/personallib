from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_collection, name='choose_collection'),
    path('collection/<int:collection_id>/', views.view_collection, name='view_collection'),  # Добавим URL для просмотра коллекции
    path('create_collection/', views.choose_collection, name='create_collection'),  # Используем тот же view для создания
    path('collection/<int:collection_id>/add_book/', views.add_book, name='add_book'),
    path('collection/<int:collection_id>/book/<int:book_id>/', views.view_book, name='view_book'),
    path('collection/<int:collection_id>/book/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('collection/<int:collection_id>/book/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_publisher/', views.add_publisher, name='add_publisher'),
    path('add_genre/', views.add_genre, name='add_genre'),
    path('add_tag/', views.add_tag, name='add_tag'),
    
]