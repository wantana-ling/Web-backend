from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User
import json

@csrf_exempt
def register_api(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # ตรวจสอบว่ามีข้อมูลครบถ้วนหรือไม่
        if not username or not email or not password:
            return JsonResponse({"message": "Missing required fields"}, status=400)

        # ตรวจสอบว่าอีเมลมีอยู่ในฐานข้อมูลแล้วหรือไม่
        if User.objects.filter(email=email).exists():
            return JsonResponse({"message": "Email already exists"}, status=400)

        # สร้างผู้ใช้ใหม่ในฐานข้อมูล (เก็บรหัสผ่านแบบธรรมดา)
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

        # ตรวจสอบว่ามีข้อมูลครบถ้วนหรือไม่
        if not email or not password:
            return JsonResponse({"message": "Missing required fields"}, status=400)

        # ค้นหาผู้ใช้ที่มีอีเมลที่ตรงกับที่กรอก
        user = User.objects.filter(email=email).first()

        if not user:
            return JsonResponse({"message": "Email not found"}, status=400)

        # ตรวจสอบว่า รหัสผ่านที่กรอกตรงกับรหัสผ่านที่เก็บไว้ในฐานข้อมูลหรือไม่
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
        user_id = request.GET.get("user_id")  # รับ user_id จาก URL parameter

        # ค้นหาผู้ใช้ในฐานข้อมูลตาม user_id
        user = User.objects.filter(id=user_id).first()

        if not user:
            return JsonResponse({"message": "User not found"}, status=404)

        # ส่งข้อมูลผู้ใช้กลับมาใน response
        user_info = {
            "username": user.username,
            "email": user.email,
            "user_id": user.id
        }

        return JsonResponse(user_info, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)
