from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import User, Book, BookIssue, Notification
from .serializers import (
    UserSerializer, BookSerializer, BookIssueSerializer, 
    NotificationSerializer, LoginSerializer
)
from .authentication import CsrfExemptSessionAuthentication

# Custom permissions
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'ADMIN'

class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['STAFF', 'ADMIN']

class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.user_type in ['STAFF', 'ADMIN']:
            return True
        return obj.user == request.user

# Authentication views
class LoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                'user': UserSerializer(user).data,
                'message': 'Login successful'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'})

class GetCSRFToken(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({"detail": "CSRF cookie set"})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action == 'list':
            permission_classes = [IsStaffUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def current_user(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# Book management views
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsStaffUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def request_issue(self, request, pk=None):
        book = self.get_object()
        user = request.user
        
        if book.available_copies <= 0:
            return Response(
                {'error': 'No copies available for issue'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Check if user already has an active request or issue for this book
        existing_issues = BookIssue.objects.filter(
            user=user, 
            book=book, 
            status__in=['REQUESTED', 'ISSUED']
        )
        
        if existing_issues.exists():
            return Response(
                {'error': 'You already have an active request or issue for this book'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book_issue = BookIssue.objects.create(
            book=book,
            user=user,
            status='REQUESTED'
        )
        
        # Create notification for staff
        staff_users = User.objects.filter(user_type__in=['STAFF', 'ADMIN'])
        for staff in staff_users:
            Notification.objects.create(
                user=staff,
                message=f"{user.get_full_name()} has requested '{book.title}'",
                notification_type='ISSUE_REQUEST',
                book_issue=book_issue
            )
        
        return Response(BookIssueSerializer(book_issue).data)

# Book Issue views
class BookIssueViewSet(viewsets.ModelViewSet):
    serializer_class = BookIssueSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['STAFF', 'ADMIN']:
            return BookIssue.objects.all()
        return BookIssue.objects.filter(user=user)
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsStaffUser]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if request.user.user_type not in ['STAFF', 'ADMIN']:
            return Response(
                {'error': 'You do not have permission to approve book issues'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        book_issue = self.get_object()
        
        try:
            book_issue.issue_book(request.user)
            
            # Create notification for the user
            Notification.objects.create(
                user=book_issue.user,
                message=f"Your request for '{book_issue.book.title}' has been approved",
                notification_type='ISSUED',
                book_issue=book_issue
            )
            
            return Response(BookIssueSerializer(book_issue).data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        if request.user.user_type not in ['STAFF', 'ADMIN']:
            return Response(
                {'error': 'You do not have permission to reject book issues'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        book_issue = self.get_object()
        
        if book_issue.status != 'REQUESTED':
            return Response(
                {'error': 'Only requested books can be rejected'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        book_issue.status = 'REJECTED'
        book_issue.save()
        
        # Create notification for the user
        Notification.objects.create(
            user=book_issue.user,
            message=f"Your request for '{book_issue.book.title}' has been rejected",
            notification_type='ISSUE_REQUEST',
            book_issue=book_issue
        )
            
        return Response(BookIssueSerializer(book_issue).data)
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        book_issue = self.get_object()
        
        if request.user.user_type not in ['STAFF', 'ADMIN']:
            return Response(
                {'error': 'You do not have permission to mark books as returned'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        try:
            book_issue.return_book()
            
            # Create notification for the user
            Notification.objects.create(
                user=book_issue.user,
                message=f"You have returned '{book_issue.book.title}'",
                notification_type='RETURNED',
                book_issue=book_issue
            )
            
            return Response(BookIssueSerializer(book_issue).data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def reissue(self, request, pk=None):
        book_issue = self.get_object()
        
        if request.user != book_issue.user and request.user.user_type not in ['STAFF', 'ADMIN']:
            return Response(
                {'error': 'You do not have permission to reissue this book'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        try:
            book_issue.reissue_book()
            
            # Create notification for the user
            Notification.objects.create(
                user=book_issue.user,
                message=f"'{book_issue.book.title}' has been reissued. New due date: {book_issue.due_date.strftime('%Y-%m-%d')}",
                notification_type='ISSUED',
                book_issue=book_issue
            )
            
            return Response(BookIssueSerializer(book_issue).data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    @action(detail=False, methods=['get'])
    def my_issues(self, request):
        queryset = BookIssue.objects.filter(user=request.user)
        serializer = BookIssueSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        if request.user.user_type not in ['STAFF', 'ADMIN']:
            return Response(
                {'error': 'You do not have permission to view overdue books'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        now = timezone.now()
        overdue_issues = BookIssue.objects.filter(
            status='ISSUED',
            due_date__lt=now
        )
        
        # Update status to OVERDUE
        for issue in overdue_issues:
            issue.check_if_overdue()
        
        overdue_issues = BookIssue.objects.filter(status='OVERDUE')
        serializer = BookIssueSerializer(overdue_issues, many=True)
        return Response(serializer.data)

# Notification views
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response(NotificationSerializer(notification).data)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        notifications = self.get_queryset()
        notifications.update(is_read=True)
        return Response({'message': 'All notifications marked as read'})

# Dashboard statistics
@api_view(['GET'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    
    if user.user_type in ['STAFF', 'ADMIN']:
        # Staff/Admin stats
        total_books = Book.objects.count()
        total_users = User.objects.filter(user_type='MEMBER').count()
        pending_requests = BookIssue.objects.filter(status='REQUESTED').count()
        overdue_books = BookIssue.objects.filter(status='OVERDUE').count()
        
        return Response({
            'total_books': total_books,
            'available_books': Book.objects.filter(available_copies__gt=0).count(),
            'total_users': total_users,
            'pending_requests': pending_requests,
            'issued_books': BookIssue.objects.filter(status='ISSUED').count(),
            'overdue_books': overdue_books
        })
    else:
        # Member stats
        my_books = BookIssue.objects.filter(user=user)
        
        return Response({
            'total_issued': my_books.filter(status='ISSUED').count(),
            'total_requested': my_books.filter(status='REQUESTED').count(),
            'total_returned': my_books.filter(status='RETURNED').count(),
            'overdue_books': my_books.filter(status='OVERDUE').count()
        })
