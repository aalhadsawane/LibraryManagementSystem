from datetime import date
from rest_framework import serializers
from .models import Book, IssueEntry, CustomUser


### NOTE: if a field is a foreign key the pk of that key is returned by the serialiser.

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'role', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            role=validated_data['role']
        )
        return user

class IssueEntrySerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    validator_name = serializers.CharField(source='validator.name', read_only=True)
    late_fine=serializers.SerializerMethodField(source='get_late_fine')

    class Meta:
        model = IssueEntry
        fields = ('transaction_id', 'book', 'book_title', 'user', 'user_name', 
                 'validator', 'validator_name', 'reissue_count', 'issue_date', 
                 'due_date', 'return_date', 'late_fine', 'damage_fine') 
        
    def get_late_fine(self, obj):
        DAILY_FINE=10
        if obj.due_date >= date.today() or (obj.return_date and obj.return_date <= obj.due_date):
            return 0
        end_date = obj.return_date if obj.return_date else date.today()
        days_late = (end_date - obj.due_date).days
        return days_late * DAILY_FINE