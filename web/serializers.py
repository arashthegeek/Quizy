from rest_framework import serializers
from .models import TestPrompt

class PromptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestPrompt
        fields = ['id','title','category','created_at']
