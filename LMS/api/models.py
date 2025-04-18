from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'ADMIN')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('MEMBER', 'Member'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin'),
    )
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='MEMBER')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"
    
    class Meta:
        permissions = [
            ("can_view_books", "Can view books"),
            ("can_request_books", "Can request books"),
            ("can_issue_books", "Can issue books"),
            ("can_manage_users", "Can manage users"),
        ]

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    genre = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    @property
    def is_available(self):
        return self.available_copies > 0

class BookIssue(models.Model):
    STATUS_CHOICES = (
        ('REQUESTED', 'Requested'),
        ('ISSUED', 'Issued'),
        ('RETURNED', 'Returned'),
        ('REJECTED', 'Rejected'),
        ('OVERDUE', 'Overdue'),
    )
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_issues')
    request_date = models.DateTimeField(auto_now_add=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='REQUESTED')
    reissue_count = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['-request_date']
    
    def __str__(self):
        return f"{self.book.title} - {self.user.get_full_name()} ({self.status})"
    
    def issue_book(self, issued_by):
        if self.book.available_copies <= 0:
            raise ValueError("No copies available for issue")
        
        self.issue_date = timezone.now()
        self.due_date = timezone.now() + timedelta(days=14)  # 2 weeks by default
        self.status = 'ISSUED'
        self.save()
        
        # Update available copies
        self.book.available_copies -= 1
        self.book.save()
        
        return True
    
    def return_book(self):
        if self.status != 'ISSUED' and self.status != 'OVERDUE':
            raise ValueError("Book not issued or already returned")
        
        self.return_date = timezone.now()
        self.status = 'RETURNED'
        self.save()
        
        # Update available copies
        self.book.available_copies += 1
        self.book.save()
        
        return True
    
    def reissue_book(self):
        if self.status != 'ISSUED' and self.status != 'OVERDUE':
            raise ValueError("Book not issued or already returned")
        
        if self.reissue_count >= 3:
            raise ValueError("Maximum reissue limit reached")
        
        self.due_date = self.due_date + timedelta(days=7)  # Extend by 1 week
        self.reissue_count += 1
        self.save()
        
        return True
    
    def check_if_overdue(self):
        if self.status == 'ISSUED' and self.due_date and timezone.now() > self.due_date:
            self.status = 'OVERDUE'
            self.save()
            return True
        return False

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('ISSUE_REQUEST', 'Issue Request'),
        ('ISSUED', 'Issued'),
        ('RETURNED', 'Returned'),
        ('OVERDUE', 'Overdue'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=15, choices=NOTIFICATION_TYPES)
    book_issue = models.ForeignKey(BookIssue, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.notification_type} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
