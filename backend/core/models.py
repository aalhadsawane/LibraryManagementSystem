from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import timedelta, date

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('member', 'Member'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    # Required for Django Admin
    REQUIRED_FIELDS = ['email', 'name', 'role']

    def __str__(self):
        return f"{self.name} ({self.role})"

    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_staff = True
            self.is_superuser = True
        elif self.role == 'staff':
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    abstract = models.TextField()
    author = models.CharField(max_length=255)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} | {self.title} - {self.author})"

class IssueEntry(models.Model):
    MAX_REISSUES = 2
    DUE_DAYS = 14

    transaction_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='issues')
    validator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='validations')
    reissue_count = models.IntegerField(default=0)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    damage_fine = models.DecimalField(max_digits=10, decimal_places=2, default=0, choices=[(0, '0'), (400, '400')])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'user'],
                condition=models.Q(return_date__isnull=True),
                name='unique_active_entry'
            )
        ]

    def save(self, *args, **kwargs):
        if not self.pk:  # If creating new entry
            self.due_date = date.today() + timedelta(days=self.DUE_DAYS)
        super().save(*args, **kwargs)

    def clean(self):
        if self.validator.role not in ['staff', 'admin']:
            raise ValidationError("Validator must be staff or admin")
        
        if self.reissue_count > self.MAX_REISSUES:
            raise ValidationError(f"Cannot reissue more than {self.MAX_REISSUES} times")

    def __str__(self):
        return f"{self.book.title} - {self.user.name} ({self.issue_date})"
