from django import forms
from . import models
from django.forms import widgets
from DjangoUeditor import widgets as duw


# 添加问题的表单
class TalkingForm(forms.ModelForm):
    class Meta:
        model = models.Talking
        fields = ["content"]
        widgets = {
            "title": widgets.TextInput(attrs={
                "placeholder": "输入问题概述",
                "class": "from-control"
            })
        }


# 添加回答的表单
class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ["content"]
        widgets = {
            "content": duw.UEditorWidget(attrs={
                "width": "100%",
                "height": 300
            })
        }
