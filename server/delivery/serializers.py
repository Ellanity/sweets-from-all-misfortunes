from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *


class CourierGetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Courier
        fields = ["courier_id", "courier_type", "regions", "working_hours", "rating", "earnings"]


class CourierPostSerializerRequest(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Courier
        fields = ["courier_type", "regions", "working_hours"]

    def is_valid(self, raise_exception=True):
        if hasattr(self, "initial_data"):
            extra_fields = set(self.initial_data.keys()) - set(self.fields.keys())
            if extra_fields:
                raise ValidationError("Extra fields %s in payload" % extra_fields)
        return super(CourierPostSerializerRequest, self).is_valid(raise_exception)


class CourierPostSerializerResponse(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Courier
        fields = ["courier_id", "courier_type", "regions", "working_hours"]

    def is_valid(self, raise_exception=True):
        check_fields(self)
        return super(CourierPostSerializerResponse, self).is_valid(raise_exception)


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ["courier_id", "order_id", "weight", "region", "delivery_hours", "complete_time"]


class OrderCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ["order_id", "weight", "region", "delivery_hours"]

    def is_valid(self, raise_exception=True):
        check_fields(self)
        return super(OrderCreateSerializer, self).is_valid(raise_exception)


class CourierIdSerializer(serializers.HyperlinkedModelSerializer):
    courier_id = serializers.IntegerField(required=True)

    class Meta:
        model = Courier
        fields = ["courier_id"]

    def is_valid(self, raise_exception=True):
        check_fields(self)
        return super(CourierIdSerializer, self).is_valid(raise_exception)


class OrdersCompleteSerializer(serializers.HyperlinkedModelSerializer):
    courier_id = serializers.IntegerField(required=True)
    order_id = serializers.IntegerField(required=True)
    complete_time = serializers.CharField(required=True)

    class Meta:
        model = OrderCompleted
        fields = ["order_id", "courier_id", "complete_time"]

    def is_valid(self, raise_exception=True):
        check_fields(self)
        return super(OrdersCompleteSerializer, self).is_valid(raise_exception)


class DataSerializer(serializers.Serializer):
    data = serializers.ListField(default=[])

    def is_valid(self, raise_exception=True):
        extra_fields = set(self.initial_data.keys()) - set(self.fields.keys())
        if extra_fields:
            raise ValidationError("Extra fields %s in payload" % extra_fields)
        return super(DataSerializer, self).is_valid(raise_exception)


def check_fields(obj):
    if hasattr(obj, "initial_data"):
        extra_fields = set(obj.initial_data.keys()) - set(obj.fields.keys())
        no_fields = set(obj.fields.keys()) - set(obj.initial_data.keys())
        if extra_fields or no_fields:
            raise ValidationError("Extra fields %s in payload" % extra_fields)
