from django.shortcuts import redirect
from django.template.context_processors import request
from django.urls import reverse


class SellerRequireMiddelWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        seller_only_path = [
            'register/seller/',
            'dashboard/seller/',
        ]
        if any(request.path.startswitch(path) for path in seler_only_paths):
            if not request.user.is_authenticated or not getattr(request.user, 'is_seller', False):
                return redirect(reverse('accounts:login'))
        response = self.get_response(request)
        return response
