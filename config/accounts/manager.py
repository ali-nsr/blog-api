from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    custom user manager for creating users and managing them
    """
    def create_user(self, email,  password):
        """
        create user with email and password and extra data
        """
        if not email:
            raise ValueError('the Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        create superuser with email and password
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user
