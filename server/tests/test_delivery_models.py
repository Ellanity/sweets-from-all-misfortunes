from django.test import TestCase
from delivery.models import *


# Models labels fields tests
class CourierModelLabelsFieldsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Courier.objects.create(courier_id=0,
                               courier_type='foot',
                               regions=[1, 2, 3],
                               working_hours=['10:30-14:30', '15:00-18:00'])

    def test_courier_type(self):
        courier = Courier.objects.get(courier_id=0)
        courier_type = courier._meta.get_field('courier_type').verbose_name
        self.assertEquals(courier_type, 'courier type')

    def test_courier_regions(self):
        courier = Courier.objects.get(courier_id=0)
        courier_regions = courier._meta.get_field('regions').verbose_name
        self.assertEquals(courier_regions, 'regions')

    def test_courier_working_hours(self):
        courier = Courier.objects.get(courier_id=0)
        courier_working_hours = courier._meta.get_field('working_hours').verbose_name
        self.assertEquals(courier_working_hours, 'working hours')


class OrderModelLabelsFieldsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Order.objects.create(order_id=0,
                             weight=3.14,
                             region=3,
                             delivery_hours=['00:20-10:25', '11:30-23:59'])

    def test_order_weight(self):
        order = Order.objects.get(order_id=0)
        order_weight = order._meta.get_field('weight').verbose_name
        self.assertEquals(order_weight, 'weight')

    def test_order_region(self):
        order = Order.objects.get(order_id=0)
        order_region = order._meta.get_field('region').verbose_name
        self.assertEquals(order_region, 'region')

    def test_order_delivery_hours(self):
        order = Order.objects.get(order_id=0)
        order_delivery_hours = order._meta.get_field('delivery_hours').verbose_name
        self.assertEquals(order_delivery_hours, 'delivery hours')


class OrderCompletedModelLabelsFieldsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        OrderCompleted.objects.create(order_id=0,
                                      weight=3.14,
                                      region=3,
                                      assign_time='2021-03-23T10:10:10.10Z',
                                      complete_time='2021-03-23T10:23:49.71Z',
                                      delivery_time=819)

    def test_order_completed_weight(self):
        order_completed = OrderCompleted.objects.get(order_id=0)
        order_completed_weight = order_completed._meta.get_field('weight').verbose_name
        self.assertEquals(order_completed_weight, 'weight')

    def test_order_completed_region(self):
        order_completed = OrderCompleted.objects.get(order_id=0)
        order_completed_region = order_completed._meta.get_field('region').verbose_name
        self.assertEquals(order_completed_region, 'region')

    def test_order_completed_assign_time(self):
        order_completed = OrderCompleted.objects.get(order_id=0)
        order_completed_assign_time = order_completed._meta.get_field('assign_time').verbose_name
        self.assertEquals(order_completed_assign_time, 'assign time')

    def test_order_completed_complete_time(self):
        order_completed = OrderCompleted.objects.get(order_id=0)
        order_completed_complete_time = order_completed._meta.get_field('complete_time').verbose_name
        self.assertEquals(order_completed_complete_time, 'complete time')

    def test_order_completed_delivery_time(self):
        order_completed = OrderCompleted.objects.get(order_id=0)
        order_delivery_time = order_completed._meta.get_field('delivery_time').verbose_name
        self.assertEquals(order_delivery_time, 'delivery time')


# Models initial data tests
class CourierModelInitialValuesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Courier.objects.create(courier_id=0,
                               courier_type='foot',
                               regions=[1, 2, 3],
                               working_hours=['10:30-14:30', '15:00-18:00'])

    def test_courier_type(self):
        courier = Courier.objects.get(courier_id=0)
        courier_type = courier.courier_type
        self.assertEquals(courier_type, 'foot')

    def test_courier_regions(self):
        courier = Courier.objects.get(courier_id=0)
        courier_regions = courier.regions
        self.assertEquals(courier_regions, [1, 2, 3])

    def test_courier_working_hours(self):
        courier = Courier.objects.get(courier_id=0)
        courier_working_hours = courier.working_hours
        self.assertEquals(courier_working_hours, ['10:30-14:30', '15:00-18:00'])


class OrderModelInitialValuesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Order.objects.create(order_id=0,
                             weight=3.14,
                             region=3,
                             delivery_hours=['00:20-10:25', '11:30-23:59'])

    def test_order_weight(self):
        order = Order.objects.get(order_id=0)
        order_weight = order.weight
        self.assertEquals(order_weight, 3.14)

    def test_order_region(self):
        order = Order.objects.get(order_id=0)
        order_region = order.region
        self.assertEquals(order_region, 3)

    def test_order_delivery_hours(self):
        order = Order.objects.get(order_id=0)
        order_delivery_hours = order.delivery_hours
        self.assertEquals(order_delivery_hours, ['00:20-10:25', '11:30-23:59'])


class OrderCompletedModelInitialValuesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        OrderCompleted.objects.create(order_id=0,
                                      weight=3.14,
                                      region=3,
                                      assign_time='2021-03-23T10:10:10.10Z',
                                      complete_time='2021-03-23T10:23:49.71Z',
                                      delivery_time=819)

    def test_order_completed_weight(self):
        order_completed = OrderCompleted.objects.get(order_id=0)
        order_completed_weight = order_completed.weight
        self.assertEquals(order_completed_weight, 3.14)

    def test_order_completed_region(self):
        order_completed = OrderCompleted.objects.get(order_id=0)
        order_completed_region = order_completed.region
        self.assertEquals(order_completed_region, 3)

    def test_order_completed_assign_time(self):
        order_completed = OrderCompleted.objects.get(order_id=0)
        order_completed_assign_time = order_completed.assign_time
        self.assertEquals(order_completed_assign_time, '2021-03-23T10:10:10.10Z')

    def test_order_completed_complete_time(self):
        order_completed = OrderCompleted.objects.get(order_id=0)
        order_completed_complete_time = order_completed.complete_time
        self.assertEquals(order_completed_complete_time, '2021-03-23T10:23:49.71Z')

    def test_order_completed_delivery_time(self):
        order_completed = OrderCompleted.objects.get(order_id=0)
        order_delivery_time = order_completed.delivery_time
        self.assertEquals(order_delivery_time, 819)
