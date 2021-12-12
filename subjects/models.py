from django.db import models
from django.contrib.auth.models import User
from department.models import Department
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

from .validators import validate_file_extension

class Subject(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    user = models.ForeignKey(User, related_name='subjects', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    department = models.ForeignKey(Department, related_name='subjects', null=True, blank=True,on_delete=models.CASCADE)
    github_url = models.URLField(blank=True)
    document_file = models.FileField(upload_to='profile_pics', blank=True, null=True, validators=[validate_file_extension])


    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse('subjects:details', kwargs={'pk':self.pk})

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    subject = models.ForeignKey(Subject, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    # comment = models.ForeignKey('self', related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['created_at']

    # def get_absolute_url(self):
    #     return reverse('subjects:details', kwargs={'pk': self.subject.pk})

    def __str__(self):
        return self.text
