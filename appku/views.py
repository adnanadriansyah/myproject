from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import ProdukForm
from .models import Produk

# Create your views here.
def home(request):
    return render(request, 'appku/index.html')

@login_required
def produk_form(request):
    session_produk = request.session.get('last_produk')
    produk_count = request.session.get('produk_count', 0)

    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            produk = form.save()
            request.session['last_produk'] = {
                'nama': produk.nama,
                'harga': produk.harga,
            }
            request.session['produk_count'] = produk_count + 1

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'message': 'Produk berhasil disimpan',
                    'last_produk': request.session['last_produk'],
                    'produk_count': request.session['produk_count'],
                })
            return HttpResponse('Produk berhasil disimpan')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'error': 'Validasi gagal',
                'fields': form.errors,
            }, status=400)
    else:
        form = ProdukForm()

    return render(request, 'appku/produk_form.html', {
        'form': form,
        'session_produk': session_produk,
        'produk_count': produk_count,
    })

def session_test(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        if nama:
            request.session['nama'] = nama
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'message': 'Session berhasil disimpan.',
                    'nama': nama,
                })
            return HttpResponse('Session disimpan')

    return render(request, 'appku/session_test.html', {
        'nama_session': request.session.get('nama'),
    })

def cache_test(request):
    data = cache.get('test_data')
    if not data:
        data = 'Data dari cache'
        cache.set('test_data', data, 300)  # cache for 5 minutes
    return HttpResponse(data)

def ajax_test(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Hello from AJAX'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def ajax_page(request):
    return render(request, 'appku/ajax_test.html')

@login_required
def produk_list(request):
    produk_list = Produk.objects.all()
    return render(request, 'appku/produk_list.html', {'produk_list': produk_list})

@login_required
def produk_edit(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diperbarui.')
            return redirect('produk_list')
    else:
        form = ProdukForm(instance=produk)
    return render(request, 'appku/produk_edit.html', {'form': form, 'produk': produk})

@login_required
def produk_delete(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        produk.delete()
        messages.success(request, 'Produk berhasil dihapus.')
        return redirect('produk_list')
    return render(request, 'appku/produk_confirm_delete.html', {'produk': produk})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username atau password salah.')
    return render(request, 'appku/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
