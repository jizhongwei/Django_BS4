from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from PIL import Image

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
    avatar = models.ImageField(upload_to= 'article/%Y%m%d/', blank=True)

    # avatar = ProcessedImageField(
    #     upload_to= 'article/%Y%m%d',
    #     processors= [ResizeToFit(width= 400)],
    #     format = 'JPEG',
    #     options= {'quality': 100}.
    # )

    column = models.ForeignKey(
        ArticleColumn,
        null= True,
        blank= True,
        on_delete= models.CASCADE,
        related_name= 'article',
    )
    tags = TaggableManager(blank= True)

    class Meta:
        ordering = ('-created',)

    # 方法__str__定义当调用对象的str（）方法时的返回内容
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article-detail', args=[self.id,])

    def save(self, *args, **kwargs):
        article = super(ArticlePost, self).save(*args, **kwargs)
        if self.avatar and not kwargs.get('update_fields'):
            img = Image.open(self.avatar)
            (x, y) = img.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resize_img = img.resize((new_x, new_y), Image.ANTIALIAS)
            resize_img.save(self.avatar.path)

        return article