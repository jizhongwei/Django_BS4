from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import ArticlePostForm
from django.contrib.auth.models import User
from .models import ArticlePost, ArticleColumn
from comment.models import Comment
from comment.forms import CommentForm
import markdown


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')
    article_list = ArticlePost.objects.all()

    if search:
        article_list = ArticlePost.objects.filter(
            Q(title__icontains= search) | Q(body__icontains= search)
        )
    else:
        search = ''

    if column is not None and column.isdigit():
        article_list = article_list.filter(column= column)
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in = [tag])
    if order == 'views':
        article_list = article_list.order_by('-views')

    paginator = Paginator(article_list, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {'articles': articles,
               'order': order,
               'search': search,
               'column': column,
               'tag': tag,
               }
    return render(request, 'article/list.html', context)

def article_detail(request,id):
    article = ArticlePost.objects.get(id = id)
    article.views += 1
    article.save(update_fields= ['views',])
    #将markdown语法渲染成HTML样式
    # article.body = markdown.markdown(article.body,
    #                                  extensions = [
    #                                      #包含 缩写、表格等常用扩展
    #                                      'markdown.extensions.extra',
    #                                      # 语法高亮扩展
    #                                      'markdown.extensions.codehilite',
    #                                      'markdown.extensions.toc',
    #                                  ])
    md = markdown.Markdown(
        extensions= [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    comments = Comment.objects.filter(article = id)
    comment_form = CommentForm()
    article.body = md.convert(article.body)
    context = {'article': article,
               'toc': md.toc,
               'comments': comments,
               'comment_form': comment_form
               }
    return render(request, 'article/detail.html', context)

#写文章的视图
@login_required(login_url= '/userprofile/login/')
def article_create(request):
    #判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit= False)
            # 指定数据库中id=1的用户为作者
            # 如果你进行过删除数据库的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入相应的用户id
            # new_article.author = User.objects.get(id = 1)
            new_article.author = User.objects.get(id = request.user.id)
            if request.POST.get('column') != 'none':
                new_article.column = ArticleColumn.objects.get(id = request.POST.get('column'))
            # 将新文章保存到数据库中
            new_article.save()
            # 保存tags的多对多关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect('article:article-list')
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    # 如果用户请求获取数据
    else:
        # 创建一个空的表单实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 上下文，传到模版中
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 进行模版渲染
        return render(request, 'article/create.html', context)

#删文章
@login_required(login_url= '/userproflie/login/')
def article_delete(request, id):
    # 根据id获取需要删除的文章
    article = ArticlePost.objects.get(id = id)
    # 调用delete方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect('article:article-list')

#要求用户必须登录才能更新文章
@login_required(login_url= '/userprofile/login/')
def article_update(request, id):
    article = ArticlePost.objects.get(id = id)

    if request.user != article.author:
        return HttpResponse("抱歉，您无权修改这篇文章。")
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data= request.POST)
        if article_post_form.is_valid():
            article.title = request.POST.get('title')
            article.body = request.POST.get('body')
            if request.POST.get('column') != 'none':
                article.column = ArticleColumn.objects.get(id = request.POST.get('column'))
            else:
                article.column = None
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            if request.POST.get('tags').strip():
                article.tags.add(*request.POST.get('tags').strip().split(','))
                # article.tags.set(*request.POST.get('tags').split(','), clear = True)
            article.save()
            return redirect('article:article-detail',id = id)
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {'article': article,
                   'article_post_form': article_post_form,
                   'columns': columns,
                   }
        return render(request, 'article/update.html', context)

class ContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = 'views'
        return context