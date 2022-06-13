from django.db import models


class Thread(models.Model):
    title = models.CharField(max_length=100, blank=True)
    poster = models.CharField(max_length=20, blank=True, default='Анон')
    text = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='thread/images/')
    thumbnail = models.ImageField(upload_to='thread/thumbnails/', blank=True)

    def __str__(self):
        return str(self.id)


class Post(models.Model):
    poster = models.CharField(max_length=20)
    text = models.TextField(max_length=501, blank=False)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post/images/', blank=True, verbose_name='Картинка')
    thumbnail = models.ImageField(upload_to='post/thumbnails/', blank=True)

    def __str__(self):
        return self.text
