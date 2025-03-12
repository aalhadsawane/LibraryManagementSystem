from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import Q
from datetime import date, timedelta
from .models import Book, IssueEntry, CustomUser
from .serializers import BookSerializer, IssueEntrySerializer, CustomUserSerializer
from .permissions import IsAdmin, IsStaffOrAdmin, IsMember
from django.db import models

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        auth_login(request, user)  # Create session
        return Response({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'name': user.name
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    auth_logout(request)
    return Response({'message': 'Successfully logged out'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_books(request):
    books = Book.objects.filter(available=True)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffOrAdmin])
def get_user_due_books(request, user_id):
    # get due books of user mentioned in url
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    entries = IssueEntry.objects.filter(
        user=user,
        return_date__isnull=True,
        due_date__lt=date.today()
    )
    serializer = IssueEntrySerializer(entries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_self_due_books(request):
    # get due books of self user.
    entries = IssueEntry.objects.filter(
        user=request.user,
        return_date__isnull=True,
        due_date__lt=date.today()
    )
    serializer = IssueEntrySerializer(entries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffOrAdmin])
def get_all_due_books(request):
    # get all due books across several users.
    entries = IssueEntry.objects.filter(
        return_date__isnull=True
    )
    serializer = IssueEntrySerializer(entries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffOrAdmin])
def get_user_issue_entries(request, user_id):
    # get issue entries for user in url
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    entries = IssueEntry.objects.filter(user=user)
    serializer = IssueEntrySerializer(entries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_self_issue_entries(request, user_id):
    # get issue entries for self user

    entries = IssueEntry.objects.filter(user=request.user)
    serializer = IssueEntrySerializer(entries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffOrAdmin])
def get_all_issue_entries(request):
    # get issue entries for all users
    entries = IssueEntry.objects.all()
    serializer = IssueEntrySerializer(entries, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsStaffOrAdmin])
def issue_book(request):
    book = get_object_or_404(Book, id=request.data.get('book'))
    user = get_object_or_404(CustomUser, id=request.data.get('user'))
    
    if not book.available:
        return Response({'error': 'Book not available'}, status=status.HTTP_400_BAD_REQUEST)
    
    entry = IssueEntry(
        book=book,
        user=user,
        validator=request.user
    )
    entry.save()
    book.available = False
    book.save()
    
    serializer = IssueEntrySerializer(entry)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsStaffOrAdmin])
def return_book(request):
    entry = get_object_or_404(
        IssueEntry,
        book_id=request.data.get('book'),
        user_id=request.data.get('user'),
        return_date__isnull=True
    )
    
    entry.return_date = date.today()
    if entry.due_date < date.today():
        days_late = (date.today() - entry.due_date).days
        entry.late_fine = days_late * entry.DAILY_FINE
    
    entry.save()
    entry.book.available = True
    entry.book.save()
    
    serializer = IssueEntrySerializer(entry)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsStaffOrAdmin])
def reissue_book(request):
    entry = get_object_or_404(
        IssueEntry,
        book_id=request.data.get('book'),
        user_id=request.data.get('user'),
        return_date__isnull=True
    )
    
    if entry.reissue_count >= IssueEntry.MAX_REISSUES:
        return Response(
            {'error': f'Maximum reissues ({IssueEntry.MAX_REISSUES}) reached'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if date.today() > entry.due_date:
        return Response(
            {'error': 'Cannot reissue overdue book'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    entry.reissue_count += 1
    entry.due_date = entry.due_date + timedelta(days=IssueEntry.DUE_DAYS)
    entry.save()
    
    serializer = IssueEntrySerializer(entry)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdmin])
def create_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        # Explicitly create the user using the serializer's create method
        user = CustomUser.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            name=serializer.validated_data['name'],
            role=serializer.validated_data['role']
        )
        # Return user data without password
        response_data = CustomUserSerializer(user).data
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsStaffOrAdmin])
def get_open_issue_entries(request):
    entries = IssueEntry.objects.filter(return_date__isnull=True)
    serializer = IssueEntrySerializer(entries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_book(request):
    query = request.GET.get('q', '')
    available = request.GET.get('available')
    
    if not query:
        return Response({'error': 'Search query is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Search with priority: title > author > genre > abstract
    books = Book.objects.annotate(
        relevance=models.Sum(
            models.Case(
                models.When(title__icontains=query, then=4),  # Highest weight
                models.When(author__icontains=query, then=3),
                models.When(genre__icontains=query, then=2),
                models.When(abstract__icontains=query, then=1),  # Lowest weight
                default=0,
                output_field=models.IntegerField()
            )
        )
    # Filter out books with no matches (relevance > 0)
    ).filter(relevance__gt=0)
    
    # Apply availability filter if specified
    if available is not None:
        is_available = available.lower() == 'true'
        books = books.filter(available=is_available)
    
    books = books.order_by('-relevance', 'title')
    
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffOrAdmin])
def get_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_issue_entry(request, transaction_id):
    try:
        entry = IssueEntry.objects.get(transaction_id=transaction_id)
        # Check if user has permission to view this entry
        if request.user.role not in ['staff', 'admin'] and request.user != entry.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        serializer = IssueEntrySerializer(entry)
        return Response(serializer.data)
    except IssueEntry.DoesNotExist:
        return Response({'error': 'Issue entry not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffOrAdmin])
def get_all_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)
