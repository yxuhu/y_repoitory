from django.db import models
from userapp.models import CustomUser
from mainapp.models import Novel
from DjangoUeditor.models import UEditorField

# Create your models here.

STATE = (
    (0, "待审核"),
    (1, "已通过"),
    (2, "未通过"),
)


class BaseOperate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)

    class Meta:
        abstract = True


# 收藏书架部分
class Collect(BaseOperate):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("novel", "user")

    def __str__(self):
        return self.user.username + "的收藏" + self.novel.name


# 评论
class Talking(BaseOperate):
    content = UEditorField(verbose_name="评论的内容", toolbars="mini", width="100%", imagePath="questions/imags/",
                           filePath="questions/files/")
    state = models.IntegerField(verbose_name="审核状态", choices=STATE, default=0)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return self.novel + '的评论' + self.content


class Answer(BaseOperate):
    content = UEditorField(verbose_name="回复正文", toolbars="mini", imagePath="article/imags/",
                           filePath="article/files/")
    talking = models.ForeignKey(Talking, on_delete=models.CASCADE, related_name="answers")
    state = models.IntegerField(verbose_name="审核状态", choices=STATE, default=0)

    def __str__(self):
        return self.talking.title + "回复"
