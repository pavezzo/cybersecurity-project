from pathlib import Path

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db import connection
from django.db.utils import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import render, redirect

from django_ratelimit.decorators import ratelimit

from cybersecproject.settings import BASE_DIR
from .models import Picture


@login_required
def index_handler(req: HttpRequest) -> HttpResponse:
    files = []
    if Picture.objects.filter(owner=req.user).exists():
        files = Picture.objects.filter(owner=req.user)

    return render(req, "pages/index.html", {"files": files})


@login_required
def add_handler(req: HttpRequest) -> HttpResponse:
    if req.method == "POST":
        desc = req.POST.get("description")
        pic = req.FILES["picture"]
        name = pic.name
        username = req.user.username
        try:
            p = Picture(owner=req.user, description=desc, name=name)
            p.save()
        except IntegrityError:
            error = "Picture name is not unique!"
            return render(req, "pages/add.html", {"error": error})

        Path(f"{BASE_DIR}/static/{username}").mkdir(exist_ok=True)
        with open(f"{BASE_DIR}/static/{username}/{name}", "wb+") as dest:
            for chunk in pic.chunks():
                dest.write(chunk)
    elif req.method == "GET":
        return render(req, "pages/add.html", {"error": None})

    return redirect("/")


def create_user_handler(req: HttpRequest) -> HttpResponse:
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")

        # password = make_password(password)

        user = User(username=username, password=password)
        user.save()
        return redirect("/login")
    elif req.method == "GET":
        return render(req, "pages/create_user.html")

    return redirect("/")


# @ratelimit(key="ip", rate="5/m", method="POST", block=True)
def login_handler(req: HttpRequest) -> HttpResponse:
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            error = "No such user exists!"
            return render(req, "pages/login.html", {"error": error})

        if user.password != password:
            error = "Wrong password!"
            return render(req, "pages/login.html", {"error": error})

        # if not check_password(password, user.password):
        #     error = "Wrong password!"
        #     return render(req, "pages/login.html", {"error": error})

        login(req, user)
        return redirect("/")

    return render(req, "pages/login.html", {"error": None})


def logout_handler(req: HttpRequest) -> HttpResponse:
    logout(req)
    return redirect("/")


@login_required
def view_handler(req: HttpRequest) -> HttpResponse:
    if req.method == "GET":
        name = req.GET.get("name", "")
        if not name:
            return redirect("/")

        # if Picture.objects.filter(owner=req.user, name=name).exists():
        #     res = Picture.objects.filter(owner=req.user, name=name)[0]
        #     return render(req, "pages/view.html", {"name": res.name, "desc": res.description})
        # else:
        #     return HttpResponseNotFound("Picture not found")

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM project_picture WHERE name = '{name}'")
            res = cursor.fetchall()

        if res:
            res = res[0]
            return render(req, "pages/view.html", {"name": res[0], "desc": res[1]})
        else:
            return HttpResponseNotFound("Picture not found")

    return redirect("/")


@login_required
def admin_panel_handler(req: HttpRequest) -> HttpResponse:
    # if not req.user.is_staff:
    #     return HttpResponseForbidden("User not admin")

    if req.method == "GET":
        users = None
        if User.objects.filter().exists():
            users = User.objects.filter()
        pics = None
        if Picture.objects.filter().exists():
            pics = Picture.objects.filter()

        return render(req, "pages/admin.html", {"users": users, "pictures": pics})

    return HttpResponseNotAllowed()

