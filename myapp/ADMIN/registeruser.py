from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from myapp.models import User
from django.shortcuts import get_object_or_404, redirect



def registeruser(request):
    users=User.objects.all()
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Basic validation
        errors = []

        if not username or not email or not password:
            errors.append("All fields are required.")

        try:
            validate_email(email)
        except ValidationError:
            errors.append("Please enter a valid email address.")

        if password and len(password) < 8:
            errors.append("Password must be at least 8 characters long.")

        # Check if passwords match (if confirm_password field exists)
        if confirm_password and password != confirm_password:
            errors.append("Passwords do not match.")

        # Check if username already exists
        if username and User.objects.filter(username=username).exists():
            errors.append("Username already exists. Please choose a different one.")

        # Check if email already exists
        if email and User.objects.filter(email=email).exists():
            errors.append("Email already registered. Please use a different email.")

        # If no errors, create the user
        if not errors:
            try:
                # IMPORTANT: Hash the password before storing
                hashed_password = make_password(password)

                user = User.objects.create(
                    username=username,
                    email=email,
                    password=hashed_password,  # Store hashed password
                )

                messages.success(
                    request, f"Account created successfully for {username}!"
                )
                return redirect("dashboard")  # Redirect to login page

            except Exception as e:
                messages.error(request, f"Error creating account: {str(e)}")
        else:
            # Display validation errors
            for error in errors:
                messages.error(request, error)

    return render(request, "admin/userregister.html",{"users":users})


def deleteuser(request, id):
    if request.method == "POST":
        user = get_object_or_404(User, id=id)
        user.delete()
        messages.success(request, "User deleted successfully.")
    return redirect('registeruser')