from django.contrib import admin
from django.urls import path
from .views import LoginView, Signupview, UserPromptsList, UserAnsweredExamsList, ExamGenerationAPI

urlpatterns = [
    path('register/', Signupview.as_view()),
    path('login/', LoginView.as_view()),
    path('userpromptslist/', UserPromptsList.as_view()),
    path('useransweredexamslist/', UserAnsweredExamsList.as_view()),
    path('examcreator/', ExamGenerationAPI.as_view()),
]
