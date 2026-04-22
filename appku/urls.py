from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("produk/", views.produk_form, name="produk_form"),
    path("produk/list/", views.produk_list, name="produk_list"),
    path("produk/<int:pk>/edit/", views.produk_edit, name="produk_edit"),
    path("produk/<int:pk>/delete/", views.produk_delete, name="produk_delete"),
    path("session/", views.session_test, name="session_test"),
    path("cache/", views.cache_test, name="cache_test"),
    path("ajax/", views.ajax_test, name="ajax_test"),
    path("ajax-page/", views.ajax_page, name="ajax_page"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
