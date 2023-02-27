from django.urls import path
from . import views

urlpatterns = [

    path('book_app/', views.BookAPI.as_view(), name='book'),
    path('book_app/<int:id>', views.BookAPI.as_view(), name='book'),

]