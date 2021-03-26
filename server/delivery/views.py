# from django.http import JsonResponse, HttpResponse
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK

from .serializers import *
from .models import *
from .exceptions import *

from rest_framework.response import Response
from rest_framework.views import APIView

from datetime import datetime


# /couriers/{courier_id}
class Couriers(APIView):

    def get(self, request, courier_id):
        try:
            courier_info = Courier.objects.get(courier_id=courier_id)
            serializer = CourierGetSerializer(courier_info)
            courier = serializer.data

            if courier.get("rating") == 0:
                courier.pop("rating", None)
            if courier.get("earnings") == 0:
                courier.pop("earnings", None)

            return Response(courier)
        except:
            return Response(status=HTTP_404_NOT_FOUND)

    def patch(self, request, courier_id):
        try:
            try:
                courier = Courier.objects.get(courier_id=courier_id)
            except:
                return Response(status=HTTP_404_NOT_FOUND)

            update_info = CourierPostSerializerRequest(data=request.data)
            try:
                update_info.is_valid()
                if update_info.errors:
                    raise ValidationErrorMy
            except:
                return Response(status=HTTP_400_BAD_REQUEST)

            # Check regions of courier and his orders
            if "regions" in update_info.data:
                courier.regions = update_info.data["regions"]
                courier.save()

                # Change some orders
                orders = Order.objects.filter(courier=courier)
                for order in orders:
                    region_ok = False
                    for region in courier.regions:
                        if order.region == region:
                            region_ok = True
                    if not region_ok:
                        order.courier = None
                        order.assign_time = ""
                        courier.have_weight += order.weight
                        order.save()

            # Check whether the time intervals of the orders and the courier match
            if "working_hours" in update_info.data:
                for date in update_info.data["working_hours"]:
                    if not (datetime.strptime(date[0:5], "%H:%M")) or not (
                            datetime.strptime(date[5:11], "-%H:%M")) or len(date) != 11:
                        return Response(status=HTTP_400_BAD_REQUEST)
                courier.working_hours = update_info.data["working_hours"]
                courier.save()

                # Change some orders
                orders = Order.objects.filter(courier=courier)
                for order in orders:
                    if not check_interval(courier, order):
                        order.courier = None
                        order.assign_time = ""
                        courier.have_weight += order.weight
                        order.save()

            # Check the weight that is available to the courier and how much his orders weigh
            if "courier_type" in update_info.data:

                orders = Order.objects.filter(courier=courier)
                orders_weight = 0.0
                for order in orders:
                    orders_weight += order.weight

                courier.courier_type = update_info.data["courier_type"]
                if courier.courier_type == "foot":
                    courier.have_weight = 10.0
                if courier.courier_type == "bike":
                    courier.have_weight = 15.0
                if courier.courier_type == "car":
                    courier.have_weight = 50.0

                courier.save()

                if courier.have_weight - orders_weight < 0.0:
                    take_orders = best_orders(courier, orders)

                    for order in take_orders:
                        order.courier = courier
                        courier.have_weight -= order.weight
                        order.save()

                else:
                    courier.have_weight -= orders_weight

            # Save updated courier info
            courier.save()
            serializer = CourierPostSerializerResponse(courier)
            return Response(serializer.data)

        except:
            return Response(status=HTTP_400_BAD_REQUEST)


