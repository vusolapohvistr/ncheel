from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TestTemplates(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=42)
    description = models.TextField()
    max_possible_result = models.SmallIntegerField()


class TestSchedule(models.Model):
    id_test_template = models.ForeignKey(TestTemplates, on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
# finish this model


class Answers(models.Model):
    email = models.EmailField()
    id_schedule = models.ForeignKey(TestSchedule, on_delete=models.CASCADE)
    date_pass = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=50)
    class_name = models.CharField(max_length=10)
    result = models.SmallIntegerField()
    victim_mac_address = models.CharField(max_length=20, default='empty')
    key = models.CharField(max_length=100, default='dsycfgcrvdxfgggfhjvjy7tgfvb3b483n23123serddsdrq78yhy')
