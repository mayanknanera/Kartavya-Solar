from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.core.mail import send_mail
from django.conf import settings

from django.db import transaction
from django.views.decorators.http import require_POST

from .models import Product, Cart, CartItem, Order, OrderItem


def home_view(request):
    # Checonck for logout success parameter
    if request.GET.get('logout') == 'success':
        messages.success(request, "You have been logged out successfully.")
    return render(request, "home.html")


def about_view(request):
    return render(request, "about.html")

@login_required
def contact_view(request):
    # Pre-fill form data for logged-in users
    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.email.split('@')[0],
            'email': request.user.email,
            'phone': request.user.phone,
        }
    
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        service = request.POST.get('service', '').strip()
        message_text = request.POST.get('message', '').strip()
        
        # Validation
        errors = []
        
        # Validate required fields
        if not all([name, phone, email, service]):
            errors.append("Please fill in all required fields.")
        
        # Name validation
        if name and len(name) < 2:
            errors.append("Name must be at least 2 characters.")
        
        # Phone validation
        if phone:
            import re
            phone_pattern = re.compile(r'^[6-9]\d{9}$')
            if not phone_pattern.match(phone):
                errors.append("Please enter a valid 10-digit mobile number starting with 6-9.")
        
        # Email validation
        if email:
            from django.core.validators import validate_email
            from django.core.exceptions import ValidationError
            try:
                validate_email(email)
            except ValidationError:
                errors.append("Please enter a valid email address.")
        
        # If there are errors, show them and return
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "contact.html", {'initial_data': initial_data})
        
        # Prepare email content
        subject = f"New Contact Form Submission - {service}"
        message = f"""
New Contact Form Submission from Kartavya Solar Website

Name: {name}
Phone: {phone}
Email: {email}
Service Interested In: {service}

Message:
{message_text if message_text else 'No message provided'}

---
This email was sent from the Kartavya Solar contact form.
        """
        
        try:
            # Use SMTP backend for contact form (send to Gmail)
            from django.core.mail import EmailMessage
            from django.core.mail.backends.smtp import EmailBackend
            
            # Create SMTP connection
            smtp_backend = EmailBackend(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS,
                fail_silently=False,
            )
            
            # Create and send email
            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['mayank73463@gmail.com'],
                connection=smtp_backend,
            )
            email_message.send()
            
            messages.success(request, "Thank you for contacting us! We'll get back to you within 24 hours.")
            return redirect('contact')
            
        except Exception as e:
            # Log the error for debugging
            print(f"Email Error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            messages.error(request, f"Sorry, there was an error sending your message. Please try again or contact us directly at mayank73463@gmail.com")
            return render(request, "contact.html", {'initial_data': initial_data})
    
    return render(request, "contact.html", {'initial_data': initial_data})


# def products_view(request):
#     return render(request, "products.html")


@login_required
def profile_view(request):
    active_tab = 'profile'  # Default tab
    # Get redirect URL from GET or POST
    next_url = request.GET.get('next') or request.POST.get('next')
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "update_profile":
            active_tab = 'profile'
            # Get form data
            first_name = request.POST.get("first_name", "").strip()
            last_name = request.POST.get("last_name", "").strip()
            phone = request.POST.get("phone", "").strip()
            address = request.POST.get("address", "").strip()
            city = request.POST.get("city", "").strip()
            state = request.POST.get("state", "").strip()
            pincode = request.POST.get("pincode", "").strip()
            
            # Validation
            errors = []
            
            # First name validation
            if not first_name:
                errors.append("First name is required.")
            elif len(first_name) < 2:
                errors.append("First name must be at least 2 characters.")
            
            # Last name validation (optional, but if provided must be valid)
            if last_name and len(last_name) < 2:
                errors.append("Last name must be at least 2 characters.")
            
            # Phone validation
            if phone:
                import re
                phone_pattern = re.compile(r'^[6-9]\d{9}$')  # Indian mobile number
                if not phone_pattern.match(phone):
                    errors.append("Please enter a valid 10-digit mobile number starting with 6-9.")
            
            # Pincode validation
            if pincode:
                if not pincode.isdigit() or len(pincode) != 6:
                    errors.append("Please enter a valid 6-digit pincode.")
            
            # If there are errors, show them and return
            if errors:
                for error in errors:
                    messages.error(request, error)
                return render(request, "profile.html", {'active_tab': active_tab, 'next': next_url})
            
            # Update profile information
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.phone = phone
            request.user.address = address
            request.user.city = city
            request.user.state = state
            request.user.pincode = pincode
            request.user.save()
            
            messages.success(request, "Profile updated successfully!")
            
            # Redirect to next URL if provided (e.g., checkout)
            if next_url:
                return redirect(next_url)
            return redirect("profile")
        
        elif action == "change_password":
            active_tab = 'password'
            # Change password
            current_password = request.POST.get("current_password", "")
            new_password = request.POST.get("new_password", "")
            confirm_password = request.POST.get("confirm_password", "")
            
            # Validate current password
            if not request.user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
                return render(request, "profile.html", {'active_tab': active_tab, 'next': next_url})
            
            # Validate new password
            if len(new_password) < 8:
                messages.error(request, "New password must be at least 8 characters long.")
                return render(request, "profile.html", {'active_tab': active_tab, 'next': next_url})
            
            if new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
                return render(request, "profile.html", {'active_tab': active_tab, 'next': next_url})
            
            # Update password
            request.user.set_password(new_password)
            request.user.save()
            
            # Re-login user
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            
            messages.success(request, "Password changed successfully!")
            return redirect("profile")

    return render(request, "profile.html", {'active_tab': active_tab, 'next': next_url})


# -----------------------------
# PRODUCT VIEWS
# -----------------------------


def product_list(request):
    products = Product.objects.filter(is_active=True)
    
    # Category filter
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category=category_filter)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            models.Q(name__icontains=search_query) | 
            models.Q(description__icontains=search_query)
        )
    
    # Price range filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Stock availability filter
    stock_filter = request.GET.get('stock', '')
    if stock_filter == 'in_stock':
        products = products.filter(stock_quantity__gt=0)
    elif stock_filter == 'out_of_stock':
        products = products.filter(stock_quantity=0)
    
    # Sorting
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-id')  # Default: newest first
    
    # Get all categories for filter dropdown
    categories = Product.CATEGORY_CHOICES
    
    context = {
        'products': products,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'stock_filter': stock_filter,
        'category_filter': category_filter,
        'categories': categories,
        'sort_by': sort_by,
        'total_count': products.count(),
    }
    
    return render(request, "products/product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "products/product_detail.html", {"product": product})


def _safe_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _cart_quantity_total(cart):
    if not cart:
        return 0
    return sum(item.quantity for item in cart.items.all())


# -----------------------------
# CART VIEWS
# -----------------------------


@require_POST
def add_to_cart(request, product_id):
    """
    Add product to cart (POST only).
    If user is not authenticated, store cart intent in session and redirect to login.
    """
    print(f"[DEBUG] add_to_cart called - product_id: {product_id}, method: {request.method}, authenticated: {request.user.is_authenticated}")
    
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = _safe_int(
        request.POST.get("quantity", product.min_order_quantity),
        product.min_order_quantity,
    )
    
    # If user is not authenticated, store cart intent and redirect to login
    if not request.user.is_authenticated:
        print(f"[DEBUG] User not authenticated - storing cart intent in session")
        request.session['pending_cart_add'] = {
            'product_id': product_id,
            'quantity': quantity,
            'product_slug': product.slug,
        }
        # Force session save
        request.session.modified = True
        print(f"[DEBUG] Session data stored: {request.session.get('pending_cart_add')}")
        
        messages.info(request, "Please login to add items to your cart.")
        
        # Redirect to login WITHOUT next parameter pointing to add-to-cart
        # The pending_cart_add in session will handle the cart addition
        redirect_url = reverse('login')
        print(f"[DEBUG] Redirecting to: {redirect_url}")
        return redirect(redirect_url)
    
    # User is authenticated - proceed with adding to cart
    print(f"[DEBUG] User authenticated - processing cart addition")
    return _process_add_to_cart(request, product, quantity)


def _process_add_to_cart(request, product, quantity):
    """
    Internal helper to process adding product to cart.
    Separated for reuse after login.
    """
    # Check stock
    if product.stock_quantity < quantity:
        messages.error(request, f"Sorry, only {product.stock_quantity} units left in stock for {product.name}.")
        return redirect("product_detail", slug=product.slug)

    # Check min/max limits
    if quantity < product.min_order_quantity:
        messages.warning(request, f"Minimum order quantity for {product.name} is {product.min_order_quantity} units.")
        return redirect("product_detail", slug=product.slug)

    if product.max_order_quantity and quantity > product.max_order_quantity:
        messages.warning(request, f"Maximum order quantity for {product.name} is {product.max_order_quantity} units.")
        return redirect("product_detail", slug=product.slug)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)

    if not created:
        new_quantity = cart_item.quantity + quantity
        # Final stock check for combined quantity
        if product.stock_quantity < new_quantity:
            messages.error(
                request,
                f"Cannot add more. You have {cart_item.quantity} in cart and only {product.stock_quantity} units available."
            )
            return redirect("cart")
        cart_item.quantity = new_quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    messages.success(request, f"Added {product.name} to your cart!")
    return redirect("cart")


