from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class movies(models.Model):
    name=models.CharField(max_length=30)
    desc=models.TextField()
    year=models.IntegerField()
    img=models.ImageField('upload_to_pics')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url

class reviews(models.Model):
    movie = models.ForeignKey(movies, on_delete=models.CASCADE)
    message = models.TextField()
    username = models.CharField(max_length=150) 

    def save(self, *args, **kwargs):
        if not self.username: 
            self.username = self.movie.user.username 
        super().save(*args, **kwargs)

@receiver(post_save, sender=reviews)
def add_user_to_review(sender, instance, created, **kwargs):
    if created and not instance.username:  
        instance.username = instance.movie.user.username 
        instance.save()

class reply(models.Model):
    review = models.ForeignKey(reviews, on_delete=models.CASCADE, related_name='replies')
    message = models.TextField()
    username = models.CharField(max_length=150) 

    def save(self, *args, **kwargs):
        if not self.username:  
            self.username = self.review.username 
        super().save(*args, **kwargs)

@receiver(post_save, sender=reply)
def add_user_to_reply(sender, instance, created, **kwargs):
    if created and not instance.username:
        instance.username = instance.review.username 
        instance.save()

class watchlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    movie=models.ForeignKey(movies,on_delete=models.CASCADE)