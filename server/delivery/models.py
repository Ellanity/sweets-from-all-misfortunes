from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.contrib.postgres.fields import ArrayField
CHOICES = (("foot", "foot"), ("bike", "bike"), ("car", "car"))


class Courier(models.Model):

    courier_id = models.PositiveIntegerField(default=0, unique=True)
    courier_type = models.CharField(max_length=4, choices=CHOICES, blank=True)
    regions = ArrayField(base_field=models.PositiveIntegerField(default=0), default=list, blank=True)
    working_hours = ArrayField(base_field=models.CharField(max_length=11, null=True), default=list, blank=True)

    rating = models.FloatField(default=0, null=True)
    earnings = models.PositiveIntegerField(default=0, null=True)

    have_weight = models.FloatField(default=0)
    last_order_time = models.CharField(max_length=28, default="")

    def __str__(self):
        return str(
            str(self.courier_id) + " " +
            str(self.courier_type) + " " +
            str(self.regions) + " " +
            str(self.working_hours) + " " +
            str(self.rating) + " " +
            str(self.earnings)
        )


class Order(models.Model):

    order_id = models.PositiveIntegerField(default=0, unique=True)
    weight = models.FloatField(default=0, validators=[MinValueValidator(0.01), MaxValueValidator(50.0)])
    region = models.PositiveIntegerField(default=0)
    delivery_hours = ArrayField(models.CharField(max_length=11))

    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, default=None, null=True)

    assign_time = models.CharField(max_length=28, default="")
    courier_coefficient = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(
            str(self.order_id) + " " +
            str(self.weight) + " " +
            str(self.region) + " " +
            str(self.delivery_hours)
        )


class OrderCompleted(models.Model):

    order_id = models.PositiveIntegerField(default=0, unique=True)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, default=None, null=True)

    weight = models.FloatField(default=0)
    region = models.PositiveIntegerField(default=0)

    complete_time = models.CharField(max_length=28, default="")
    assign_time = models.CharField(max_length=28, default="")
    delivery_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(
            str(self.order_id) + " " +
            str(self.courier) + " " +
            str(self.weight) + " " +
            str(self.region) + " " +
            str(self.complete_time) + " " +
            str(self.assign_time) + " " +
            str(self.delivery_time)
        )
