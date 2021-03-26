from unittest import mock

from django.test import TestCase
from rest_framework.utils import json

from delivery.views import *


class ProcessorCouriersGetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Courier.objects.create(courier_id=0,
                               courier_type="foot",
                               regions=[1, 2, 3],
                               working_hours=["10:30-14:30", "15:00-18:00"],
                               rating=0,
                               earnings=0)

        Courier.objects.create(courier_id=1,
                               courier_type="car",
                               regions=[3, 4, 5, 6, 7],
                               working_hours=["00:30-04:30", "05:00-10:45"],
                               rating=4.3,
                               earnings=50000)

    def test_couriers_id_0_get(self):
        response = self.client.get("/couriers/0")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"courier_id": 0,
                                                         "courier_type": "foot",
                                                         "regions": [1, 2, 3],
                                                         "working_hours": ["10:30-14:30", "15:00-18:00"]})

    def test_couriers_id_1_get(self):
        response = self.client.get("/couriers/1")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"courier_id": 1,
                                                         "courier_type": "car",
                                                         "regions": [3, 4, 5, 6, 7],
                                                         "working_hours": ["00:30-04:30", "05:00-10:45"],
                                                         "rating": 4.3,
                                                         "earnings": 50000})

    def test_couriers_no_id_get(self):
        response = self.client.get("/couriers/2")
        self.assertEquals(response.status_code, 404)


class ProcessorCouriersPatchTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Courier.objects.create(courier_id=0,
                               courier_type="foot",
                               regions=[1, 2, 3],
                               working_hours=["10:30-14:30", "15:00-18:00"],
                               rating=3.9,
                               earnings=77500)

    def test_couriers_id_patch_200_1(self):
        data = json.dumps({"courier_type": "bike", "regions": [2, 3]})
        response = self.client.patch("/couriers/0", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"courier_id": 0,
                                                         "courier_type": "bike",
                                                         "regions": [2, 3],
                                                         "working_hours": ["10:30-14:30", "15:00-18:00"]})

    def test_couriers_id_patch_200_2(self):
        data = json.dumps({"working_hours": ["15:30-16:00", "22:00-23:59", "17:00-17:55"], "regions": [1, 3, 4, 2]})
        response = self.client.patch("/couriers/0", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"courier_id": 0,
                                                         "courier_type": "foot",
                                                         "regions": [1, 3, 4, 2],
                                                         "working_hours": ["15:30-16:00", "22:00-23:59",
                                                                           "17:00-17:55"]})

    # No such field
    def test_couriers_id_patch_400_1(self):
        data = json.dumps({"courier_type": "foot", "rating": 1})
        response = self.client.patch("/couriers/0", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    # Invalid data working_hours
    def test_couriers_id_patch_400_2(self):
        data = json.dumps({"courier_type": "foot", "working_hours": ["1:30-14:30", "15:00-18:00"]})
        response = self.client.patch("/couriers/0", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    # Invalid data working_hours
    def test_couriers_id_patch_400_3(self):
        data = json.dumps({"courier_type": "foot", "working_hours": ["10:30-14:30", "15:00-18:90"]})
        response = self.client.patch("/couriers/0", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    # Invalid data courier_type
    def test_couriers_id_patch_400_4(self):
        data = json.dumps({"courier_type": "none", "working_hours": ["10:30-14:30", "15:00-18:19"]})
        response = self.client.patch("/couriers/0", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    # Invalid data regions
    def test_couriers_id_patch_400_5(self):
        data = json.dumps({"courier_type": "bike", "regions": "it is not array"})
        response = self.client.patch("/couriers/0", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    # Invalid fields
    def test_couriers_id_patch_400_6(self):
        data = json.dumps({"regions": [4, 5], "no_field": "no_field"})
        response = self.client.patch("/couriers/0", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    # Invalid courier_id
    def test_couriers_id_patch_404(self):
        response = self.client.patch("/couriers/1")
        self.assertEquals(response.status_code, 404)


class ProcessorCouriersPostTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_couriers_post_200_1(self):
        data = json.dumps(
            {
                "data": [
                    {
                        "courier_id": 1,
                        "courier_type": "foot",
                        "regions": [1, 12, 22],
                        "working_hours": ["11:35-14:05", "09:00-11:00"]
                    }
                ]
            }
        )
        response = self.client.post("/couriers", data, content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(json.loads(response.content), {"couriers": [{"id": 1}]})

    def test_couriers_post_200_2(self):
        data = json.dumps(
            {
                "data": [
                    {
                        "courier_id": 1,
                        "courier_type": "foot",
                        "regions": [1, 12, 22],
                        "working_hours": ["11:35-14:05", "09:00-11:00"]
                    },
                    {
                        "courier_id": 2,
                        "courier_type": "bike",
                        "regions": [22],
                        "working_hours": ["09:00-18:00"]
                    },
                    {
                        "courier_id": 3,
                        "courier_type": "car",
                        "regions": [12, 22, 23, 33],
                        "working_hours": []
                    }
                ]
            }
        )
        response = self.client.post("/couriers", data, content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(json.loads(response.content), {"couriers": [{"id": 1}, {"id": 2}, {"id": 3}]})

    def test_couriers_post_400_1(self):
        # 1. Everything ok
        # 2. No such field
        # 3. Invalid working_hours
        # 4. Invalid courier_type
        # 5. Invalid regions
        # 6. Id is invalid -> No id in response
        data = json.dumps(
            {
                "data": [
                    {
                        "courier_id": 1,
                        "courier_type": "foot",
                        "regions": [1, 12, 22],
                        "working_hours": ["11:35-14:05", "09:00-11:00"]
                    },
                    {
                        "courier_id": 2,
                        "courier_type": "bike",
                        "regions": [22],
                        "working_hours": ["09:00-18:00"],
                        "no": "no"
                    },
                    {
                        "courier_id": 3,
                        "courier_type": "car",
                        "regions": [12, 22, 23, 33],
                        "working_hours": ["25-34:34-45"]
                    },
                    {
                        "courier_id": 4,
                        "courier_type": "none",
                        "regions": [12, 22, 23, 33],
                        "working_hours": ["11:34-14:45"]
                    },
                    {
                        "courier_id": 5,
                        "courier_type": "foot",
                        "regions": ["12, 22", "23, 33"],
                        "working_hours": ["00:34-23:12"]
                    },
                    {
                        "courier_id": ["courier", "id"],
                        "courier_type": "bike",
                        "regions": [6, 7, 213],
                        "working_hours": ["10:00-12:12", "14:00-20:00"]
                    }
                ]
            }
        )
        response = self.client.post("/couriers", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content), {"validation_error": {
            "couriers": [{"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}]}})

    def test_couriers_post_400_2(self):
        data = json.dumps({"data": "not_list"})
        response = self.client.post("/couriers", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_couriers_post_400_3(self):
        data = json.dumps(
            {
                "data": [
                    {
                        "courier_id": 1,
                        "courier_type": "foot",
                        "regions": [1, 12, 22],
                        "working_hours": ["11:35-14:05", "09:00-11:00"]
                    }
                ],
                "no_field": "no_field"
            }
        )
        response = self.client.post("/couriers", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    """def test_couriers_post_400_4(self):
        data = json.dumps(
            {
                "data": [
                    {
                        "courier_id": 1,
                        "courier_type": "foot",
                        "regions": [1, 12, 22],
                        "working_hours": ["11:35-14:05", "09:00-11:00"]
                    },
                    {
                        "object": {
                            "field_1": [12, 34],
                            "field_2": "incorrect_object"
                        }
                    }
                ]
            }
        )
        response = self.client.post("/couriers", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)"""


class ProcessorOrdersPostTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Order.objects.create(order_id=9,
                             region=2,
                             weight=2.23,
                             delivery_hours=["12:00-13:00"])
        OrderCompleted.objects.create(order_id=10,
                                      region=3,
                                      weight=3.23)

    def test_orders_post_200_1(self):
        data = json.dumps(
            {
                "data": [
                    {
                        "order_id": 1,
                        "weight": 0.23,
                        "region": 12,
                        "delivery_hours": ["08:00-12:00", "12:20-22:00"]
                    }
                ]
            }
        )
        response = self.client.post("/orders", data, content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(json.loads(response.content), {"orders": [{"id": 1}]})

    def test_orders_post_200_2(self):
        data = json.dumps(
            {
                "data": [
                    {
                        "order_id": 1,
                        "weight": 0.23,
                        "region": 12,
                        "delivery_hours": ["09:00-18:00"]
                    },
                    {
                        "order_id": 2,
                        "weight": 15,
                        "region": 1,
                        "delivery_hours": ["09:00-18:00"]
                    },
                    {
                        "order_id": 3,
                        "weight": 0.01,
                        "region": 22,
                        "delivery_hours": ["09:00-12:00", "16:00-21:30"]
                    },
                    {
                        "order_id": 4,
                        "weight": 3.14,
                        "region": 1,
                        "delivery_hours": ["08:00-12:00", "12:20-22:00"]
                    }
                ]
            }
        )
        response = self.client.post("/orders", data, content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(json.loads(response.content), {"orders": [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}]})

    def test_orders_post_400_1(self):
        # 1. Everything ok
        # 2. No such field
        # 3. Invalid weight
        # 4. Invalid region
        # 5. Invalid delivery_hours
        # 6. Invalid delivery_hours
        # 7. Invalid weight
        # 8. Invalid weight
        # 9. Order with such id already exist
        # 10. CompletedOrder with such id already exist
        # 11. Id is invalid -> No id in response
        data = json.dumps(
            {
                "data": [
                    {
                        "order_id": 1,
                        "weight": 0.01,
                        "region": 22,
                        "delivery_hours": ["09:00-12:00", "16:00-21:30"]
                    },
                    {
                        "order_id": 2,
                        "weight": 12.2,
                        "region": 3,
                        "delivery_hours": ["09:00-18:00"],
                        "no_field": "no_field"
                    },
                    {
                        "order_id": 3,
                        "weight": "not_weight",
                        "region": 33,
                        "delivery_hours": ["12:34-21:45"]
                    },
                    {
                        "order_id": 4,
                        "weight": 11.4,
                        "region": [12, 22, 23, 33],
                        "delivery_hours": ["11:34-14:45"]
                    },
                    {
                        "order_id": 5,
                        "weight": 0.4,
                        "region": 14,
                        "delivery_hours": ["00:12-25:12"]
                    },
                    {
                        "order_id": 6,
                        "weight": 49.9,
                        "regions": 2,
                        "delivery_hours": ["0:12-5:00"]
                    },
                    {
                        "order_id": 7,
                        "weight": 0.001,
                        "region": 1,
                        "delivery_hours": ["11:34-12:34", "12:45-21:45"]
                    },
                    {
                        "order_id": 8,
                        "weight": 50.001,
                        "region": 1,
                        "delivery_hours": ["11:34-12:34", "12:45-21:45"]
                    },
                    {
                        "order_id": 9,
                        "weight": 2.23,
                        "region": 2,
                        "delivery_hours": ["12:00-13:00"]
                    },
                    {
                        "order_id": 10,
                        "weight": 3.23,
                        "region": 3,
                        "delivery_hours": ["10:00-13:00"]
                    },
                    {
                        "order_id": ["order", "id"],
                        "weight": 12,
                        "region": 222,
                        "delivery_hours": ["10:00-12:12", "14:00-20:00"]
                    }
                ]
            }
        )
        response = self.client.post("/orders", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content), {"validation_error": {
            "orders": [{"id": 2}, {"id": 3}, {"id": 4}, {"id": 5},
                       {"id": 6}, {"id": 7}, {"id": 8}, {"id": 9}, {"id": 10}]}})

    def test_orders_post_400_2(self):
        data = json.dumps({"data": "not_list"})
        response = self.client.post("/orders", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_orders_post_400_3(self):
        data = json.dumps(
            {
                "data": [
                    {
                        "order_id": 4,
                        "weight": 10,
                        "region": 2.16,
                        "delivery_hours": ["09:00-12:00", "16:00-22:30"]
                    }
                ],
                "no_field": "no_field"
            }
        )
        response = self.client.post("/orders", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)


class ProcessorOrdersAssignPostTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Courier.objects.create(courier_id=1,
                               courier_type="foot",
                               regions=[1, 2, 3],
                               working_hours=["10:30-14:30", "15:00-18:00"],
                               have_weight=10)

        Courier.objects.create(courier_id=2,
                               courier_type="bike",
                               regions=[3, 4, 5, 6, 7],
                               working_hours=["00:30-04:30", "05:00-11:05"],
                               have_weight=15)

        Courier.objects.create(courier_id=3,
                               courier_type="car",
                               regions=[1, 2, 3, 4, 5, 6, 7],
                               working_hours=["00:30-04:30", "05:00-10:45"],
                               have_weight=50)

        Courier.objects.create(courier_id=4,
                               courier_type="foot",
                               regions=[1, 2],
                               working_hours=["00:30-04:30", "19:00-21:45"],
                               have_weight=10)

        Order.objects.create(order_id=1,
                             weight=3,
                             region=1,
                             delivery_hours=["10:00-12:00"])
        Order.objects.create(order_id=2,
                             weight=4,
                             region=2,
                             delivery_hours=["15:00-17:00"])
        Order.objects.create(order_id=3,
                             weight=5,
                             region=3,
                             delivery_hours=["09:00-11:00"])
        Order.objects.create(order_id=4,
                             weight=5,
                             region=3,
                             delivery_hours=["15:20-19:30"])
        Order.objects.create(order_id=5,
                             weight=6,
                             region=3,
                             delivery_hours=["10:00-12:00"])

        Order.objects.create(order_id=6,
                             weight=10,
                             region=4,
                             delivery_hours=["11:00-12:00"])

        Order.objects.create(order_id=7,
                             weight=1,
                             region=5,
                             delivery_hours=["06:00-13:00"])
        Order.objects.create(order_id=8,
                             weight=2,
                             region=6,
                             delivery_hours=["06:00-13:00"])
        Order.objects.create(order_id=9,
                             weight=49,
                             region=4,
                             delivery_hours=["06:00-13:00"])

    @mock.patch('delivery.views.datetime')
    def test_orders_assign_200_1(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime(2021, 3, 29, 12, 00, 00, 00)
        data = json.dumps({"courier_id": 1})
        response = self.client.post("/orders/assign", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"orders": [{"id": 5}, {"id": 2}],
                                                         "assign_time": "2021-03-29T12:00:00.00Z"})

    @mock.patch('delivery.views.datetime')
    def test_orders_assign_200_2(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime(2021, 3, 29, 12, 00, 00, 00)
        data = json.dumps({"courier_id": 2})
        response = self.client.post("/orders/assign", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"orders": [{'id': 7}, {'id': 8},
                                                                    {'id': 3}, {'id': 5}],
                                                         "assign_time": "2021-03-29T12:00:00.00Z"})

    @mock.patch('delivery.views.datetime')
    def test_orders_assign_200_3(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime(2021, 3, 29, 12, 00, 00, 00)
        data = json.dumps({"courier_id": 3})
        response = self.client.post("/orders/assign", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"orders": [{'id': 7}, {'id': 8}, {'id': 1},
                                                                    {'id': 3}, {'id': 5}],
                                                         "assign_time": "2021-03-29T12:00:00.00Z"})

    def test_orders_assign_200_4(self):
        data = json.dumps({"courier_id": 4})
        response = self.client.post("/orders/assign", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"orders": []})

    def test_orders_assign_400_1(self):
        data = json.dumps({"courier_id": 5})
        response = self.client.post("/orders/assign", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_orders_assign_400_2(self):
        data = json.dumps({"courier_id": 5, "no_field": "no_field"})
        response = self.client.post("/orders/assign", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)


class ProcessorOrdersCompletePostTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        last_order_time = datetime(2021, 3, 29, 11, 40, 00, 00).strftime("%Y-%m-%dT%H:%M:%S.%f")[:22] + "Z"
        assign_time = datetime(2021, 3, 29, 12, 00, 00, 00).strftime("%Y-%m-%dT%H:%M:%S.%f")[:22] + "Z"
        Courier.objects.create(courier_id=1,
                               courier_type="foot",
                               regions=[1, 2, 3],
                               working_hours=["10:30-14:30", "15:00-18:00"],
                               have_weight=5)

        Courier.objects.create(courier_id=2,
                               courier_type="bike",
                               regions=[3, 4, 5],
                               working_hours=["00:30-04:30", "05:00-11:05"],
                               last_order_time=last_order_time,
                               have_weight=5)

        Order.objects.create(order_id=1,
                             courier=Courier.objects.get(courier_id=1),
                             assign_time=assign_time,
                             weight=3,
                             region=1,
                             delivery_hours=["10:00-12:00"])

        Order.objects.create(order_id=2,
                             courier=Courier.objects.get(courier_id=1),
                             assign_time=assign_time,
                             weight=2,
                             region=2,
                             delivery_hours=["15:20-19:30"])

        Order.objects.create(order_id=3,
                             courier=Courier.objects.get(courier_id=2),
                             assign_time=assign_time,
                             weight=10,
                             region=3,
                             delivery_hours=["06:00-13:00"])

    def test_orders_complete_200_1(self):
        data = json.dumps({"courier_id": 1, "order_id": 1, "complete_time": "2021-03-29T12:20:00.00Z"})
        response = self.client.post("/orders/complete", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"order_id": 1})

    def test_orders_complete_200_2(self):
        data = json.dumps({"courier_id": 2, "order_id": 3, "complete_time": "2021-03-29T12:20:00.00Z"})
        response = self.client.post("/orders/complete", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"order_id": 3})

    def test_orders_complete_400_1(self):
        data = json.dumps({"courier_id": 1, "order_id": 3, "complete_time": "2021-03-29T11:30:00.00Z"})
        response = self.client.post("/orders/complete", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_orders_complete_400_2(self):
        data = json.dumps({"courier_id": 2, "order_id": 1, "complete_time": "2021-03-29T11:30:00.00Z"})
        response = self.client.post("/orders/complete", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_orders_complete_400_3(self):
        data = json.dumps({"courier_id": 2, "order_id": 1, "complete_time": "2021-03-29T11:30:00.00Z"})
        response = self.client.post("/orders/complete", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_orders_complete_400_4(self):
        data = json.dumps({"courier_id": 2, "order_id": 3})
        response = self.client.post("/orders/complete", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)
