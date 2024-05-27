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
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('generate_pdf_report/<int:collection_id>/', views.generate_pdf_report, name='generate_pdf_report'),
    path('collection/<int:collection_id>/book/<int:book_id>/generate_pdf_report/', views.generate_book_pdf_report, name='generate_book_pdf_report'),
    
]