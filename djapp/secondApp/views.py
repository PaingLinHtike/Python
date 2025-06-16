from django.shortcuts import render
from django.http import HttpResponse
import pymongo

connection = pymongo.MongoClient("localhost",27017)
admin_database = connection["admin"]
admin_collection = admin_database["login"]

instructor_database = connection["instructor"]
instructor_collection = instructor_database["signin"]

student_database = connection["student"]
student_collection = student_database["signin"]

def home(request):
    if request.method == "POST":
        try:
            user_name = request.POST.get('usename')
            email = request.POST.get('email')
            password = request.POST.get('password')
            created_date = request.POST.get('created_datae')
            user_type = request.POST.get('user_type')

            if user_type == "instructor":
                exists = instructor_collection.find_one({"user_name": user_name, "email": email})
                if exists:
                    return render(request, 'signin.html', {'popup': f"{user_type.capitalize()} already exists with this username and email!"})

                instructor_collection.insert_one({
                    "user_name": user_name,
                    "email": email,
                    "password": password,
                    "created_date": created_date,
                    "user_type": user_type
                })
                return render(request, 'login.html')

            elif user_type == "student":
                exists = student_collection.find_one({"user_name": user_name, "email": email})
                if exists:
                    return render(request, 'signin.html', {'popup': f"{user_type.capitalize()} already exists with this username and email!"})
                if exists:
                    return render(request, 'signin.html', {'error': 'Student already exists with this username and email!'})
                student_collection.insert_one({
                    "user_name": user_name,
                    "email": email,
                    "password": password,
                    "created_date": created_date,
                    "user_type": user_type
                })
                return render(request, 'login.html')

            else:
                return render(request, 'signin.html', {'error': 'Invalid user type!'})

        except Exception as error:
            return render(request, 'signin.html', {'error': error})

    # This is the default for GET requests
    return render(request, 'signin.html')


def add(request):
    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        date = request.POST.get('created_date')
        user_type = request.POST.get('user_type')

        try:
            if user_type == "instructor":
                exists = instructor_collection.find_one({"user_name": name, "email": email})
                if exists:
                    return render(request, 'signin.html', {'popup': f"{user_type.capitalize()} already exists with this username and email!"})
                instructor_collection.insert_one({
                    "user_name": name,
                    "email": email,
                    "password": password,
                    "created_date": date,
                    "user_type": user_type
                })

                return render(request, 'result.html', {
                    'name': name,
                    'email': email,
                    'password': password,
                    'date': date,
                    'user_type': user_type
                })
            elif user_type == "student":
                    exists = student_collection.find_one({"user_name": name, "email": email})
                    if exists:
                        return render(request, 'signin.html', {'popup': f"{user_type.capitalize()} already exists with this username and email!"})
                    student_collection.insert_one({
                    "user_name": name,
                    "email": email,
                    "password": password,
                    "created_date": date,
                    "user_type": user_type
                })

                    return render(request, 'result.html', {
                        'name': name,
                        'email': email,
                        'password': password,
                        'date': date,
                        'user_type': user_type
                    })

        except Exception as error:
            return HttpResponse(f"Error storing data: {error}")
    else:
        return HttpResponse("Invalid request method.")

def index(request):
    return render(request,'index.html')

def login(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if role == "admin":
            collection = admin_collection
        elif role == "instructor":
            collection = instructor_collection
        elif role == "student":
            collection = student_collection
        else:
            return render(request, "login.html", {"popup": "Invalid role selected."})

        user = collection.find_one({"user_name": user_name})
        if not user:
            return render(request, "login.html", {"popup": "Invalid username"})

        invalid_fields = 0
        if user.get("user_name") != user_name:
            invalid_fields += 1
        if user.get("email") != email:
            invalid_fields += 1
        if user.get("password") != password:
            invalid_fields += 1

        if invalid_fields > 1:
            return render(request, "login.html", {"popup": "Invalid Data"})
        elif invalid_fields == 1:
            if user.get("email") != email:
                return render(request, "login.html", {"popup": "Invalid email"})
            if user.get("password") != password:
                return render(request, "login.html", {"popup": "Invalid password"})

        # ✅ Redirect based on role
        if role == "admin":
            return render(request, "Admin/admin_dashboard.html", {"name": user_name})
        elif role == "instructor":
            return render(request, "Instructor/instructor_home.html", {"name": user_name})
        elif role == "student":
            return render(request, "Student/student_home.html", {"name": user_name})

    return render(request, "login.html")


def email_enter(request):
    return render(request,'Forgot Password/email_enter.html')

def code_enter(request):
    return render(request,'Forgot Password/code_enter.html',)

def reset_successful(request):
    return render(request,'Forgot Password/reset_successful.html')

def successful(request):
    return render(request,'Forgot Password/successful.html')


# Admin
def admin_dashboard(request):
    return render(request,'Admin/admin_dashboard.html')