from django import template
from core.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            item_count = order.items.count()
            return item_count
    return 0
