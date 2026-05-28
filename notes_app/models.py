from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    # FLAW 3: A02 Cryptographic Failures - password stored in plaintext
    # FIX: Use Django's built-in User model which hashes passwords automatically
    # from django.contrib.auth.models import User
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title