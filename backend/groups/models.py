from django.db import models
from accounts.models import User
# Create your models here.


class Study(models.Model):

    category = (
        ('1:1 코칭', '1:1 코칭'),
        ('스터디', '스터디'),
        ('프로젝트', '프로젝트') 
    )

    tech = (
        ("Algorithm", 'Algorithm'),
        ("cs_study", 'cs_study'),
        ("AI", 'AI'),
        ("BigData", 'BigData'),
        ("Game", 'Game'),
        ("Security", 'Security'),
        ("Embedded",'Embedded'),
        ("Mobile",'Mobile'),
        ("Web",'Web')
    )
    
    title = models.CharField(max_length=50)
    tech_tags = models.CharField(choices=tech,max_length=10)
    kind_tags = models.CharField(choices=category,max_length=20)
    study_image = models.URLField(default='')
    subject = models.TextField()
    content = models.TextField()
    member_limit = models.PositiveIntegerField(default=0)
    apply_numbers = models.PositiveIntegerField(default=0) 
    needmoney = models.PositiveIntegerField(default=0)
    deposit = models.PositiveIntegerField(default=0)
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_owner')
    applied = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
   

class Group(models.Model):
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='group_study')
    start = models.DateTimeField()
    end = models.DateTimeField()
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_owner')
    ok = models.BooleanField(default=False)


class Apply(models.Model):

    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='study_apply')
    apply_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apply_user')
    created_at = models.DateTimeField(auto_now_add=True)
