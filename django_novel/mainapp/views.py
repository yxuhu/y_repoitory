from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, reverse, HttpResponse
from .models import Tag, Novel, Chapter
from django.core.paginator import Paginator, Page
from operateapp.models import Collect, Talking, Answer
from operateapp.forms import *


# Create your views here.

def index(req):
    first_novel = get_object_or_404(Novel, tag=1)
    list = get_list_or_404(Novel)
    novel_list = list[:10]
    bottom_list = list[:9]
    imgs = novel_list[:4]
    return render(req, 'index.html', locals())


# 热度部分
# 根据文章的浏览量来排热力榜
def hot(req):
    # 获得路由
    page_num = req.GET.get('page_num', 1)
    # 根据时间的查询书籍
    books = Novel.objects.all().order_by('-counter')
    #  依靠分页器类 将书籍分成每页3个数据
    paginator = Paginator(books, 3)
    # 获得第page_num页的书籍列表
    current_page_books = paginator.get_page(page_num)
    return render(req, 'hot.html', locals())


# 书的详情页
def book(req, bid):
    # 传入讨论的列表
    talkings = Talking.objects.all()
    print(type(talkings))
    # 传入问题表单
    tf = TalkingForm()
    # 传入评论的表单
    af = AnswerForm()
    # 查看这本小说是否本该用户收藏了
    if req.user.is_authenticated:
        has_collect = Collect.objects.filter(novel=get_object_or_404(Novel, id=bid)).filter(user=req.user).exists()
    else:
        has_collect = False
    # 浏览量加一实现
    novel_list = get_list_or_404(Novel)[:7]
    current_novel = get_object_or_404(Novel, id=bid)
    has_last = current_novel.novel.last()
    if has_last:
        current_novel_chapter_content = current_novel.novel.last().content[:552]
    else:
        current_novel_chapter_content = '暂无详情'
    current_novel.counter += 1
    current_novel.save()
    return render(req, 'book.html', locals())


def chapter(req, cid):
    # 当前章节
    chap = get_object_or_404(Chapter, id=cid)
    return render(req, 'chapter.html', locals())
