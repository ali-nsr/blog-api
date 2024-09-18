from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    custom user manager for creating users and managing them
    """

    def create_user(self, email, phone, password):
        """
        create user with email and password and extra data
        """
        if not email:
            raise ValueError('email must be set')
        if not phone:
            raise ValueError('phone must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone, password):
        """
        create superuser with email and password
        """
        user = self.create_user(email, phone, password)
        user.is_active = True
        user.is_superuser = True
        user.is_verified = True
        user.save()
        return user
