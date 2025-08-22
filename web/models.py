from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    role_choices = [('admin', 'Admin'), ('user', 'User')]
    role = models.CharField(max_length=10, choices=role_choices, default='user')

    preferred_categories = models.ManyToManyField('TestCategory', blank=True, related_name='preferred_users')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username



class TestCategory(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    superior = models.BooleanField()

    def __str__(self):
        return self.title



class TestPrompt(models.Model):
    class PromptType(models.IntegerChoices):
        FOUR_OPTION = 1, "Four Option"
        YES_NO = 2, "Yes / No"

    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_prompts')
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, related_name='prompts')
    title = models.CharField(max_length=25, blank=True)
    prompt_text = models.CharField(max_length=2048)
    prompt_type = models.IntegerField(choices=PromptType.choices) #1 for 4option, 2 for yes/no
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    share_key = models.CharField(max_length=12, unique=True, null=True, blank=True)
    
    def generate_unique_share_key(self):
        while True:
            import secrets
            import string
            key = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(12))
            if not TestPrompt.objects.filter(share_key=key).exist():
                self.share_key = key
                break
    
    def __str__(self):
        return f"{self.title} - {self.prompt_text[:30]}..."



class FourOptionQuestion(models.Model):
    prompt = models.ForeignKey(TestPrompt, on_delete=models.CASCADE, related_name='four_option_questions')
    question_text = models.CharField(max_length=256)
    option_a = models.CharField(max_length=128)
    option_b = models.CharField(max_length=128)
    option_c = models.CharField(max_length=128)
    option_d = models.CharField(max_length=128)

    class CorrectOption(models.IntegerChoices):
        A = 1
        B = 2
        C = 3
        D = 4

    correct_option = models.IntegerField(choices=CorrectOption.choices)

    def __str__(self):
        return self.question_text



class YesNoQuestion(models.Model):
    prompt = models.ForeignKey(TestPrompt, on_delete=models.CASCADE, related_name='yes_no_questions')
    question_text = models.CharField(max_length=256)
    correct_answer = models.BooleanField()

    def __str__(self):
        return self.question_text



class UserFourOptionAnswer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='four_option_answers')
    question = models.ForeignKey(FourOptionQuestion, on_delete=models.CASCADE, related_name='answers')
    selected_option = models.IntegerField(choices=FourOptionQuestion.CorrectOption.choices)
    answered_at = models.DateTimeField(auto_now_add=True)


class UserYesNoAnswer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='yes_no_answers')
    question = models.ForeignKey(YesNoQuestion, on_delete=models.CASCADE, related_name='answers')
    selected_answer = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)


class TestExamReport(models.Model):
    exam = models.ForeignKey(TestPrompt, on_delete=models.CASCADE, related_name='reports')
    report_text = models.TextField()
    created_at = models.DateField(auto_now_add=True)


class TestCategoryReport(models.Model):
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, related_name='reports')
    report_text = models.TextField()
    created_at = models.DateField(auto_now_add=True)
