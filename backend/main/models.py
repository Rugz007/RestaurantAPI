from django.db import models
import uuid

class Table(models.Model):
    table_no = models.AutoField(primary_key=True)
    table_capacity = models.IntegerField(default=4)
    is_occupied = models.BooleanField(default=False)
    fk_customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True,blank=True)


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name= models.CharField(max_length=255)
    phone_no = models.IntegerField(unique=True)
    number_of_people = models.IntegerField(default=1)

class Meal(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    time_to_prepare = models.IntegerField(default=10)

class OrderedMeal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fk_customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    fk_meal = models.ForeignKey('Meal', on_delete=models.CASCADE)
    is_served = models.BooleanField(default=False)
    is_ready = models.BooleanField(default=False)
    is_proper = models.BooleanField(default=True)

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fk_customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    total_amount = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
