from django.shortcuts import render,redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from myapp.models import User
import json
import time
from django.contrib import messages

@csrf_protect
@never_cache
def loginuser(request):
    # Redirect if already logged in
    # if request.session.get('user_id'):
    #     messages.info(request, "You are already logged in.")
    #     return redirect('dashboard')
    if request.method == "POST":
        # Get form data
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        remember = request.POST.get("remember")
        
        # Input validation
        if not username:
            messages.error(request, "Please enter your username.")
            return render(request, "login.html")
        
        if not password:
            messages.error(request, "Please enter your password.")
            return render(request, "login.html")
        
        # Rate limiting - prevent brute force attacks
        session_key = f"login_attempts_{request.META.get('REMOTE_ADDR', 'unknown')}"
        attempts = request.session.get(session_key, 0)
        
        if attempts >= 5:
            messages.error(request, "Too many failed login attempts. Please try again in 15 minutes.")
            return render(request, "login.html")
        
        try:
            # Find user by username (case-insensitive)
            user = User.objects.get(username__iexact=username)
            
            # Verify password
            if check_password(password, user.password):
                # Successful login
                
                # Clear failed attempts
                if session_key in request.session:
                    del request.session[session_key]
                
                # Create user session
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['email'] = user.email
                request.session['login_time'] = int(time.time())
                request.session['is_authenticated'] = True
                
                # Set session expiry based on "Remember Me"
                if remember:
                    # Remember for 30 days
                    request.session.set_expiry(30 * 24 * 60 * 60)
                else:
                    # Session expires when browser closes
                    request.session.set_expiry(0)
                
                # Success message
                messages.success(request, f"Welcome back, {user.username}!")
                
                # Redirect to dashboard or next page
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            
            else:
                # Wrong password
                request.session[session_key] = attempts + 1
                messages.error(request, "Invalid username or password.")
                
        except User.DoesNotExist:
            # User not found
            request.session[session_key] = attempts + 1
            messages.error(request, "Invalid username or password.")
            
        except Exception as e:
            # Unexpected error
            messages.error(request, "An error occurred during login. Please try again.")
            print(f"Login error: {str(e)}")  # Log for debugging
    
    return render(request, "admin/login.html")

def logoutuser(request):
    if request.method == "POST":
        request.session.flush()  # Clear all session data
        messages.success(request, "You have been logged out.")
        return redirect('login')  # Redirect to login page
    return redirect('dashboard')  # Optional fallback