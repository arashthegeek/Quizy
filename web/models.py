from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models import CASCADE


# Create your models here.
class Custom_User(AbstractUser):
    nickname = models.CharField(max_length=15)
    bio = models.TextField(blank=True)
    PreferdCategories = models.ManyToManyField('TestCategory', blank=True)
    isVerifeid = models.BooleanField(default=False)
    
    def __str__(self):
        return "{self.nickname}"

User = get_user_model()

class TestCategory(models.Model):
    Category = models.CharField(max_length=25)
    
    def __str__(self):
        return "{self.Category}"

class TestPrompt(models.Model):
    User = User
    Category = models.ForeignKey(TestCategory, on_delete=CASCADE)
    PromptText = models.CharField(max_length=2048)
    TypeofPrompt = models.IntegerField() #1 for 4option, 2 for yes/no
    isPublic = models.BooleanField(default=False)
    Date = models.DateField()

class FourOptionTest(models.Model):
    Prompt = models.ForeignKey(TestPrompt, on_delete=CASCADE)
    Question = models.CharField(max_length=50)
    option_a = models.CharField(max_length=30)
    option_b = models.CharField(max_length=30)
    option_c = models.CharField(max_length=30)
    option_d = models.CharField(max_length=30)
    CorrectOption = models.IntegerField() #1 for a, 2 for b,..., 4 for c

class YesNoTest(models.Model):
    Prompt = models.ForeignKey(TestPrompt, on_delete=CASCADE)
    Question = models.CharField(max_length=50)
    CorrectOption = models.BooleanField()

class UserFourOptionTestAnswer(models.Model):
    FourOption = models.ForeignKey(FourOptionTest, on_delete=CASCADE)
    Answer = models.IntegerField()
    User = models.ForeignKey(User, on_delete=CASCADE)

class UserYesNoTestAnswer(models.Model):
    YesNo = models.ForeignKey(YesNoTest, on_delete=CASCADE)
    Answer = models.BooleanField()
    User = models.ForeignKey(User, on_delete=CASCADE)
    
class TestExamReport(models.Model):
    Exam = models.ForeignKey(TestPrompt, on_delete=CASCADE)
    Report = models.TextField()
    Date = models.DateField()

class TestCategoryReport(models.Model):
    Category = models.ForeignKey(TestCategory, on_delete=CASCADE)
    Report = models.TextField()
    Date = models.DateField()