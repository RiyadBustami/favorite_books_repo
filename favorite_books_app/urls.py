from django.urls import path
from . import views

urlpatterns=[
    path('',views.show_books),
    path('add_book/',views.add_book),
    path('<book_id>/',views.show_book),
    path('<book_id>/add_book_to_favorites/',views.add_book_to_favorites),
    path('<book_id>/unfavorite_book/',views.unfavorite_book),
    path('<book_id>/update_book/',views.update_book),
    path('<book_id>/delete/',views.delete_book),
]