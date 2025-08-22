from django import forms
from .models import CustomUser as User

class Signup(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="password")
    confrim_password = forms.CharField(widget=forms.PasswordInput, label="confrim password")
    class Meta():
        model = User
        fields = ('username','password','email')
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confrim_password = cleaned_data.get('confrim_password')
        
        if '@' in cleaned_data.get('username'):
            raise forms.ValidationError("نام کاربری حاوی '@' است")
        
        if password == "" or confrim_password == "" or password != confrim_password:
            raise forms.ValidationError('رمز عبور ها یکسان نیستند')
        
        #if User.objects.filter(username=cleaned_data.get('username')).exists() or User.objects.filter(email=cleaned_data.get('email')).exists():
        #    raise forms.ValidationError('نام کاربری یا ایمیل از قبل استفاده شده است')
        
        return cleaned_data

class Login(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="username or email")
    password = forms.CharField(widget=forms.PasswordInput, label="password")
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        if password == "":
            raise forms.ValidationError('رمز عبور نامعتبر')
        if not User.objects.filter(username=cleaned_data.get('username')).exists(): #logic gate for if that was email and not username
            if not User.objects.filter(email=cleaned_data.get('username')).exists():
                raise forms.ValidationError('نام کاربری نامعتبر')
            raise forms.ValidationError('نام کاربری نامعتبر')
            
        return cleaned_data