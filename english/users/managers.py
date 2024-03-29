from django.contrib.auth.models import UserManager
from django.db.models import Manager


class CustomUserManager(UserManager):
    use_in_migrations = True

    def create_superuser(
        self, username, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("first_name", "admin")
        extra_fields.setdefault("last_name", "admin")
        extra_fields.setdefault("birth_date", "1990-01-01")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class StudentsManager(Manager):
    """Returns only users without admin rights (i.e. students)."""
    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=False,
                                             is_staff=False)
