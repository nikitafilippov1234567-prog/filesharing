from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the site password from settings
        site_password = getattr(settings, 'SITE_PASSWORD', 'default')
        
        # URLs that don't require authentication
        exempt_urls = [
            reverse('login'),
        ]
        
        # Check if current URL is exempt
        current_url = request.path_info
        is_exempt = any(current_url.startswith(url) for url in exempt_urls)
        
        # Check if user is authenticated (has correct session)
        is_authenticated = request.session.get('authenticated', False)
        
        # If not authenticated and not on exempt URL, redirect to login
        if not is_authenticated and not is_exempt:
            return redirect('login')
        
        # Handle login POST request
        if current_url == reverse('login') and request.method == 'POST':
            password = request.POST.get('password', '')
            if password == site_password:
                request.session['authenticated'] = True
                logger.info(f"Successful authentication from IP: {request.META.get('REMOTE_ADDR')}")
                return redirect('upload')
            else:
                logger.warning(f"Failed authentication attempt from IP: {request.META.get('REMOTE_ADDR')}")
                # Let the view handle the error message
        
        response = self.get_response(request)
        return response
