from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, BookViewSet, BookIssueViewSet, NotificationViewSet,
    LoginView, LogoutView, GetCSRFToken, dashboard_stats
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'book-issues', BookIssueViewSet, basename='book-issue')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('csrf-token/', GetCSRFToken.as_view(), name='csrf'),
    path('dashboard-stats/', dashboard_stats, name='dashboard-stats'),
] 