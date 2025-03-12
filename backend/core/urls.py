from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('books/available/', views.get_available_books, name='get_available_books'),
    path('books/search/', views.search_book, name='search_book'),

    path('issues/<int:user_id>/', views.get_user_issue_entries, name='get_user_issue_entries'), # returns all issueEntry objects for given user
    path('issues/', views.get_self_issue_entries, name='get_self_issue_entries'), # returns issueEntry objects with self as user

    path('due/all', views.get_all_due_books, name='get_get_all_due_books'), # returns all issueEntry objects which are due.
    path('due/', views.get_self_due_books, name='get_self_due_books'), # returns due issueEntry objects with self as the user.
    path('due/<int:user_id>/', views.get_user_due_books, name='get_user_due_books'), # returns due issueEntrt objects with user with user_id

    path('issue-book/', views.issue_book, name='issue_book'),
    path('return-book/', views.return_book, name='return_book'),
    path('reissue-book/', views.reissue_book, name='reissue_book'),

    path('create-user/', views.create_user, name='create_user'), 

    # getters
    path('users/', views.get_all_users, name='get_all_users'), # gets all users.
    path('users/<int:user_id>/', views.get_user, name='get_user'), # get user with id
    path('issues/', views.get_all_issue_entries, name='get_all_issue_entries'), # returns all issueEntry objects
    path('issues/entry/<int:transaction_id>/', views.get_issue_entry, name='get_issue_entry'), # get issueEntry obj.
    path('books/', views.get_all_books, name='get_all_books'), # get all books
    path('books/<int:book_id>/', views.get_book, name='get_book'), # get book
] 