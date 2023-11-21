from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        try:
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    profile_photo = models.ImageField(
        upload_to="user_image", max_length=300, null=True, blank=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=12)
    referral_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


# basic details
class UserBasicDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=40)
    fullName = models.CharField(max_length=50)
    d_o_b = models.DateField()
    address_details = models.TextField()
    zip_code = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    REQUIRED_FIELDS = [
        "nationality",
        "company",
        "fullName",
        "d_o_b",
        "address_details",
        "zip_code",
        "state",
        "user",
    ]


# Pan verfication
class PanVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pan_card = models.ImageField(upload_to="user_image", max_length=300)
    pan_no = models.CharField(max_length=10)


# adhar card verification
class AdharCardVerify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adhar_card_front = models.ImageField(upload_to="user_image", max_length=300)
    adhar_card_back = models.ImageField(upload_to="user_image", max_length=300)
    adhar_no = models.CharField(max_length=10)
