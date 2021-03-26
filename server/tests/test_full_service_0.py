from unittest import mock
from django.test import TestCase
from freezegun import freeze_time
from rest_framework.utils import json
from delivery.views import *


# Integration test
class FullServiceTest(TestCase):

    # last_order_time = datetime(2021, 3, 29, 11, 40, 00, 00).strftime("%Y-%m-%dT%H:%M:%S.%f")[:22] + "Z"

    @classmethod
    def setUpTestData(cls):
        pass

    # @mock.patch('delivery.views.datetime.now')
    @freeze_time("2021-03-29-12-00-00-00")
    def test_create_couriers__change_couriers__create_orders__assign_orders__complete_orders(
            self):  # , mocked_datetime):
        # Create some couriers
        data = json.dumps(
            {
                "data": [
                    {
                        "courier_id": 1,
                        "courier_type": "foot",
                        "regions": [1, 2, 3],
                        "working_hours": ["10:30-14:30", "15:00-18:00"]
                    },
                    {
                        "courier_id": 2,
                        "courier_type": "bike",
                        "regions": [3, 4, 5, 6, 7],
                        "working_hours": ["00:30-04:30", "05:00-11:05"]
                    },
                    {
                        "courier_id": 3,
                        "courier_type": "car",
                        "regions": [1, 2, 3, 4, 5, 6, 7],
                        "working_hours": ["10:30-10:45", "19:00-23:45"]
                    }
                ]
            }
        )
        response = self.client.post("/couriers", data, content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(json.loads(response.content), {"couriers": [{"id": 1}, {"id": 2}, {"id": 3}]})

        # Try to change one of them with not right method
        data = json.dumps(
            {
                "data": [
                    {
                        "courier_id": 1,
                        "courier_type": "foot",
                        "regions": [1, 2, 3, 7],
                        "working_hours": ["10:30-14:30", "15:00-18:00"]
                    }
                ]
            }
        )
        response = self.client.post("/couriers", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content), {"validation_error": {"couriers": [{"id": 1}]}})

        # Understand mistake and this time doing everything right
        data = json.dumps({
            "courier_type": "foot",
            "regions": [1, 2, 3, 8],
            "working_hours": ["10:30-13:30", "14:00-18:00"]})
        response = self.client.patch("/couriers/1", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"courier_id": 1,
                                                         "courier_type": "foot",
                                                         "regions": [1, 2, 3, 8],
                                                         "working_hours": ["10:30-13:30", "14:00-18:00"]})

        # Check courier
        response = self.client.get("/couriers/1", content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"courier_id": 1,
                                                         "courier_type": "foot",
                                                         "regions": [1, 2, 3, 8],
                                                         "working_hours": ["10:30-13:30", "14:00-18:00"]})

        # Create some orders
        data = json.dumps(
            {
                "data": [
                    {
                        "order_id": 1,
                        "weight": 3.99,
                        "region": 1,
                        "delivery_hours": ["10:00-12:00"]
                    },
                    {
                        "order_id": 2,
                        "weight": 4,
                        "region": 3,
                        "delivery_hours": ["00:00-05:00"]
                    },
                    {
                        "order_id": 3,
                        "weight": 5.2,
                        "region": 5,
                        "delivery_hours": ["09:00-11:00", "16:00-21:30"]
                    },
                    {
                        "order_id": 4,
                        "weight": 5,
                        "region": 1,
                        "delivery_hours": ["15:20-19:30"]
                    },
                    {
                        "order_id": 5,
                        "weight": 6,
                        "region": 3,
                        "delivery_hours": ["07:20-19:30"]
                    },
                    {
                        "order_id": 6,
                        "weight": 10,
                        "region": 3,
                        "delivery_hours": ["11:20-11:30"]
                    },
                    {
                        "order_id": 7,
                        "weight": 2,
                        "region": 5,
                        "delivery_hours": ["06:20-15:30"]
                    },
                    {
                        "order_id": 8,
                        "weight": 4,
                        "region": 3,
                        "delivery_hours": ["06:20-14:30"]
                    },
                    {
                        "order_id": 9,
                        "weight": 45,
                        "region": 7,
                        "delivery_hours": ["06:00-13:30"]
                    }
                ]
            }
        )
        response = self.client.post("/orders", data, content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(json.loads(response.content), {"orders": [{"id": 1}, {"id": 2}, {"id": 3},
                                                                    {"id": 4}, {"id": 5}, {"id": 6},
                                                                    {"id": 7}, {"id": 8}, {"id": 9}]})

        # Need MORE orders
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
                        "order_id": 10,
                        "weight": 15,
                        "region": 1,
                        "delivery_hours": ["09:00-18:00"],
                        "customer": "Ivan Ivanov"
                    },
                    {
                        "order_id": 11,
                        "weight": 15,
                        "region": 1
                    }
                ]
            }
        )
        response = self.client.post("/orders", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content), {"validation_error": {"orders": [{"id": 1},
                                                                                         {"id": 10}, {"id": 11}]}})

        # Give orders to couriers
        data = json.dumps({"courier_id": 1})
        # mocked_datetime.now.return_value = datetime(2021, 3, 29, 12, 00, 00, 00)
        # @freeze_time("2021-3-29-12-00-00-00")
        response = self.client.post("/orders/assign", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"orders": [{"id": 1}, {"id": 8}],
                                                         "assign_time": "2021-03-29T12:00:00.00Z"})

        data = json.dumps({"courier_id": 2})
        response = self.client.post("/orders/assign", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"orders": [{"id": 5}, {"id": 3}, {"id": 7}],
                                                         "assign_time": "2021-03-29T12:00:00.00Z"})

        data = json.dumps({"courier_id": 3})
        response = self.client.post("/orders/assign", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"orders": [{"id": 9}, {"id": 4}],
                                                         "assign_time": "2021-03-29T12:00:00.00Z"})

        # Trying to give an order to a non-existent courier
        data = json.dumps({"courier_id": 4})
        response = self.client.post("/orders/assign", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

        # Order complete
        data = json.dumps({"courier_id": 2, "order_id": 7, "complete_time": "2021-03-29T12:05:00.00Z"})
        response = self.client.post("/orders/complete", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"order_id": 7})

        # Check courier
        response = self.client.get("/couriers/2", content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"courier_id": 2,
                                                         "courier_type": "bike",
                                                         "regions": [3, 4, 5, 6, 7],
                                                         "working_hours": ["00:30-04:30", "05:00-11:05"],
                                                         'earnings': 2500,
                                                         'rating': 4.58})

        # Order complete
        data = json.dumps({"courier_id": 1, "order_id": 1, "complete_time": "2021-03-29T12:24:10.00Z"})
        response = self.client.post("/orders/complete", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"order_id": 1})

        # Order complete
        data = json.dumps({"courier_id": 1, "order_id": 8, "complete_time": "2021-03-29T12:30:55.00Z"})
        response = self.client.post("/orders/complete", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"order_id": 8})

        # Check courier
        response = self.client.get("/couriers/1", content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"courier_id": 1,
                                                         "courier_type": "foot",
                                                         "regions": [1, 2, 3, 8],
                                                         "working_hours": ["10:30-13:30", "14:00-18:00"],
                                                         'earnings': 2000,
                                                         'rating': 4.44})

        data = json.dumps(
            {"courier_type": "foot", "regions": [3, 4, 5], "working_hours": ["00:30-04:30", "05:00-11:05"]})
        response = self.client.patch("/couriers/2", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"courier_id": 2,
                                                         "courier_type": "foot",
                                                         "regions": [3, 4, 5],
                                                         "working_hours": ["00:30-04:30", "05:00-11:05"]})

        # Check courier
        response = self.client.get("/couriers/2", content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"courier_id": 2,
                                                         "courier_type": "foot",
                                                         "regions": [3, 4, 5],
                                                         "working_hours": ["00:30-04:30", "05:00-11:05"],
                                                         "earnings": 2500,
                                                         "rating": 4.58})

        data = json.dumps({"courier_id": 2})
        # print("")
        # print(Order.objects.filter(courier=Courier.objects.get(courier_id=2)))
        response = self.client.post("/orders/assign", data, content_type="application/json")
        # print(Order.objects.filter(courier=Courier.objects.get(courier_id=2)))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"orders": [{"id": 2}],
                                                         "assign_time": "2021-03-29T12:00:00.00Z"})

        data = json.dumps({"courier_type": "foot"})
        response = self.client.patch("/couriers/3", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"courier_id": 3,
                                                         "courier_type": "foot",
                                                         "regions": [1, 2, 3, 4, 5, 6, 7],
                                                         "working_hours": ["10:30-10:45", "19:00-23:45"]})

        data = json.dumps({"courier_type": "car",
                           "regions": [3, 4, 5, 6, 7],
                           "working_hours": ["00:30-04:30", "09:00-15:05"]})
        response = self.client.patch("/couriers/2", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"courier_id": 2,
                                                         "courier_type": "car",
                                                         "regions": [3, 4, 5, 6, 7],
                                                         "working_hours": ["00:30-04:30", "09:00-15:05"]})

        data = json.dumps({"courier_id": 2})
        response = self.client.post("/orders/assign", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"orders": [{"id": 6}, {"id": 3}],
                                                         "assign_time": "2021-03-29T12:00:00.00Z"})

        # Complete orders
        data = json.dumps({"courier_id": 2, "order_id": 3, "complete_time": "2021-03-29T12:45:55.00Z"})
        response = self.client.post("/orders/complete", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"order_id": 3})

        data = json.dumps({"courier_id": 2, "order_id": 6, "complete_time": "2021-03-29T13:00:29.30Z"})
        response = self.client.post("/orders/complete", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"order_id": 6})

        data = json.dumps({"courier_id": 2, "order_id": 2, "complete_time": "2021-03-29T13:33:11.09Z"})
        response = self.client.post("/orders/complete", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"order_id": 2})

        data = json.dumps({"courier_id": 2, "order_id": 4, "complete_time": "2021-03-29T12:46:35.99Z"})
        response = self.client.post("/orders/complete", data, content_type="application/json")
        self.assertEquals(response.status_code, 400)

        # Check information
        response = self.client.get("/couriers/2", content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), {"courier_id": 2,
                                                         "courier_type": "car",
                                                         "regions": [3, 4, 5, 6, 7],
                                                         "working_hours": ["00:30-04:30", "09:00-15:05"],
                                                         "earnings": 12500,
                                                         "rating": 3.09})