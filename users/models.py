import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group

class UserManager(BaseUserManager):
    def create_user(self, email, phone, password):
        if not email:
            raise ValueError("email is required")

        if not phone:
            raise ValueError("phone number is required")
        
        user =self.model(
            email=self.normalize_email(email),
            phone = phone
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, phone, password):
        user=self.create_user(
            email=self.normalize_email(email),
            phone=phone,
            password=password
            )
        user.is_admin= True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)  
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address", max_length=60, unique=True )
    phone = models.CharField(verbose_name="phone", unique=True, max_length=20)
    # password = models.CharField(verbose_name="password")
    date_joined = models.DateTimeField(verbose_name="date joined", editable=False, auto_now_add=True )
    last_login = models.DateTimeField(verbose_name="last login", editable=False, auto_now=True)
    is_admin = models.BooleanField(verbose_name="Staff status",default=False)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(verbose_name="Superuser status",default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS =['phone']
    objects = UserManager()
    
    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
       
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    



    
    


