from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from .models import *
from rest_framework import status

class Home(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home/index.html'
    def get(self, request):
        questions = Question.objects.all()
        srz = QuestionSerializer(instance=questions, many=True)
        return Response({'questions':questions})


class QuestionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        questions = Question.objects.all()
        srz = QuestionSerializer(instance=questions, many=True)
        
        return Response(srz.data, status=status.HTTP_200_OK)
        
class QuestionCreateView(APIView):
    def post(self, request):
        srz = QuestionSerializer(data=request.data)
        if srz.is_valid():
            srz.save()
            return Response(srz.data, status=status.HTTP_201_CREATED)
        return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class QuestionUpdateView(APIView):
    def put(self, request, pk):
        question = Question.objects.get(id=pk)
        srz = QuestionSerializer(instance=question, data=request.data, partial=True)
        if srz.is_valid():
            srz.save()
            return Response(srz.data, status=status.HTTP_200_OK)
        return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuestionDeleteView(APIView):
    def delete(self, request, pk):
        question = Question.objects.get(id=pk)
        question.delete()
        
        return Response({'message':'deleted'}, status=status.HTTP_200_OK)