from django.shortcuts import render
from django.db import connection


def index(request):
    return render(request, "index.html")


def entity(request):
    return render(request, "entity.html")


def equipment_type(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM equipment_type')
            rows = cursor.fetchall()
    finally:
        cursor.close()
    print(rows)
    return render(request, "entity.html")
