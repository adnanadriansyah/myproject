from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
    get_permission_codename,
)
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import ProdukForm, KategoriForm, SupplierForm, PelangganForm
from .models import Produk, Kategori, Supplier, Pelanggan, Pesanan, DetailPesanan


# Create your views here.
def home(request):
    # Get recent/latest products for featured section
    produk_terbaru = Produk.objects.all().order_by("-id")[:6]
    total_produk = Produk.objects.count()

    # Get session data
    last_produk = request.session.get("last_produk")
    produk_count = request.session.get("produk_count", 0)

    context = {
        "produk_terbaru": produk_terbaru,
        "total_produk": total_produk,
        "last_produk": last_produk,
        "produk_count": produk_count,
    }
    return render(request, "appku/index.html", context)


@login_required
def produk_form(request):
    session_produk = request.session.get("last_produk")
    produk_count = request.session.get("produk_count", 0)

    if request.method == "POST":
        form = ProdukForm(request.POST)
        if form.is_valid():
            produk = form.save()
            request.session["last_produk"] = {
                "nama": produk.nama,
                "harga": produk.harga,
            }
            request.session["produk_count"] = produk_count + 1

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "message": "Produk berhasil disimpan",
                        "last_produk": request.session["last_produk"],
                        "produk_count": request.session["produk_count"],
                    }
                )
            return redirect("dashboard")

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "error": "Validasi gagal",
                    "fields": form.errors,
                },
                status=400,
            )
    else:
        form = ProdukForm()

    return render(
        request,
        "appku/produk_form.html",
        {
            "form": form,
            "session_produk": session_produk,
            "produk_count": produk_count,
        },
    )


def session_test(request):
    if request.method == "POST":
        nama = request.POST.get("nama")
        if nama:
            request.session["nama"] = nama
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "message": "Session berhasil disimpan.",
                        "nama": nama,
                    }
                )
            return HttpResponse("Session disimpan")

    return render(
        request,
        "appku/session_test.html",
        {
            "nama_session": request.session.get("nama"),
        },
    )


def cache_test(request):
    data = cache.get("test_data")
    if not data:
        data = "Data dari cache"
        cache.set("test_data", data, 300)  # cache for 5 minutes
    return HttpResponse(data)


def ajax_test(request):
    if request.method == "GET":
        return JsonResponse({"message": "Hello from AJAX"})
    return JsonResponse({"error": "Method not allowed"}, status=405)


def ajax_page(request):
    return render(request, "appku/ajax_test.html")


@login_required
def produk_list(request):
    produk_list = Produk.objects.all()
    return render(request, "appku/produk_list.html", {"produk_list": produk_list})


