from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length= 100)
    body = models.TextField()
    created = models.DateTimeField(default= timezone.now)
    updated = models.DateTimeField(auto_now= True)

    class Meta:
        ordering = ('-created',)

    # 方法__str__定义当调用对象的str（）方法时的返回内容
    def __str__(self):
        return self.title