# /couriers
class CouriersPost(APIView):

    def post(self, request):
        couriers = []  # All couriers that is possible to get
        couriers_ids = []  # Couriers with correct data
        not_valid_ids = []  # Couriers with incorrect data

        data = DataSerializer(data=request.data)
        try:
            data.is_valid()
            couriers_data = data.data["data"]
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

        # Checking all request data and couriers
        for courier in couriers_data:
            courier_data = CourierPostSerializerResponse(data=courier)

            try:
                courier_data.is_valid()
                for date in courier_data.data["working_hours"]:
                    try:
                        if not (datetime.strptime(date[0:5], "%H:%M")) or not (
                                datetime.strptime(date[5:12], "-%H:%M")) or len(date) != 11:
                            # if ("courier_id" in courier) and (str(courier["courier_id"]).isdigit()):
                            not_valid_ids.append(dict(id=courier_data.data["courier_id"]))
                            break
                    except:
                        # if ("courier_id" in courier) and (str(courier["courier_id"]).isdigit()):
                        not_valid_ids.append(dict(id=courier_data.data["courier_id"]))

                couriers.append(courier_data.data)
            except:
                if ("courier_id" in courier) and (str(courier["courier_id"]).isdigit()):
                    not_valid_ids.append(dict(id=courier["courier_id"]))

        # After checking all request data
        # If exist couriers with incorrect data
        if not_valid_ids:
            raise ValidationErrorMy(dict(couriers=not_valid_ids))

        else:
            # Saving couriers in the database
            for courier in couriers:
                courier_info = Courier(courier_id=courier["courier_id"],
                                       courier_type=courier["courier_type"],
                                       regions=courier["regions"],
                                       working_hours=courier["working_hours"])

                if courier_info.courier_type == "foot":
                    courier_info.have_weight = 10.0
                if courier_info.courier_type == "bike":
                    courier_info.have_weight = 15.0
                if courier_info.courier_type == "car":
                    courier_info.have_weight = 50.0

                courier_info.save()
                couriers_ids.append(dict(id=courier_info.courier_id))
            return Response(dict(couriers=couriers_ids), status=HTTP_201_CREATED)


# /orders
class Orders(APIView):

    def post(self, request):
        orders = []  # All orders that is possible to get
        orders_ids = []  # Orders with correct data
        not_valid_ids = []  # Orders with incorrect data

        data = DataSerializer(data=request.data)
        try:
            data.is_valid()
            orders_data = data.data["data"]
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

        # Checking all request data and orders
        for order in orders_data:

            order_data = OrderCreateSerializer(data=order)
            try:
                order_data.is_valid()
                try:
                    if OrderCompleted.objects.get(order_id=order_data.data["order_id"]) is not None:
                        not_valid_ids.append(dict(id=order_data.data["order_id"]))
                except:
                    for date in order_data.data["delivery_hours"]:
                        try:
                            if not (datetime.strptime(date[0:5], "%H:%M")) or not (
                                    datetime.strptime(date[5:12], "-%H:%M")) or len(date) != 11:
                                not_valid_ids.append(dict(id=order_data.data["order_id"]))
                                break
                        except:
                            not_valid_ids.append(dict(id=order_data.data["order_id"]))
                    if 0.01 <= order_data.data["weight"] <= 50:
                        orders.append(order_data.data)
                    else:
                        not_valid_ids.append(dict(id=order_data.data["order_id"]))
            except:
                if ("order_id" in order) and (str(order["order_id"]).isdigit()):
                    not_valid_ids.append(dict(id=order["order_id"]))

        # After checking all request data
        # If exist orders with incorrect data
        if not_valid_ids:
            raise ValidationErrorMy(dict(orders=not_valid_ids))

        else:
            # Saving orders in the database
            for order in orders:
                order_info = Order(order_id=order["order_id"],
                                   weight=order["weight"],
                                   region=order["region"],
                                   delivery_hours=order["delivery_hours"])
                order_info.save()
                orders_ids.append(dict(id=order_info.order_id))
            return Response(dict(orders=orders_ids), HTTP_201_CREATED)


# /orders/assign
class OrdersAssign(APIView):

    def post(self, request):
        try:
            assign_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:22] + "Z"
            courier_id = CourierIdSerializer(data=request.data)
            try:
                courier_id.is_valid()
                courier = Courier.objects.get(courier_id=courier_id.data["courier_id"])
            except:
                return Response(status=HTTP_400_BAD_REQUEST)

            # Choose best orders and set it in database
            take_orders = best_orders(courier, None)
            response = dict(orders=[])
            if take_orders:
                response["assign_time"] = assign_time

                for order in take_orders:
                    order.courier = courier
                    order.assign_time = assign_time
                    if courier.courier_type == "foot":
                        order.courier_coefficient = 2
                    if courier.courier_type == "bike":
                        order.courier_coefficient = 5
                    if courier.courier_type == "car":
                        order.courier_coefficient = 9
                    order.save()

                    courier.have_weight -= order.weight
                    courier.save()
                    response["orders"].append(dict(id=order.order_id))

            return Response(data=response, status=HTTP_200_OK)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)


