import random
import string
from django.db import models
from django.urls import reverse
from django.utils import timezone
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
    user_name = models.CharField(max_length=150, unique=True, )
    email = models.EmailField(_('Email'),unique=True, blank=False, max_length=255)
    first_name = models.CharField(_("Prénom"), max_length=100)
    last_name = models.CharField(_("Nom de famille"), max_length=50)
    company = models.CharField(_("Société"), max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company']
    def __str__(self):
        return self.user_name or self.email

class Consultant(NewUser):

    MATRICULE_LENGTH = 5

    matricule = models.CharField(_("Matricule"),max_length=MATRICULE_LENGTH, unique=True)


    def generate_random_matricule(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=self.MATRICULE_LENGTH))

    def save(self, *args, **kwargs):
        if not self.matricule:
            while True:
                matricule = self.generate_random_matricule()
                if not Consultant.objects.filter(matricule=matricule).exists():
                    self.matricule = matricule
                    break
        super().save(*args, **kwargs)

    class Meta:
        db_table = "Consultants"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_clients_count(self):
        return self.clients.count()

    def get_absolute_url(self):
        return reverse('consultant-home', kwargs={'matricule': self.matricule})
    # def get_absolute_url(self):
    #     return '/consultant/list'

class Customer(NewUser):
    consultant_applied = models.ForeignKey('Consultant', on_delete=models.CASCADE, null=True, related_name='clients')

    class Meta:
        db_table = "Customers"

    @staticmethod
    def assign_consultant_to_client(user):
        if not user.customer:
            consultant = Consultant.objects.annotate(num_clients=models.Count('clients')).order_by(
                'num_clients').first()
            Customer.objects.create(consultant_applied=user, consultant=consultant, company=user.company)
            return consultant
        return None










