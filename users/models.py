from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password = None, company = None,  **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        if not company:
            raise ValueError('The Company field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, company=company, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("user_name", "Administrateur")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('company', 'Ventalis')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(email, password, **extra_fields)

class NewUser(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(_('Email'),unique=True, blank=False, max_length=255)
    first_name = models.CharField(_("Prénom"), max_length=100)
    last_name = models.CharField(_("Nom de famille"), max_length=50)
    company = models.CharField(_("Société"), max_length=100)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company']
    def __str__(self):
        return self.user_name or self.email

class Consultant(NewUser):
    matricule = models.CharField(max_length=10)

    class Meta:
        db_table = "Consultants"
    def get_absolute_url(self):
        return '/consultant/list'



class Customer(NewUser):
    consultant_applied = models.ForeignKey(Consultant, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "Customers"
    def get_absolute_url(self):
        return '/consultant/list'





