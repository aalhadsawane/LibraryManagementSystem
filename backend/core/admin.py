from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, IssueEntry, CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'email', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'name', 'email')
    ordering = ('username',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'available')
    list_filter = ('genre', 'available')
    search_fields = ('title', 'author')

@admin.register(IssueEntry)
class IssueEntryAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'book', 'user', 'issue_date', 'due_date', 'return_date')
    list_filter = ('return_date', 'due_date')
    search_fields = ('book__title', 'user__name')

admin.site.register(CustomUser, CustomUserAdmin)
