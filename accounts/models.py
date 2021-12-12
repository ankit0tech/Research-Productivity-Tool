from django.db import models
from django.contrib.auth.models import User
from department.models import Department
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    department = models.ForeignKey(Department, related_name='students', on_delete=models.CASCADE)
    course = models.CharField(max_length=50)
    year = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=8),MinValueValidator(limit_value=1)])
    description = models.TextField(max_length=250)

    def save(self, *args, **kwargs):
        self.username = self.user.username
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username



