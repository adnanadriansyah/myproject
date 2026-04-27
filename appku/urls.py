from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("produk/", views.produk_form, name="produk_form"),
    path("produk/list/", views.produk_list, name="produk_list"),
    path("produk/<int:pk>/edit/", views.produk_edit, name="produk_edit"),
    path("produk/<int:pk>/delete/", views.produk_delete, name="produk_delete"),
    path("pesanan/", views.pesanan_list, name="pesanan_list"),
    path("pesanan/create/", views.pesanan_create, name="pesanan_create"),
    path("pesanan/<int:pk>/", views.pesanan_detail, name="pesanan_detail"),
    path("pesanan/<int:pk>/edit/", views.pesanan_update, name="pesanan_update"),
    path("pesanan/<int:pk>/delete/", views.pesanan_delete, name="pesanan_delete"),
    path("pesanan/<int:pk>/add-item/", views.pesanan_add_item_ajax, name="pesanan_add_item_ajax"),
    path("session/", views.session_test, name="session_test"),
    path("cache/", views.cache_test, name="cache_test"),
    path("ajax/", views.ajax_test, name="ajax_test"),
    path("ajax-page/", views.ajax_page, name="ajax_page"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
