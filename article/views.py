from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import ArticlePostForm
from django.contrib.auth.models import User
from .models import ArticlePost
import markdown


def article_list(request):
    articles = ArticlePost.objects.all()
    context = {'articles': articles}
    return render(request, 'article/list.html', context)

def article_detail(request,id):
    article = ArticlePost.objects.get(id = id)
    #将markdown语法渲染成HTML样式
    article.body = markdown.markdown(article.body,
                                     extensions = [
                                         #包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    context = {'article': article}
    return render(request, 'article/detail.html', context)

#写文章的视图
def article_create(request):
    #判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data = request.POST)
        # 判断提交的数据是满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit= False)
            # 指定数据库中id=1的用户为作者
            # 如果你进行过删除数据库的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入相应的用户id
            new_article.author = User.objects.get(id = 1)
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect('article:article-list')
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    # 如果用户请求获取数据
    else:
        # 创建一个空的表单实例
        article_post_form = ArticlePostForm()
        # 上下文，传到模版中
        context = {'article_post_form': article_post_form}
        # 进行模版渲染
        return render(request, 'article/create.html', context)

#删文章
def article_delete(request, id):
    # 根据id获取需要删除的文章
    article = ArticlePost.objects.get(id = id)
    # 调用delete方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect('article:article-list')

def article_update(request, id):
    article = ArticlePost.objects.get(id = id)
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data= request.POST)
        if article_post_form.is_valid():
            article.title = request.POST.get('title')
            article.body = request.POST.get('body')
            article.save()
            return redirect('article:article-detail',id = id)
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    else:
        article_post_form = ArticlePostForm()
        context = {'article': article, 'article_post_form': article_post_form}
        return render(request, 'article/update.html', context)