@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    items = cart.items.all() if cart else []

    total = sum(item.get_total_price() for item in items)

    return render(
        request,
        "cart/cart.html",
        {
            "cart": cart,
            "items": items,
            "total": total,
        },
    )


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update the quantity of a cart item"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product = cart_item.product
    quantity = _safe_int(request.POST.get("quantity"), cart_item.quantity)

    success = False
    message = ""

    if quantity > 0:
        # Check limits
        if quantity < product.min_order_quantity:
            message = f"Minimum order quantity for {product.name} is {product.min_order_quantity} units."
        elif product.max_order_quantity and quantity > product.max_order_quantity:
            message = f"Maximum order quantity for {product.name} is {product.max_order_quantity} units."
        # Check stock
        elif product.stock_quantity < quantity:
            message = f"Not enough stock for {product.name}. Only {product.stock_quantity} units available."
        else:
            cart_item.quantity = quantity
            cart_item.save()
            success = True
            message = "Cart updated successfully!"
    else:
        cart_item.delete()
        success = True
        # Check if cart is now empty after deletion
        cart = Cart.objects.filter(user=request.user).first()
        items = cart.items.all() if cart else []
        if not items.exists():
            message = "Your cart is now empty. Continue shopping to add more items!"
        else:
            message = "Item removed from cart"

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        from django.http import JsonResponse

        cart = Cart.objects.filter(user=request.user).first()
        items = cart.items.all() if cart else []
        total = sum(item.get_total_price() for item in items)

        return JsonResponse(
            {
                "success": success,
                "message": message,
                "item_id": item_id,
                "quantity": cart_item.quantity if (quantity > 0 and success) else 0,
                "item_total": float(cart_item.get_total_price()) if (quantity > 0 and success) else 0,
                "cart_total": float(total),
                "cart_count": _cart_quantity_total(cart),
            }
        )

    if success:
        messages.success(request, message)
    else:
        messages.warning(request, message)

    return redirect("cart")