@login_required
def produk_edit(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == "POST":
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            messages.success(request, "Produk berhasil diperbarui.")
            return redirect("produk_list")
    else:
        form = ProdukForm(instance=produk)
    return render(request, "appku/produk_edit.html", {"form": form, "produk": produk})


@login_required
def produk_delete(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == "POST":
        produk.delete()
        messages.success(request, "Produk berhasil dihapus.")
        return redirect("produk_list")
    return render(request, "appku/produk_confirm_delete.html", {"produk": produk})


@login_required
def dashboard(request):
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group

    User = get_user_model()
    semua_produk = Produk.objects.all()
    semua_user = User.objects.all()
    semua_group = Group.objects.all()
    semua_kategori = Kategori.objects.all()
    semua_supplier = Supplier.objects.all()
    semua_pelanggan = Pelanggan.objects.all()
    semua_pesanan = Pesanan.objects.all()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create_user":
            username = request.POST.get("username")
            password = request.POST.get("password")
            groups = request.POST.getlist("groups")
            if username and password:
                if User.objects.filter(username=username).exists():
                    messages.error(request, f"User '{username}' sudah ada.")
                else:
                    user = User.objects.create_user(
                        username=username, password=password
                    )
                    for g_id in groups:
                        try:
                            group = Group.objects.get(id=g_id)
                            group.user_set.add(user)
                        except Group.DoesNotExist:
                            pass
                    messages.success(request, f"User '{username}' berhasil dibuat.")

        elif action == "create_group":
            group_name = request.POST.get("group_name")
            if group_name:
                if Group.objects.filter(name=group_name).exists():
                    messages.error(request, f"Group '{group_name}' sudah ada.")
                else:
                    Group.objects.create(name=group_name)
                    messages.success(request, f"Group '{group_name}' berhasil dibuat.")

        elif action == "add_kategori":
            nama = request.POST.get("nama")
            if nama:
                Kategori.objects.create(nama=nama)
                messages.success(request, f"Kategori '{nama}' berhasil dibuat.")

        elif action == "add_supplier":
            nama = request.POST.get("nama")
            kontak = request.POST.get("kontak", "") or ""
            telepon = request.POST.get("telepon", "") or ""
            email = request.POST.get("email", "") or ""
            if nama:
                Supplier.objects.create(
                    nama=nama, kontak=kontak, telepon=telepon, email=email
                )
                messages.success(request, f"Supplier '{nama}' berhasil dibuat.")

        elif action == "add_pelanggan":
            nama = request.POST.get("nama")
            kontak = request.POST.get("kontak", "") or ""
            telepon = request.POST.get("telepon", "") or ""
            email = request.POST.get("email", "") or ""
            if nama:
                Pelanggan.objects.create(
                    nama=nama, kontak=kontak, telepon=telepon, email=email
                )
                messages.success(request, f"Pelanggan '{nama}' berhasil dibuat.")

        elif action == "add_produk":
            nama = request.POST.get("nama")
            harga = request.POST.get("harga")
            kategori_id = request.POST.get("kategori")
            supplier_id = request.POST.get("supplier")
            stok = request.POST.get("stok", 0)
            if nama and harga:
                produk = Produk.objects.create(
                    nama=nama,
                    harga=int(harga),
                    kategori_id=kategori_id if kategori_id else None,
                    supplier_id=supplier_id if supplier_id else None,
                    stok=int(stok) if stok else 0,
                )
                messages.success(request, f"Produk '{nama}' berhasil ditambahkan.")

        elif action == "delete_produk":
            produk_id = request.POST.get("produk_id")
            try:
                produk = Produk.objects.get(id=produk_id)
                produk.delete()
                messages.success(request, "Produk dihapus.")
            except Produk.DoesNotExist:
                pass

        elif action == "delete_kategori":
            kategori_id = request.POST.get("kategori_id")
            try:
                kategori = Kategori.objects.get(id=kategori_id)
                kategori.delete()
                messages.success(request, "Kategori dihapus.")
            except Kategori.DoesNotExist:
                pass

        elif action == "delete_supplier":
            supplier_id = request.POST.get("supplier_id")
            try:
                supplier = Supplier.objects.get(id=supplier_id)
                supplier.delete()
                messages.success(request, "Supplier dihapus.")
            except Supplier.DoesNotExist:
                pass

        elif action == "delete_pelanggan":
            pelanggan_id = request.POST.get("pelanggan_id")
            try:
                pelanggan = Pelanggan.objects.get(id=pelanggan_id)
                pelanggan.delete()
                messages.success(request, "Pelanggan dihapus.")
            except Pelanggan.DoesNotExist:
                pass

        return redirect("dashboard")

    total_nilai = sum(p.harga * p.stok for p in semua_produk)
    context = {
        "total_produk": semua_produk.count(),
        "total_user": semua_user.count(),
        "total_group": semua_group.count(),
        "total_kategori": semua_kategori.count(),
        "total_supplier": semua_supplier.count(),
        "total_pelanggan": semua_pelanggan.count(),
        "total_pesanan": semua_pesanan.count(),
        "total_nilai": total_nilai,
        "produk_list": semua_produk.order_by("-id")[:8],
        "user_list": semua_user[:6],
        "group_list": semua_group,
        "kategori_list": semua_kategori,
        "supplier_list": semua_supplier,
        "pelanggan_list": semua_pelanggan[:6],
    }
    return render(request, "appku/dashboard.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Username atau password salah.")
    return render(request, "appku/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")
