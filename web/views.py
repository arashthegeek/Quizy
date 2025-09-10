from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
import requests
from json import loads

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .forms import Signup, Login
from .models import CustomUser as User, TestPrompt, TestCategory, FourOptionQuestion, YesNoQuestion
from .permissions import IsJWTCAuthenticated
from .serializers import PromptsSerializer, QuastionSerializer
from .dsapi import *

# -------------------------
# Auth Views
# -------------------------

class SignupView(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name, {'form': Signup()})

    def post(self, request):
        form = Signup(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        token_response = requests.post(
            'http://localhost:8000/api/token/',
            json={'username': user.username, 'password': form.cleaned_data['password']}
        ).json()

        response = JsonResponse(token_response)
        response.set_cookie('access', token_response['access'])
        response.set_cookie('refresh', token_response['refresh'])
        return response


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name, {'form': Login()})

    def post(self, request):
        form = Login(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # Support login by email
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                username = user.username
            except User.DoesNotExist:
                form.add_error('username', 'کاربر با این ایمیل یافت نشد.')
                return render(request, self.template_name, {'form': form})

        if authenticate(username=username, password=password) is None:
            form.add_error('password', 'رمز عبور اشتباه است')
            return render(request, self.template_name, {'form': form})

        token_response = requests.post(
            'http://localhost:8000/api/token/',
            json={'username': username, 'password': password}
        ).json()

        response = JsonResponse(token_response)
        response.set_cookie('access', token_response['access'])
        response.set_cookie('refresh', token_response['refresh'])
        return response


# -------------------------
# API Views
# -------------------------

class UserPromptsList(APIView):
    permission_classes = [IsJWTCAuthenticated]

    def get(self, request):
        prompts = TestPrompt.objects.filter(creator=request.user)
        serializer = PromptsSerializer(prompts, many=True)
        return Response(serializer.data)


class UserAnsweredExamsList(APIView):
    permission_classes = [IsJWTCAuthenticated]

    def get(self, request):
        user = request.user
        yn_prompts = TestPrompt.objects.filter(yes_no_questions__answers__user=user)
        fo_prompts = TestPrompt.objects.filter(four_option_questions__answers__user=user)
        answered_prompts = (yn_prompts | fo_prompts).distinct()
        serializer = PromptsSerializer(answered_prompts, many=True)
        return Response(serializer.data)


class ExamGenerationAPI(APIView):
    permission_classes = [IsJWTCAuthenticated]

    def get(self, request):
        creator = request.user
        category_title = request.GET.get('category')
        prompt_text = request.GET.get('prompt_text')
        prompt_type = request.GET.get('prompt_type')
        is_public = request.GET.get('ispublic', 'False').lower() in ['true', '1']

        if not category_title or not prompt_text or not prompt_type:
            raise ValidationError('پارامترهای لازم ارسال نشده‌اند.')

        category = get_object_or_404(TestCategory, title=category_title)

        try:
            prompt_type = int(prompt_type)
        except ValueError:
            raise ValidationError('نوع سوال نامعتبر است.')

        if prompt_type not in [1, 2]:
            raise ValidationError('نوع سوال باید 1 یا 2 باشد.')

        json_form = {
            1: '"{"title": "exam title", "questions" : [{"question": "text of quastion","options": {"a":"option_a","b":"option_b","c":"option_c","d":"option_d"},"answer": "a,b,c,d"}]}"',
            2: '"{"title": "exam title", "questions" : [{"question": "text of quastion","answer": true,false}]}"',
        }[prompt_type]

        ptype_text = {1: "چهارگزینه ای", 2: "صحیح غلط"}[prompt_type]
        ai_prompt = ai_prompt = f'{prompt_text} با موضوع یا متن داده شده، سوالات امتحانی {ptype_text} بساز با سطح متوسط و تا حد توان تعداد سوال. اگر مطلب کم باشد، از اینترنت مطلب اضافه نکن. خروجی باید دقیقا یک JSON معتبر باشد چون توسط JSON Decoder پردازش می‌شود. هیچ توضیح یا متن اضافی نده و فقط JSON بده. این کار را در کمتر از ۴۰ ثانیه انجام بده. {json_form}'

        a = aichat(ai_prompt).replace('json', '').replace('Copy', '')
        print(a)
        json_data = loads(str(a))

        prompt_object = TestPrompt.objects.create(
            creator=creator,
            category=category,
            title=json_data['title'],
            prompt_text=prompt_text,
            prompt_type=prompt_type,
            is_public=is_public
        )

        for q in json_data.get('questions', []):
            if prompt_type == 1:
                ans_map = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
                quastion_object = FourOptionQuestion(
                    prompt=prompt_object,
                    question_text=q['question'],
                    option_a=q['options']['a'],
                    option_b=q['options']['b'],
                    option_c=q['options']['c'],
                    option_d=q['options']['d'],
                    correct_option=ans_map.get(q['answer'].lower(), 0)
                )
            else:
                quastion_object = YesNoQuestion(
                    prompt=prompt_object,
                    question_text=q['question'],
                    correct_answer=bool(q['answer'])
                )
            quastion_object.save()

        return redirect('/userpromptslist/')

class ExamPageAPI(APIView):
    permission_classes = [IsJWTCAuthenticated]
    def get(self, request):
        try:
            ExamID = int(request.GET.get('ExamID'))
        except:
            raise ValidationError("invalid ID")
        Exam = TestPrompt.objects.get(id=ExamID)
        if Exam.creator == request.user:
            if Exam.prompt_type == 1:
                Quastions = FourOptionQuestion.objects.filter(prompt__id=ExamID)
                serializer = QuastionSerializer(Quastions, many=True)
                return Response(serializer.data)
            elif Exam.prompt_type == 2:
                Quastions = YesNoQuestion.objects.filter(id=ExamID)
                serializer = QuastionSerializer(Quastions, many=True)
                return Response(serializer.data)
