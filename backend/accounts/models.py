from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('input email')
        if not username: 
            raise ValueError('input username')
        user = self.model(
            email    = self.normalize_email(email),
            username = username 
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email    = email,
            password = password,
            username = username
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email        = models.EmailField('email', max_length=60, unique=True)
    username     = models.CharField(max_length=20, unique=True)
    money        = models.PositiveIntegerField(default="1000000")

    data_joined  = models.DateTimeField('data joined', auto_now_add=True)
    last_login   = models.DateTimeField('last login', auto_now=True)
    is_admin     = models.BooleanField(default=False)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email 
    def get_username(self):
        return self.username
    def get_user_id(self):  
        return self.pk
        
    class Meta:
        verbose_name ="user"
        verbose_name_plural ="users"



class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_user')
    profile_image = models.ImageField(upload_to="%Y/%m/%d")
    img_url = models.URLField(default='')
    message = models.TextField(default='')

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)