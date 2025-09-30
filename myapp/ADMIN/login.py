from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db import DatabaseError, OperationalError
from myapp.models import User
import json
import time
import logging

# Configure logger
logger = logging.getLogger(__name__)


@csrf_protect
@never_cache
def loginuser(request):
    """
    Handle user login with proper error handling and security measures.
    """
    try:
        # Redirect if already logged in
        if request.session.get("user_id") and request.session.get("is_authenticated"):
            messages.info(request, "You are already logged in.")
            return redirect("dashboard")

        if request.method == "POST":
            try:
                # Get form data with safe defaults
                username = request.POST.get("username", "").strip()
                password = request.POST.get("password", "")
                remember = request.POST.get("remember")

                # Input validation
                if not username:
                    messages.error(request, "Please enter your username.")
                    return render(request, "admin/login.html")

                if not password:
                    messages.error(request, "Please enter your password.")
                    return render(request, "admin/login.html")

                # Additional validation
                if len(username) > 150:
                    messages.error(request, "Username is too long.")
                    return render(request, "admin/login.html")

                if len(password) > 128:
                    messages.error(request, "Password is too long.")
                    return render(request, "admin/login.html")

                # Rate limiting - prevent brute force attacks
                try:
                    remote_addr = request.META.get(
                        "HTTP_X_FORWARDED_FOR",
                        request.META.get("REMOTE_ADDR", "unknown"),
                    )
                    # Get first IP if multiple (for proxies/load balancers)
                    if "," in remote_addr:
                        remote_addr = remote_addr.split(",")[0].strip()

                    session_key = f"login_attempts_{remote_addr}"
                    attempts = request.session.get(session_key, 0)

                    if attempts >= 5:
                        logger.warning(f"Rate limit exceeded for IP: {remote_addr}")
                        messages.error(
                            request,
                            "Too many failed login attempts. Please try again in 15 minutes.",
                        )
                        return render(request, "admin/login.html")
                except Exception as e:
                    logger.error(f"Rate limiting error: {str(e)}")
                    # Continue without rate limiting if it fails
                    session_key = None
                    attempts = 0

                try:
                    # Find user by username (case-insensitive)
                    user = User.objects.get(username__iexact=username)

                    # Verify password
                    try:
                        password_valid = check_password(password, user.password)
                    except Exception as e:
                        logger.error(f"Password verification error: {str(e)}")
                        messages.error(
                            request, "An error occurred during authentication."
                        )
                        return render(request, "admin/login.html")

                    if password_valid:
                        # Successful login
                        try:
                            # Clear failed attempts
                            if session_key and session_key in request.session:
                                del request.session[session_key]

                            # Create user session
                            request.session["user_id"] = user.id
                            request.session["username"] = user.username
                            request.session["email"] = user.email
                            request.session["login_time"] = int(time.time())
                            request.session["is_authenticated"] = True

                            # Set session expiry based on "Remember Me"
                            if remember:
                                # Remember for 30 days
                                request.session.set_expiry(30 * 24 * 60 * 60)
                            else:
                                # Session expires when browser closes
                                request.session.set_expiry(0)

                            # Save session explicitly for Vercel
                            request.session.modified = True

                            # Success message
                            messages.success(request, f"Welcome back, {user.username}!")

                            # Redirect to dashboard or next page
                            next_page = request.GET.get("next", "dashboard")

                            # Validate next_page to prevent open redirect
                            if next_page and not next_page.startswith("/"):
                                next_page = "dashboard"

                            logger.info(f"Successful login for user: {user.username}")
                            return redirect(next_page)

                        except Exception as e:
                            logger.error(f"Session creation error: {str(e)}")
                            messages.error(
                                request,
                                "Login successful but session creation failed. Please try again.",
                            )
                            return render(request, "admin/login.html")

                    else:
                        # Wrong password
                        if session_key:
                            request.session[session_key] = attempts + 1
                            request.session.modified = True
                        logger.warning(f"Failed login attempt for username: {username}")
                        messages.error(request, "Invalid username or password.")

                except User.DoesNotExist:
                    # User not found
                    if session_key:
                        request.session[session_key] = attempts + 1
                        request.session.modified = True
                    logger.warning(f"Login attempt for non-existent user: {username}")
                    messages.error(request, "Invalid username or password.")

                except DatabaseError as e:
                    # Database connection issues
                    logger.error(f"Database error during login: {str(e)}")
                    messages.error(
                        request, "Database connection error. Please try again later."
                    )

                except OperationalError as e:
                    # Database operational issues
                    logger.error(f"Database operational error: {str(e)}")
                    messages.error(
                        request,
                        "Service temporarily unavailable. Please try again later.",
                    )

                except Exception as e:
                    # Unexpected database/user query errors
                    logger.error(
                        f"Unexpected error during user authentication: {str(e)}"
                    )
                    messages.error(
                        request, "An error occurred during login. Please try again."
                    )

            except Exception as e:
                # POST request processing errors
                logger.error(f"Error processing login request: {str(e)}")
                messages.error(
                    request,
                    "An error occurred processing your request. Please try again.",
                )

        # Render login page for GET requests or after errors
        return render(request, "admin/login.html")

    except Exception as e:
        # Top-level catch-all for any unexpected errors
        logger.critical(f"Critical error in loginuser view: {str(e)}")
        try:
            messages.error(
                request, "A critical error occurred. Please contact support."
            )
            return render(request, "admin/login.html")
        except:
            # If even rendering fails, return a basic error response
            return JsonResponse(
                {"error": "A critical error occurred. Please try again later."},
                status=500,
            )


def logoutuser(request):
    """
    Handle user logout with proper error handling.
    """
    try:
        if request.method == "POST":
            try:
                # Get username before flushing session
                username = request.session.get("username", "User")

                # Clear all session data
                request.session.flush()

                # Success message
                messages.success(
                    request,
                    f"Goodbye {username}! You have been logged out successfully.",
                )

                logger.info(f"User logged out: {username}")
                return redirect("login")

            except Exception as e:
                # Session flush error
                logger.error(f"Error during logout session flush: {str(e)}")

                # Try to clear session manually
                try:
                    request.session.clear()
                    messages.warning(
                        request,
                        "Logged out with warnings. Please clear your browser cache.",
                    )
                    return redirect("login")
                except:
                    messages.error(
                        request, "Error during logout. Please close your browser."
                    )
                    return redirect("login")

        # GET request - redirect to dashboard
        return redirect("dashboard")

    except Exception as e:
        # Top-level error handling
        logger.critical(f"Critical error in logoutuser view: {str(e)}")
        try:
            messages.error(request, "An error occurred during logout.")
            return redirect("login")
        except:
            return JsonResponse(
                {"error": "Logout failed. Please close your browser."}, status=500
            )
