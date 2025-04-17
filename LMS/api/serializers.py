from rest_framework import serializers
from .models import User, Book, BookIssue, Notification
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'user_type', 'password']
        extra_kwargs = {
            'username': {'required': False},
        }
    
    def create(self, validated_data):
        username = validated_data.pop('username', None)
        if not username:
            username = validated_data['email'].split('@')[0]
        
        user = User.objects.create_user(
            username=username,
            **validated_data
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Incorrect credentials")

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookIssueSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source='book.title')
    user_name = serializers.ReadOnlyField(source='user.get_full_name')
    
    class Meta:
        model = BookIssue
        fields = [
            'id', 'book', 'user', 'book_title', 'user_name', 
            'request_date', 'issue_date', 'due_date', 'return_date', 
            'status', 'reissue_count'
        ]
        read_only_fields = ['issue_date', 'due_date', 'return_date', 'reissue_count']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['created_at'] 