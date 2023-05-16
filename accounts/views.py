from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status


class UserReisterView(APIView):
    serializer = UserRegisterSerializer
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'accounts/register.html'
    
    
    def get(self, request):
        srz = self.serializer()
        return Response(srz.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        srz = self.serializer(data=request.POST)
        if srz.is_valid():
            srz.create(srz.validated_data)
            return Response(srz.data, status=status.HTTP_200_OK)
        return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    serializer = UserLoginSerializer
    
    def get(self, request):
        srz = self.serializer()
        return Response(srz.data)

    def post(self, request):
        srz = self.serializer(data=request.POST)
        
        if srz.is_valid():
            vd = srz.validated_data
            user = authenticate(
                request, username=vd['username'], password=vd['password'])
            if user is not None:
                login(request, user)
                Response(srz.data, status = status.HTTP_200_OK)

        return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        logout(request)

        return Response(status = status.HTTP_200_OK)
    
    
    
class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_pro = ProfileSerializer


    def get(self, request, id):
        is_followig = False
        user = User.objects.get(id=id)
        srz = self.serializer_pro(instance=user)
        
        relation = Relation.objects.filter(from_user = request.user, to_user=user)
        if relation.exists():
            is_followig = True
        
        srz_data = srz.data  
        srz_data['is_following'] = is_followig

        return Response(srz_data, status=status.HTTP_200_OK)
    
    def post(self, request, id):
        form = self.form_class(request.POST)


class UserResetPassword(APIView):
    serializer = PasswordResetSerializer
    
    def get(self, request):
        user = request.user
        srz = self.serializer()
        
        return Response(srz.data, status=status.HTTP_200_OK)
    
    def put(self, requset):
        user = requset.user
        srz = self.serializer(data=requset.data)
        if srz.is_valid():
            user.set_password(srz.data.get('new_password'))
            user.save()
            return Response(data={'message':'ok'}, status=status.HTTP_200_OK)
        return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
    
    
class UserFollowView(APIView):
    
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relatin = Relation.objects.filter(from_user=request.user, to_user=user)
        if relatin.exists():
            return Response({'message':'you already followed this user.'},status=status.HTTP_400_BAD_REQUEST)
            
        Relation(from_user=request.user, to_user=user).save()
        return Response(data={'user_id':user_id ,'message':'you followed this user.'} ,status=status.HTTP_200_OK)

        
        
class UserUnfollowView(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relatin = Relation.objects.filter(from_user=request.user, to_user=user)
        if relatin.exists():
            relatin.delete()
            return Response({'message':'user unfollowed.'}, status=status.HTTP_200_OK)
            
        return Response(status=status.HTTP_400_BAD_REQUEST)

        
class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = ProfileEditSerializer
    
    def get(self, request):
        srz = self.serializer(instance=request.user.profile)
        
        return Response(srz.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        srz = self.serializer(data=request.POST)
        if srz.is_valid():
            srz.user = request.user
            srz.save()
            # request.user.email = srz.validated_data['email']
            # request.user.is_verified = True
            # request.user.is_active = True  
            # request.user.save()
            # messages(request, 'your profile saved successfully !!')
            Response(srz.data, status=status.HTTP_200_OK)
        return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)
            
        
        

