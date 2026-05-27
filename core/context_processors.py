from .models import Cart


def cart_count(request):
    """Inject the total cart item count into every template context."""
    if not request.user.is_authenticated:
        return {"cart_item_count": 0}
    try:
        cart = Cart.objects.get(user=request.user)
        return {"cart_item_count": sum(item.quantity for item in cart.items.all())}
    except Cart.DoesNotExist:
        return {"cart_item_count": 0}
