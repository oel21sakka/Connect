from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField()
    body = models.TextField()
    publish_date = models.DateField(auto_now_add=True)
    publish_time = models.TimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    tags = TaggableManager(blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title','publish_date'],name='uniqueTitle_Publishdate')
        ]
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['body']),
        ]
        ordering = ['-publish_date']
    
    def get_absolute_url(self):
        return reverse('SinglePostView', kwargs={'slug':self.slug, 'publish_date':self.publish_date.strftime('%Y-%m-%d')})
