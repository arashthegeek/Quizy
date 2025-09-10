from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('userpromptslist/', UserPromptsList.as_view()),
    path('useransweredexamslist/', UserAnsweredExamsList.as_view()),
    path('examcreator/', ExamGenerationAPI.as_view()),
    path('exam/', ExamPageAPI.as_view()),
]
