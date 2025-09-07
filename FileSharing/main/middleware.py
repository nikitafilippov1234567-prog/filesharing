from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

class PasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip password check for admin and login page
        if request.path.startswith('/admin/') or request.path == '/login/':
            return self.get_response(request)

        # Check if user is authenticated (password entered)
        if not request.session.get('authenticated', False):
            if request.path == '/login/' and request.method == 'POST':
                # Handle login
                password = request.POST.get('password', '')
                if password == settings.SITE_PASSWORD:
                    request.session['authenticated'] = True
                    return redirect('/')
                else:
                    return render(request, 'login.html', {'error': 'Неправильный пароль'})
            else:
                # Show login page
                return render(request, 'login.html')

        response = self.get_response(request)
        return response
