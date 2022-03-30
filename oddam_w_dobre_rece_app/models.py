from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.


class Category(models.Model):
    """
    # 1 Model Category
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Institution(models.Model):
    """
    # 1 Model Institution
    """
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    TYPE_CHOICES = [
        ('1', 'fundacja'),
        ('2', 'organizacja pozarządowa'),
        ('3', 'zbiórka lokalna')
    ]
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='1')
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    """
    # 1 Model Donation
    """
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    adress = models.CharField(max_length=64)
    phone_number = models.IntegerField(default=0)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=64)
    pick_up_date = models.DateField(null=True)
    pick_up_time = models.TimeField(null=True)
    pick_up_comment = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
