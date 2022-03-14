from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
from datetime import timedelta, datetime

# Create your models here.


class User(AbstractUser):
    userTypes = (
        ('A', 'Admin'),
        ('G', 'Giver'),
        ('T', 'Taker'),
        ('O', 'Organizer'),
    )
    role = models.CharField(max_length=1, choices=userTypes, default="A")
    address = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=150, blank=True)
    verified_by = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.username


class Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default=random.randint(111111, 999999))
    expiration_date = models.DateTimeField(default=datetime.now()+timedelta(days=1))

    def __str__(self):
        return self.user.username


class VerificationRequest(models.Model):
    statusTypes = (
        ('P', 'Pending'),
        ('V', 'Verified'),
        ('R', 'Rejected'),
    )
    sender = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    organizer = models.ForeignKey(User, related_name="requests", on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default=random.randint(111111, 999999))
    status = models.CharField(max_length=1, choices=statusTypes, default="P")
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.sender.username


class Photo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    datafile = models.ImageField(height_field='height', width_field='width')
    height = models.IntegerField()
    width = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.datafile.name


class Category(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, unique=True)
    icon = models.ForeignKey(Photo, related_name="categories", on_delete=models.SET_NULL, null=True, blank=True)
    brief = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Point(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    images = models.ManyToManyField(Photo, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    brief = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, related_name="points", on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('lat', 'lng')

    def __str__(self):
        return self.name


class Need(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    images = models.ManyToManyField(Photo, blank=True)
    brief = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='needs', on_delete=models.SET_NULL, blank=True, null=True)
    point = models.ForeignKey(Point, related_name='needs', on_delete=models.SET_NULL, blank=True, null=True)
    giver = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Report(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="reports", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sent_reports", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    brief = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Notification(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sent_notifications", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    brief = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


