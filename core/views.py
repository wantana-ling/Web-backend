from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User
from .models import CoreDetail
from .models import Donation
import json
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Home Page!")

@csrf_exempt
def register_api(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return JsonResponse({"message": "Missing required fields"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"message": "Email already exists"}, status=400)

        user = User.objects.create(username=username, email=email, password=password)

        return JsonResponse({"message": "registered", "user_id": user.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)


@csrf_exempt
def login_api(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({"message": "Missing required fields"}, status=400)

        user = User.objects.filter(email=email).first()

        if not user:
            return JsonResponse({"message": "Email not found"}, status=400)

        if user.password != password:
            return JsonResponse({"message": "Incorrect password"}, status=400)

        return JsonResponse({"message": "Login successful", "user_id": user.id}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)
    
@csrf_exempt
def get_user_info(request):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        user_id = request.GET.get("user_id")

        user = User.objects.filter(id=user_id).first()

        if not user:
            return JsonResponse({"message": "User not found"}, status=404)

        user_info = {
            "username": user.username,
            "rank":user.rank
        }

        return JsonResponse(user_info, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)

@csrf_exempt
def get_all_product_details(request):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        products = CoreDetail.objects.all()

        product_data = []
        for product in products:
            product_data.append({
                "id": product.id,
                "product_name": product.product_name,
                "product_description": product.product_description,
                "product_price": product.product_price,
                "product_rank": product.product_rank,
            })

        return JsonResponse({"products": product_data}, status=200)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

@csrf_exempt
def get_product_names(request):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        products = CoreDetail.objects.all()

        product_names = []
        for product in products:
            product_names.append({
                "id": product.id,
                "product_name": product.product_name,
                "color": product.product_color
            })

        return JsonResponse({"products": product_names}, status=200)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

@csrf_exempt
def get_product_details_by_id(request, product_id):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        product = CoreDetail.objects.filter(id=product_id).first()

        if not product:
            return JsonResponse({"message": f"Product with ID {product_id} not found"}, status=404)

        product_info = {
            "id": product.id,
            "product_name": product.product_name,
            "product_description": product.product_description,
            "product_price": product.product_price,
            "product_rank": product.product_rank,
            "product_color": product.product_color,
        }

        return JsonResponse(product_info, status=200)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)
    
@csrf_exempt
def get_user_all_info(request):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        user_id = request.GET.get("user_id")

        user = User.objects.filter(id=user_id).first()

        if not user:
            return JsonResponse({"message": "User not found"}, status=404)

        user_info = {
            "username": user.username,
            "email": user.email,
            "rank":user.rank
        }

        return JsonResponse(user_info, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)

@csrf_exempt
def update_username(request):
    if request.method != "PUT":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)

        user_id = data.get("user_id")
        new_username = data.get("username")

        if not user_id or not new_username:
            return JsonResponse({"message": "Missing required fields"}, status=400)

        user = User.objects.filter(id=user_id).first()

        if not user:
            return JsonResponse({"message": "User not found"}, status=404)

        user.username = new_username
        user.save()

        return JsonResponse({"success": True, "message": "Username updated successfully!"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON format"}, status=400)

    except Exception as e:
        return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=500)
    
@csrf_exempt
def delete_user(request):
    if request.method != "DELETE":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        if request.body:
            try:
                data = json.loads(request.body)
                user_id = data.get("user_id")
            except json.JSONDecodeError:
                return JsonResponse({"message": "Invalid JSON format"}, status=400)
        else:
            user_id = None

        if not user_id:
            user_id = request.GET.get("user_id")

        if not user_id:
            return JsonResponse({"message": "Missing user_id"}, status=400)

        print(f"Delete user called with user_id: {user_id}")

        try:
            user_id_int = int(user_id)
        except ValueError:
            return JsonResponse({"message": "Invalid user_id"}, status=400)

        user = User.objects.filter(id=user_id_int).first()

        if not user:
            return JsonResponse({"message": "User not found"}, status=404)

        user.delete()

        return JsonResponse({"success": True, "message": "User deleted successfully!"}, status=200)

    except Exception as e:
        return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=500)
    
@csrf_exempt
def add_donation(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        product_id = data.get("product_id")
        amount = data.get("amount")
        note = data.get("note", "")

        if not user_id or not amount:
            return JsonResponse({"message": "Missing required fields"}, status=400)

        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({"message": "User not found"}, status=404)

        product = CoreDetail.objects.filter(id=product_id).first() if product_id else None

        donation = Donation.objects.create(
            user=user,
            product=product,
            amount=amount,
            note=note
        )

        return JsonResponse({"success": True, "message": "Donation added successfully", "donation_id": donation.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON format"}, status=400)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

@csrf_exempt
def update_rank(request):
    if request.method != "PUT":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)

        user_id = data.get("user_id")
        new_rank = data.get("rank")

        if not user_id or new_rank is None:
            return JsonResponse({"message": "Missing required fields"}, status=400)

        user = User.objects.filter(id=user_id).first()

        if not user:
            return JsonResponse({"message": "User not found"}, status=404)

        user.rank = new_rank
        user.save()

        return JsonResponse({"success": True, "message": "Rank updated successfully!"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON format"}, status=400)

    except Exception as e:
        return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=500)

@csrf_exempt
def get_all_donations(request):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        donations = Donation.objects.select_related("user", "product").all().order_by("-timestamp")
        data = []
        for d in donations:
            data.append({
                "user": d.user.username,
                "product_name": d.product.product_name if d.product else "N/A",
                "amount": float(d.amount),
                "timestamp": d.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "note": d.note,
            })
        return JsonResponse({"donations": data}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)
