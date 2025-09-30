from django.shortcuts import redirect
from django.contrib import messages

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define paths that explicitly require authentication
        protected_paths = [
            "/dashboard/",
            "/dashboard",
            "/products/",
            "/slider/",
            # "/registeruser/",
        ]
        
        # Get current path
        path = request.path
        
        # Check if path is protected
        is_protected = any(path.startswith(p) for p in protected_paths)
        
        # Check if user is authenticated
        is_authenticated = request.session.get("is_authenticated", False)
        
        # If accessing protected path and not authenticated, redirect
        if is_protected and not is_authenticated:
            # Store the attempted URL for redirect after login
            request.session['next'] = request.get_full_path()
            
            # Add warning message
            messages.warning(request, "You need to login first to access this page.")
            
            # Return redirect response immediately
            return redirect("login")
        
        # Continue with normal request processing
        response = self.get_response(request)
        return response























# from django.shortcuts import redirect
# from django.contrib import messages
# from django.urls import reverse

# class AuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Debug: Print session and path info
#         print(f"DEBUG - Path: {request.path}")
#         print(f"DEBUG - Session Keys: {list(request.session.keys())}")
#         print(f"DEBUG - is_authenticated: {request.session.get('is_authenticated')}")
#         print(f"DEBUG - user_id: {request.session.get('user_id')}")
        
#         # Define paths that don't require authentication
#         allowed_paths = [
#             "/login/", 
#             "/logout/",
#             "/static/",
#             "/media/",
#             "/admin/"
#             "/favicon.ico",
#             "/",  # Homepage
#         ]
        
#         # Define paths that explicitly require authentication
#         protected_paths = [
#             "/dashboard/",
#             "/dashboard",
#             "/products/",
#             "/slider/",  # Add slider to protected paths
#             "/registeruser/",
#         ]
        
#         # Get current path
#         path = request.path
#         print(f"DEBUG - Checking path: {path}")
        
#         # Check if path is in allowed paths
#         is_allowed = any(path.startswith(p) for p in allowed_paths)
#         is_protected = any(path.startswith(p) for p in protected_paths)
#         print(f"DEBUG - Is path allowed: {is_allowed}")
#         print(f"DEBUG - Is path protected: {is_protected}")
        
#         # Check if user is authenticated
#         is_authenticated = request.session.get("is_authenticated", False)
#         print(f"DEBUG - User authenticated: {is_authenticated}")
        
#         # If accessing protected path and not authenticated, redirect
#         if is_protected and not is_authenticated:
#             print(f"DEBUG - Redirecting to login from protected path: {path}")
            
#             # Store the attempted URL for redirect after login
#             request.session['next'] = request.get_full_path()
            
#             # Add warning message
#             messages.warning(request, "You need to login first to access this page.")
            
#             # Return redirect response immediately
#             return redirect("login")
        
#         # If not allowed and not authenticated, redirect (for other paths)
#         if not is_allowed and not is_authenticated:
#             print(f"DEBUG - Redirecting to login from: {path}")
            
#             # Store the attempted URL for redirect after login
#             request.session['next'] = request.get_full_path()
            
#             # Add warning message
#             messages.warning(request, "You need to login first to access this page.")
            
#             # Return redirect response immediately
#             return redirect("login")
        
#         print(f"DEBUG - Allowing access to: {path}")
        
#         # Continue with normal request processing
#         response = self.get_response(request)
#         return response