from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter to handle redirects after social login.
    """
    
    def get_login_redirect_url(self, request):
        """
        Override to redirect to cart page if there was a pending cart addition.
        """
        print(f"[DEBUG] Adapter: get_login_redirect_url called")
        print(f"[DEBUG] Adapter: Session keys: {list(request.session.keys())}")
        print(f"[DEBUG] Adapter: redirect_to_cart flag: {request.session.get('redirect_to_cart')}")
        
        # Check if we should redirect to cart
        redirect_to_cart = request.session.pop('redirect_to_cart', False)
        if redirect_to_cart:
            print("[DEBUG] Adapter: Redirecting to cart page")
            return reverse('cart')
        
        # Default behavior
        print("[DEBUG] Adapter: Using default redirect")
        return super().get_login_redirect_url(request)
