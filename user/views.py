from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import User

# Create your views here.


def index(request):
    return JsonResponse({'code': 200, 'data': "Hello"}, status=200)


def sign_up(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except ValueError:
            return JsonResponse({
                'code': 400,
                'data': "Format Error"
            },
                                status=400)
        name = body["name"]
        password = body["password"]
        role = body["role"]
        if User.objects.filter(name=name, role=role).first():
            return JsonResponse({
                'code': 400,
                'data': "Sign up failed!"
            },
                                status=400)
        user = User(name=name, password=password, role=role)
        user.full_clean()
        user.save()
        return JsonResponse({
            'code': 200,
            'data': "Sign up succeeded!"
        },
                            status=200)


def sign_in(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except ValueError:
            return JsonResponse({
                'code': 400,
                'data': "Format Error"
            },
                                status=400)
        name = body["name"]
        password = body["password"]
        role = body["role"]
        if not User.objects.filter(name=name, password=password,
                                   role=role).first():
            return JsonResponse({
                'code': 400,
                'data': "Sign in failed!"
            },
                                status=400)
        return JsonResponse({
            'code': 200,
            'data': "Sign in succeeded!"
        },
                            status=200)


def read_user(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            name = body["name"]
            role = body["role"]
        except ValueError:
            return JsonResponse({
                'code': 400,
                'data': "Format Error"
            },
                                status=400)

        if not User.objects.filter(name=name, role=role).first():
            return JsonResponse({
                'code': 400,
                'data': "Read failed!"
            },
                                status=400)
        return JsonResponse({
            'code': 200,
            'data': {
                'name': name,
                'role': role
            }
        },
                            status=200)


def read_all_user(request):
    return JsonResponse(
        {
            'code':
            200,
            'data': [{
                "name": user.name,
                "password": user.password,
                "role": user.role
            } for user in User.objects.all()]
        },
        status=200)
