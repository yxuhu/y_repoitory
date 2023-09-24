from django import forms
from captcha.fields import CaptchaField
from django.forms import widgets
from .models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField(widget=widgets.EmailInput(attrs={
        "placeholder": "请输入电子邮箱地址",
        "class": "form-control"
    }))
    password = forms.CharField(widget=widgets.PasswordInput(attrs={
        "placeholder": "请输入密码",
        "class": "form-control"
    }))
    captcha = CaptchaField(label="验证码")


class RegistModelForm(forms.Form):
    # captcha = CaptchaField(label="验证码")
    email = forms.EmailField(widget=widgets.EmailInput(attrs={
        "placeholder": "请输入电子邮箱地址",
        "class": "form-control"
    }))
    username = forms.CharField(widget=widgets.TextInput(attrs={
        "placeholder": "请输入昵称",
        "class": "form-control"
    }))
    password1 = forms.CharField(widget=widgets.PasswordInput(attrs={
        "placeholder": "请输入密码",
        "class": "form-control"
    }))
    password2 = forms.CharField(widget=widgets.PasswordInput(attrs={
        "placeholder": "请确认密码",
        "class": "form-control"
    }))
    captcha = CaptchaField(label="验证码")


class NameModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username"]
        widgets = {
            "username": widgets.TextInput(attrs={
                "class": "form-control",
                "placeholder": "请输入昵称"
            })
        }


class PasswordModelForm(forms.ModelForm):
    newpwd1 = forms.CharField(widget=widgets.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "请输入新密码"
    }))
    newpwd2 = forms.CharField(widget=widgets.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "请确认密码"
    }))

    class Meta:
        model = CustomUser
        fields = ["password"]
        widgets = {
            "password": widgets.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "请输入原始密码"
            })
        }


class HeadModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["head"]
        widgets = {
            "head": widgets.FileInput(attrs={
                "class": "headpic"
            })
        }


class AccountModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["account"]
        widgets = {
            "account": widgets.TextInput(attrs={
                "class": "form-control",
                "placeholder": "请输入账户名"
            })
        }
