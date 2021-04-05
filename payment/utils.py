from order.models import Order

def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)