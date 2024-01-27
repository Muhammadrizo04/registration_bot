import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from common import validate_phone
from common.models import Region, District, Quarter


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        USER = "user", _("User")
        ADMIN = "admin", _("Admin")

    guid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        null=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    phone_number = models.CharField(
        max_length=12,
        unique=True,
        validators=[validate_phone],
        null=True,
    )
    full_name = models.CharField(max_length=255, null=True)
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, related_name="users"
    )
    district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True, related_name="users"
    )
    quarter = models.ForeignKey(
        Quarter, on_delete=models.SET_NULL, null=True, related_name="users"
    )
    role = models.CharField(
        choices=Role.choices,
        max_length=10,
        null=True,
        blank=True,
    )
    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        if self.phone_number:
            return str(self.phone_number)
        elif self.full_name:
            return str(self.full_name)
        elif self.email:
            return str(self.email)