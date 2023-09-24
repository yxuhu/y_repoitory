from django.db import models
from DjangoUeditor.models import UEditorField

# Create your models here.
STATUS = (
    ('0', '已完结'),
    ('1', '连载中')
)


class Tag(models.Model):
    title = models.CharField(max_length=10, verbose_name="标签名")

    def __str__(self):
        return self.title


class Novel(models.Model):
    name = models.CharField(max_length=10, verbose_name="小说名")
    create_time = models.DateField(verbose_name="创建日期", auto_now_add=True)
    author = models.CharField(max_length=10, verbose_name="作者名")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag')
    status = models.CharField(max_length=1, default='0', choices=STATUS)
    img = models.ImageField(verbose_name="封面", upload_to="novels/imgs/")
    info = UEditorField(verbose_name="小说介绍", imagePath="novels/imgs/", filePath="novels/files/")
    counter = models.IntegerField(default=0, verbose_name='点赞数')

    def __str__(self):
        return self.name


class Chapter(models.Model):
    name = models.CharField(max_length=10, verbose_name="章节名")
    create_time = models.DateField(verbose_name="创建日期", auto_now_add=True)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='novel')
    content = UEditorField(verbose_name="文章正文", imagePath="novels/imgs/", filePath="novels/files/")
    num = models.CharField(max_length=10, verbose_name='章节数', default='1')

    def prev(self):
        chapters = self.novel.novel.all()
        # 返回当前文章的索引
        index = list(chapters).index(self)

        return chapters[index-1]

    def next(self):
        chapters = self.novel.novel.all()
        # 返回当前文章的索引
        index = list(chapters).index(self)
        return chapters[index + 1]

    def __str__(self):
        return f'{self.novel}小说中的第{self.num}章节:{self.name}'
