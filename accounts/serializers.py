from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2',)
        
        extra_kwargs = {'password':{'write_only':True}}

        
    def create(self, validated_data):
        del validated_data['password2']
        user = User.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        return user, token
        
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('passwords must match')
        
        return data
    
class UserLoginSerializer(serializers.Serializer):
    
    username = serializers.CharField()
    password = serializers.CharField()
        
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('body', 'slug', 'created', 'updated')
        
        
class ProfileEditSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Profile
        fields = ("__all__")
    

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ('__all__')

class ProfileSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('username','posts', 'profile',)
        
    def get_posts(self, obj):
        result = obj.user_posts.all()
        return PostSerializer(instance=result, many=True).data
    
    def get_profile(self, obj):
        result = obj.profile
        return ProfileEditSerializer(instance=result).data
    
    
class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField()

        
        