# /orders/complete
class OrdersComplete(APIView):
    def post(self, request):

        try:
            # Check request data
            complete_request = OrdersCompleteSerializer(data=request.data)
            try:
                complete_request.is_valid()

                complete = complete_request.data
                order = Order.objects.get(order_id=complete.get("order_id"))
                courier = Courier.objects.get(courier_id=complete.get("courier_id"))

            except:
                return Response(status=HTTP_400_BAD_REQUEST)

            if order.courier != courier:
                return Response(status=HTTP_400_BAD_REQUEST)

            # Create new completed order, add in database
            start_str = order.assign_time
            if courier.last_order_time != "":
                start_str = courier.last_order_time

            start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
            finish = datetime.strptime(complete.get("complete_time"), "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()

            delivery_time = int(finish - start)
            order_completed = OrderCompleted(courier=courier,
                                             order_id=order.order_id,
                                             weight=order.weight,
                                             region=order.region,
                                             assign_time=order.assign_time,
                                             complete_time=complete.get("complete_time"),
                                             delivery_time=delivery_time)
            order_completed.save()

            # Change information in courier
            completed_orders = OrderCompleted.objects.filter(courier=courier)
            regions = [order.region for order in completed_orders]

            middle_times = []
            regions = set(regions)
            for region in regions:

                middle_time_region = 0
                orders_count_region = 0
                orders_completed_region = completed_orders.filter(region=region)

                if orders_completed_region:
                    for order_completed_region in orders_completed_region:
                        orders_count_region += 1
                        middle_time_region = ((orders_count_region - 1) * middle_time_region +
                                              order_completed_region.delivery_time) / orders_count_region

                    middle_times.append(middle_time_region)

            if middle_times:
                middle_times.sort()
                courier.rating = (60 * 60 - min(middle_times[0], 60 * 60)) / (60 * 60) * 5
                courier.rating = round(courier.rating, 2)

            courier.earnings += 500 * order.courier_coefficient
            courier.last_order_time = complete.get("complete_time")
            courier.have_weight += order.weight

            courier.save()
            order.delete()

            response = dict(order_id=complete.get("order_id"))
            return Response(data=response, status=HTTP_200_OK)

        except:
            return Response(status=HTTP_400_BAD_REQUEST)


def best_orders(courier, orders):
    orders_list = []
    for region in courier.regions:
        orders_in_region = []

        if orders is None:
            orders_in_region = Order.objects.filter(region=region, courier=None)  # weight__lte=need_weight
        else:
            for order in orders:

                order.courier = None
                # courier.have_weight += order.weight
                order.save()

                if order.region == region:
                    orders_in_region.append(order)

        for order in orders_in_region:
            if check_interval(courier, order):
                orders_list.append(order)

    orders_list = sorted(orders_list, key=lambda x: x.weight, reverse=True)

    heavy_take_orders = []
    light_take_orders = []
    take_weight = 0.0
    for order in orders_list:
        if (take_weight < courier.have_weight) and (take_weight + order.weight <= courier.have_weight):
            heavy_take_orders.append(order)
            take_weight += order.weight
        else:
            pass

    take_weight = 0.0
    for order in reversed(orders_list):
        if (take_weight < courier.have_weight) and (take_weight + order.weight <= courier.have_weight):
            light_take_orders.append(order)
            take_weight += order.weight
        else:
            pass

    if len(heavy_take_orders) >= len(light_take_orders):
        take_orders = heavy_take_orders
    else:
        take_orders = light_take_orders

    return take_orders


def check_interval(courier, order):
    for time_c in courier.working_hours:
        for time_o in order.delivery_hours:
            if (time_o[0:5] <= time_c[0:5] < time_o[6:11]) or (
                    time_c[0:5] <= time_o[0:5] <= time_c[6:11]):
                return True
    return False
