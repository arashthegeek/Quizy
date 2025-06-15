from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class test_category(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    category = models.CharField(max_length=25)

class test_prompt(models.Model):
    category = models.ForeignKey(test_category, on_delete=CASCADE)
    prompt_text = models.CharField(max_length=2048)
    type_of_prompt = models.IntegerField() #1 for 4option, 2 for yes/no
    is_public = models.BooleanField()
    Date = models.DateField()

class test_4option(models.Model):
    prompt = models.ForeignKey(test_prompt, on_delete=CASCADE)
    question = models.CharField(max_length=50)
    option_a = models.CharField(max_length=30)
    option_b = models.CharField(max_length=30)
    option_c = models.CharField(max_length=30)
    option_d = models.CharField(max_length=30)
    correct_option = models.IntegerField() #1 for a, 2 for b,..., 4 for c

class test_yes_no(models.Model):
    prompt = models.ForeignKey(test_prompt, on_delete=CASCADE)
    question = models.CharField(max_length=50)
    correct_option = models.BooleanField()

class test_user_fo_answer(models.Model):
    fouroption = models.ForeignKey(test_4option, on_delete=CASCADE)
    answer = models.IntegerField()
    user = models.ForeignKey(User, on_delete=CASCADE)

class test_user_yn_answer(models.Model):
    yes_no = models.ForeignKey(test_yes_no, on_delete=CASCADE)
    answer = models.BooleanField()
    user = models.ForeignKey(User, on_delete=CASCADE)