@login_required
@require_POST
def remove_cart_item(request, item_id):
    """Remove an item from the cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name

    cart = cart_item.cart
    cart_item.delete()
    
    # Check if cart is now empty
    items = cart.items.all()
    is_empty = not items.exists()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        from django.http import JsonResponse

        total = sum(item.get_total_price() for item in items)
        
        # Different message if cart is now empty
        if is_empty:
            message = "Your cart is now empty. Continue shopping to add more items!"
        else:
            message = f"{product_name} removed from cart"
        
        return JsonResponse(
            {
                "success": True,
                "message": message,
                "cart_total": float(total),
                "cart_count": _cart_quantity_total(cart),
                "cart_empty": is_empty,
            }
        )

    # For non-AJAX requests
    if is_empty:
        messages.info(request, "Your cart is now empty. Continue shopping to add more items!")
    else:
        messages.success(request, f"{product_name} removed from cart")
    
    return redirect("cart")


@login_required
@require_POST
def clear_cart(request):
    cart = Cart.objects.filter(user=request.user).first()

    if cart and cart.items.exists():
        cart.items.all().delete()
        messages.success(request, "Cart cleared successfully!")
    else:
        messages.info(request, "Your cart is already empty")

    return redirect("cart")


# -----------------------------
# CHECKOUT & ORDER (COD)
# -----------------------------


@login_required
@transaction.atomic
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty. Please add items before checkout.")
        return redirect("product_list")

    if request.method == "POST":
        # Final stock check before processing
        for item in cart.items.all():
            if item.product.stock_quantity < item.quantity:
                messages.error(
                    request,
                    f"Sorry, {item.product.name} is out of stock or has insufficient quantity. Please adjust your cart."
                )
                return redirect("cart")

        # Create order
        order = Order.objects.create(
            user=request.user,
            payment_method="COD",
            status="PLACED",
        )

        # Move cart items → order items & Deduct Stock
        for item in cart.items.all():
            # Create order item
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            # Deduct stock
            product = item.product
            product.stock_quantity -= item.quantity
            product.save()

        # Clear cart
        cart.items.all().delete()

        messages.success(request, "Order placed successfully! Your order will be delivered with Cash on Delivery.")
        return redirect("order_success")

    total = sum(item.get_total_price() for item in cart.items.all())

    return render(
        request,
        "checkout/checkout.html",
        {
            "cart": cart,
            "total": total,
        },
    )


@login_required
def order_success(request):
    return render(request, "orders/order_success.html")


@login_required
def orders_view(request):
    """Display user's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Calculate total for each order
    for order in orders:
        order.total = sum(item.price * item.quantity for item in order.items.all())
    
    return render(request, "orders/orders.html", {"orders": orders})


@login_required
def order_detail_view(request, order_id):
    """Display detailed view of a specific order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Calculate totals
    items = order.items.all()
    subtotal = sum(item.price * item.quantity for item in items)
    
    context = {
        'order': order,
        'items': items,
        'subtotal': subtotal,
    }
    
    return render(request, "orders/order_detail.html", context)


@login_required
@require_POST
def cancel_order(request, order_id):
    """Cancel an order and restore stock"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if order can be cancelled
    if order.status in ['COMPLETED', 'CANCELLED']:
        messages.error(request, f"Cannot cancel order. Order is already {order.status.lower()}.")
        return redirect('order_detail', order_id=order_id)
    
    # Restore stock for all items
    for item in order.items.all():
        product = item.product
        product.stock_quantity += item.quantity
        product.save()
    
    # Update order status
    order.status = 'CANCELLED'
    order.save()
    
    messages.success(request, f"Order #{order.id} has been cancelled successfully. Stock has been restored.")
    return redirect('order_detail', order_id=order_id)

