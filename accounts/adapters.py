from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    After a social login (e.g. Google), redirect to the cart page
    if the user had a pending cart addition, otherwise use the default redirect.
    """

    def get_login_redirect_url(self, request):
        if request.session.pop("redirect_to_cart", False):
            return reverse("cart")
        return super().get_login_redirect_url(request)
