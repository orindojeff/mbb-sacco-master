from stock.models import Order


def get_cart(user):
    order, created = Order.objects.get_or_create(user=user, complete=False)
    return order
