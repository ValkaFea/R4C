from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from customers.models import Customer
from orders.models import Order
import json


@csrf_exempt
def create_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        customer, _ = Customer.objects.get_or_create(email=data["customer_email"])
        robot_serial = data["robot_serial"]
        order = Order.objects.create(customer=customer, robot_serial=robot_serial)
        return JsonResponse({"message": "Order created", "id": order.id}, status=201)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)
