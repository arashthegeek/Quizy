from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import Signup, Login
from django.contrib.auth import authenticate
from .models import CustomUser as User
import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsJWTCAuthenticated
from .models import *
from .serializers import PromptsSerializer
from rest_framework.exceptions import ValidationError
from .dsapi import quastiontojson
from json import loads

# Create your views here.

class Signupview(View):
    def post(self, request):
        form = Signup(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            reqres = requests.post('http://localhost:8000/api/token/',json={'username':user.username,'password':form.cleaned_data['password']})
            response = JsonResponse(reqres.json())
            response.set_cookie(key='access',value=reqres.json()['access'])
            response.set_cookie(key='refresh',value=reqres.json()['refresh'])
            return response
        else:
            return render(request,'register.html', {'form':form})
    def get(self, request):
        form = Signup()
        return render(request,'register.html', {'form':form})
        
        #TODO:
        #-login view that get information with form and send it to jwt page and return the token
        #-a i forgot my password page (side quest: make a i forgot my username or find my account page)
        #-dashbord page that u can accses with only authorization

class LoginView(View):
    def post(self, request):
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if '@' not in username:
                if authenticate(username=username,password=password) is not None:
                    reqres = requests.post('http://localhost:8000/api/token/', json={'username':username,'password':password})
                    response = JsonResponse(reqres.json())
                    response.set_cookie(key='access',value=reqres.json()['access'])
                    response.set_cookie(key='refresh',value=reqres.json()['refresh'])
                    return response
                else:
                    form.add_error('password','رمز عبور اشتباه است')
            elif '@' in username:
                user = User.objects.get(email=username)
                if authenticate(username=user.username,password=password) is not None:
                    reqres = requests.post('http://localhost:8000/api/token/', json={'username':user.username,'password':password})
                    response = JsonResponse(reqres.json())
                    response.set_cookie(key='access',value=reqres.json()['access'])
                    response.set_cookie(key='refresh',value=reqres.json()['refresh'])
                    return response
                else:
                    form.add_error('password','رمز عبور اشتباه است')
        
        return render(request,'login.html',{'form':form})
    def get(self, request):
        form = Login()
        return render(request,'login.html',{'form':form})
        
#-----------------------

class UserPromptsList(APIView):
    permission_classes = [IsJWTCAuthenticated]
    
    def get(self, request):
        user = request.user
        TestPrompts =  TestPrompt.objects.filter(creator=user)
        serializer = PromptsSerializer(TestPrompts, many=True)
        return Response(serializer.data)

class UserAnsweredExamsList(APIView):
    permission_classes = [IsJWTCAuthenticated]
    
    def get(self, request):
        user = request.user
        
        YNPrompts = TestPrompt.objects.filter(yes_no_questions__answers__user=user)
        FOPrompts = TestPrompt.objects.filter(four_option_questions__answers__user=user)
        
        answered_prompts = (YNPrompts | FOPrompts).distinct()
        serializer = PromptsSerializer(answered_prompts, many=True)
        return Response(serializer.data)

class ExamGenerationAPI(APIView):
    permission_classes = [IsJWTCAuthenticated]
    
    def get(self, request):
        creator = request.user
        category = get_object_or_404(TestCategory, title=request.GET.get('category'))
        prompt_text = request.GET.get('prompt_text')
        if prompt_text is None:
            raise ValidationError('Prompt text cant be none.')
        
        try:
            prompt_type = int(request.GET.get('prompt_type'))
        except:
            raise ValidationError('PromptType has a error.')
        if prompt_type != 1 and prompt_type != 2:
            raise ValidationError('Invalid Input on prompt type.')
        
        try:
            is_public = bool(request.GET.get('ispublic'))
        except:
            raise ValidationError('IsPublic has a error.')
        
        #-------demo
        
        if prompt_type == 1:
            ptype = "چهارگزینه ای"
            json_form = '"{"title": exam title, "questions" : [{"question": text of quastion,"options": {"a":"option_a","b":"option_b","c":"option_c","d":"option_d"},"answer": (a,b,c,d)}]}"'
        elif prompt_type == 2:
            ptype = "صحیح غلط"
            json_form = '"{"title": exam title, "questions" : [{"question": text of quastion,"answer": true or false}]}"'
        else:
            raise ValidationError('Invalid prompttype.')
        ai_prompt = f'"{prompt_text}" از این پرامت که یا موضوع مطلب, کتاب یا خود مطلب یا درس هست سوالات امتحانی {ptype} بساز با سطح متوسط وتعداد تا حد توان اگر مطلب کم آوردی از اینترنت راجب همین موضوع مطلب اضافه نکن و ازت  میخوام به این فرم json باشد و هرچه سریعتر و حداکثر 60 ثانیه طول بکشه و هیچ توضیح اضافه ای نده و فقط کد جیسون بنویس.\t{json_form}'
        json = str(quastiontojson(ai_prompt))
        
        #json proccesing
        data = loads(json)
        print(json)
        title = str(data['title'])
        prompt_object = TestPrompt(creator=creator,category=category,title=title,prompt_text=prompt_text,prompt_type=prompt_type,is_public=is_public)
        prompt_object.save()
        quastions = data['questions']
        if len(quastions) == 0:
            return HttpResponse('Error while generating.')
        
        for quastion_dict in quastions:
            Quastion = quastion_dict['question']
            answer = quastion_dict['answer']
            if prompt_type == 1:
                Options = quastion_dict['options']
                oa = Options['a']
                ob = Options['b']
                oc = Options['c']
                od = Options['d']
                if answer == 'a' or answer == 'A':
                    ao = 1
                elif answer == 'b' or answer == 'B':
                    ao = 2
                elif answer == 'c' or answer == 'C':
                    ao = 3
                elif answer == 'd' or answer == 'D':
                    ao = 4
                else:
                    continue
                quastion_object = FourOptionQuestion(prompt=prompt_object,question_text=Quastion,option_a=oa,option_b=ob,option_c=oc,option_d=od,correct_option=ao)
                quastion_object.save()
            elif prompt_type == 2:
                ao = bool(answer)
                quastion_object = YesNoQuestion(prompt=prompt_object, question_text=Quastion, correct_answer=ao)
                quastion_object.save()
        return redirect('/userpromptslist/')
