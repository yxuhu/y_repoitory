from django.shortcuts import render, reverse, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import logout as lgo, login as lgi
from . import forms
from .models import CustomUser
from django.http import HttpResponse
from django.contrib import messages
from itsdangerous import TimedJSONWebSignatureSerializer as TJWS
from itsdangerous import SignatureExpired
from django_novel.settings import SECRET_KEY
from django.contrib.auth.decorators import login_required
from operateapp.models import Collect


# Create your views here.

def regist(req):
    if req.method == "POST":
        rf = forms.RegistModelForm(data=req.POST)
        if rf.is_valid():
            email = rf.cleaned_data.get("email")
            password1 = rf.cleaned_data.get("password1")
            password2 = rf.cleaned_data.get("password2")
            username = rf.cleaned_data.get("username")
            user = CustomUser.objects.filter(email=email).first()
            if user:
                messages.error(req, "邮箱已经注册")
                url = reverse("userapp:regist")
                return redirect(url)
            else:
                if password1 != password2:
                    messages.error(req, "两次密码输入不一致")
                else:
                    user = CustomUser.objects.create_user(username=username, password=password1, email=email)
                    user.is_active = False
                    user.save()
                    util = TJWS(SECRET_KEY, expires_in=60 * 60)
                    info = util.dumps({"uid": user.id}).decode("utf8")
                    html_msg = f"<a href='http://127.0.0.1:8000/userapp/active/{info}/'>点我激活</a>  "
                    user.email_user("Online账户激活邮件", "请点击一下连接激活", from_email="yxh17538146236@163.com",
                                    html_message=html_msg)
                    url = reverse("userapp:login")
                    return redirect(url)
        else:
            for k, v in rf.errors.items():
                messages.error(req, v)
            url = reverse("userapp:regist")
            return redirect(url)
    lf = forms.LoginForm()
    rf = forms.RegistModelForm()
    return render(req, "userapp/login_regist.html", locals())


def login(req):
    next = req.GET.get('next')
    print(next)
    if req.method == "POST":
        lf = forms.LoginForm(data=req.POST)
        if lf.is_valid():
            email = lf.cleaned_data.get("email")
            password = lf.cleaned_data.get("password")
            user = CustomUser.objects.filter(email=email).first()
            if user:
                if user.check_password(password):
                    if user.is_active:
                        lgi(req, user)
                        if next:
                            return redirect(next)
                        else:
                            url = reverse("mainapp:index")
                            return redirect(url)

                    else:
                        messages.error(req, "账户尚未激活")

                else:
                    messages.error(req, "密码错误")

            else:
                messages.error(req, "邮箱尚未注册")

        else:
            for k, v in lf.errors.items():
                messages.error(req, v)
        url = reverse("userapp:login")
        url += f'?next={next}'
        return redirect(url)
    lf = forms.LoginForm()
    rf = forms.RegistModelForm()
    page_type = "login"
    return render(req, "userapp/login_regist.html", locals())


# 账号激活
def active(req, userid):
    util = TJWS(SECRET_KEY, expires_in=60 * 60)
    try:
        obj = util.loads(userid)
        user = get_object_or_404(CustomUser, id=obj.get("uid"))
        user.is_active = True
        user.save()
        lgi(req, user)
        url = reverse("mainapp:index")
        return redirect(url)
    except SignatureExpired as e:
        return HttpResponse("激活超时，请重新发送激活链接")


def logout(req):
    lgo(req)
    url = reverse("mainapp:index")
    return redirect(url)


def book_list(req):
    collects = get_list_or_404(Collect, user=req.user)

    return render(req, 'userapp/book_list.html', locals())


# 修改个人信息路由
def change(req):
    if req.method == "POST":
        form_type = req.GET.get("type")
        if form_type == "nickname":
            username = req.POST.get("username")
            user = CustomUser.objects.filter(username=username).first()  # 从数据的里面取数据  找到返回用户 找不到返回空
            if user:
                messages.error(req, "用户名已存在")
            else:
                req.user.username = username
                req.user.save()
            url = reverse("userapp:change")
            url += f"?page_type=nickname"
            return redirect(url)
        elif form_type == "password":
            password = req.POST.get("password")
            newpwd1 = req.POST.get("newpwd1")
            newpwd2 = req.POST.get("newpwd2")

            if req.user.check_password(password):
                if newpwd2 != newpwd1:
                    messages.error(req, "两次输入的密码不一致")
                else:
                    req.user.set_password(newpwd1)
                    req.user.save()
                    lgi(req, req.user)
            else:
                messages.error(req, "原始密码不正确")
            url = reverse("userapp:change")
            url += f"?page_type=password"
            return redirect(url)

        elif form_type == "head":
            if req.method == "POST":
                hf = forms.HeadModelForm(data=req.POST, files=req.FILES)
                if hf.is_valid():
                    req.user.head = hf.cleaned_data.get("head")
                    req.user.save()
                else:
                    for k, v in hf.errors.items():
                        messages.error(req, v)
                url = reverse("userapp:change")
                url += f"?page_type=head"
                return redirect(url)
        else:
            if req.method == 'POST':
                account = req.POST.get('account')
                user = CustomUser.objects.filter(account=account).first()
                if user:
                    messages.error(req, "账号已经存在")
                else:
                    req.user.account = account
                    req.user.save()
                url = reverse("userapp:change")
                url += f"?page_type=account"
                return redirect(url)

    af = forms.AccountModelForm()
    nf = forms.NameModelForm()
    pf = forms.PasswordModelForm()
    hf = forms.HeadModelForm()
    page_type = req.GET.get("page_type", "nickname")
    return render(req, 'userapp/change.html', locals())
