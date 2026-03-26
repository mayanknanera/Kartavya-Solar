from .models import Cart


def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = sum(item.quantity for item in cart.items.all())
            return {"cart_item_count": count}
        except Cart.DoesNotExist:
            return {"cart_item_count": 0}
    return {"cart_item_count": 0}
