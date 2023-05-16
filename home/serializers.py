from rest_framework import serializers
from .models import *


class ModelSerializer(serializers.Serializer):
    esm = serializers.CharField()
    famil = serializers.CharField()
    tozih = serializers.CharField()
    
    
    
class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Question
        fields = ('__all__')
        
    def get_answers(self, obj):
        result = obj.question_answers.all()
        
        return AnswerSerializer(instance=result, many=True).data
        
class AnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Answer
        fields = ('__all__')
        
        