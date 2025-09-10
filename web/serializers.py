from rest_framework import serializers
from .models import TestPrompt, FourOptionQuestion

class PromptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestPrompt
        fields = ['id','title','category','created_at']

class QuastionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    QuastionType = serializers.SerializerMethodField()
    question_text = serializers.CharField()
    Options = serializers.SerializerMethodField()
    correct_answer = serializers.SerializerMethodField()
    
    def get_QuastionType(self, obj):
        return self.context.get('quastion_type')
    
    def get_Options(self, obj):
        if isinstance(obj, FourOptionQuestion):
            return {'A': obj.option_a,'B': obj.option_b,'C': obj.option_c,'D': obj.option_d}
        return None
    
    def get_correct_answer(self, obj):
        if isinstance(obj, FourOptionQuestion):
            return str(obj.correct_option)
        return str(obj.correct_answer)
