# middleware.py
from django.shortcuts import redirect
import json

class AccessCodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is trying to access a protected view
        if request.path.startswith('/dashboard/'):
            access_data = request.COOKIES.get('access_data')
            if not access_data:
                return redirect('enter_access_code')  # Redirect to the enter access code page
            access_data_dict = json.loads(access_data)
            name = access_data_dict.get('name')

            if name:
                request.access_name = name  # Add 'name' to the request object for template context

        response = self.get_response(request)
        return response
