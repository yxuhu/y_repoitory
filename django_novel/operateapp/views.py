from django.shortcuts import render, HttpResponse, get_object_or_404, get_list_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from mainapp.models import Novel
from django.contrib import messages
from .models import Collect, Talking, Answer
from .forms import *


# Create your views here.

# 删除我的书架的书籍
def deletecollect(req, cid):
    collect = Collect.objects.filter(id=cid)
    collect.delete()
    return JsonResponse({"state": 1})


# 收藏小说呢

def collect(req, nid):
    # 查找是否有这本小说
    novel = get_object_or_404(Novel, id=nid)
    if novel:
        first = Collect.objects.filter(user=req.user).filter(novel=novel).first()
        if first:
            first.delete()
            return JsonResponse({
                'status': 1,
                'state': 0,
                'info': '删除成功'
            })
        else:
            col = Collect()
            col.user = req.user
            col.novel = novel
            col.save()
            return JsonResponse({
                'status': 1,
                'state': 1,
                'info': '收藏成功'
            })
    else:
        return JsonResponse({
            'status': 0,
            'info': '文章不存在'
        })


# 添加讨论
def addtalking(req, aid):
    if req.method == "POST":
        tf = TalkingForm(data=req.POST)
        if tf.is_valid():
            ins = tf.save(commit=False)
            ins.user = req.user
            ins.novel = get_object_or_404(Novel, id=aid)
            ins.save()
        else:
            for k, v in tf.errors.item:
                messages.error(req, v)
        url = reverse("mainapp:book", args=(aid,))
        url += "#end"
        return redirect(url)
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST"])
    # 添加回复


# 添加回复
def addanswer(req, tid):
    if req.method == "POST":
        t = get_object_or_404(Talking, id=tid)
        af = AnswerForm(data=req.POST)
        if af.is_valid():
            ins = af.save(commit=False)
            ins.talking = t
            ins.user = req.user
            ins.save()
        else:
            for k, v in af.errors.item():
                messages.error(req, v)
        url = reverse("mainapp:book", args=(t.novel.id,))
        return redirect(url)
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST"])
