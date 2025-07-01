from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TestCategory(models.Model):
    User = models.ForeignKey(User, on_delete=CASCADE)
    Category = models.CharField(max_length=25)

class TestPrompt(models.Model):
    Category = models.ForeignKey(test_category, on_delete=CASCADE)
    PromptText = models.CharField(max_length=2048)
    TypeofPrompt = models.IntegerField() #1 for 4option, 2 for yes/no
    isPublic = models.BooleanField()
    Date = models.DateField()

class FourOptionTest(models.Model):
    Prompt = models.ForeignKey(test_prompt, on_delete=CASCADE)
    Question = models.CharField(max_length=50)
    option_a = models.CharField(max_length=30)
    option_b = models.CharField(max_length=30)
    option_c = models.CharField(max_length=30)
    option_d = models.CharField(max_length=30)
    CorrectOption = models.IntegerField() #1 for a, 2 for b,..., 4 for c

class YesNoTest(models.Model):
    Prompt = models.ForeignKey(test_prompt, on_delete=CASCADE)
    Question = models.CharField(max_length=50)
    CorrectOption = models.BooleanField()

class UserFourOptionTestAnswer(models.Model):
    FourOption = models.ForeignKey(test_4option, on_delete=CASCADE)
    Answer = models.IntegerField()
    User = models.ForeignKey(User, on_delete=CASCADE)

class test_user_yn_answer(models.Model):
    yes_no = models.ForeignKey(test_yes_no, on_delete=CASCADE)
    answer = models.BooleanField()
    user = models.ForeignKey(User, on_delete=CASCADE)
    
class TestExamReport(models.Model):
    Exam = models.ForeignKey(Exam, on_delete=CASCADE)
    Report = models.TextField()
    Date = models.DateField()

class TestCategoryReport(models.Model):
    Category = models.ForeignKey(test_category, on_delete=CASCADE)
    Report = models.TextField()
    Date = models.DateField()