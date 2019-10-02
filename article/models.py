from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class ArticleColumn(models.Model):
    title = models.CharField(max_length= 100, blank= True)
    created = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return self.title

class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length= 100)
    body = models.TextField()
    created = models.DateTimeField(default= timezone.now)
    updated = models.DateTimeField(auto_now= True)

    views = models.PositiveIntegerField(default= 0)

    column = models.ForeignKey(
        ArticleColumn,
        null= True,
        blank= True,
        on_delete= models.CASCADE,
        related_name= 'article',
    )

    class Meta:
        ordering = ('-created',)

    # 方法__str__定义当调用对象的str（）方法时的返回内容
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article-detail', args=[self.id,])