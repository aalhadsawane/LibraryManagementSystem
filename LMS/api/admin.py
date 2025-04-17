from django.contrib import admin
from .models import User, Book, BookIssue, Notification

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type')
    list_filter = ('user_type',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publication_date', 'available_copies', 'total_copies')
    list_filter = ('publication_date',)
    search_fields = ('title', 'author', 'isbn')
    ordering = ('title',)

class BookIssueAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'status', 'issue_date', 'due_date', 'return_date')
    list_filter = ('status',)
    search_fields = ('book__title', 'user__email')
    date_hierarchy = 'request_date'

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read', 'notification_type')
    list_filter = ('is_read', 'notification_type')
    search_fields = ('user__email', 'message')
    date_hierarchy = 'created_at'

admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookIssue, BookIssueAdmin)
admin.site.register(Notification, NotificationAdmin)
