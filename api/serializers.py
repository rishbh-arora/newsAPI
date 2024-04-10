from .models import *
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Comments
        fields = "__all__"

class NewsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, source='fk_news')

    class Meta:
        model = News    
        fields = '__all__'

class BookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmarks
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password',)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    bookmarks = BookmarkSerializer(many=True, read_only=True, source='fk_bookmarks')
    comments = CommentSerializer(many=True, read_only=True, source='fk_comments')

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined', 'karma', 'gender', 'pno', 'comments', 'bookmarks']
