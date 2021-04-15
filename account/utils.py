from order.models import Order


def orders_list(request) -> list:
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id, billing_status=True)

    return orders
