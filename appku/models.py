from django.db import models
from django.contrib.auth.models import User


class Kategori(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, default="")

    def __str__(self):
        return self.nama


class Supplier(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama = models.CharField(max_length=200)
    kontak = models.CharField(max_length=100, blank=True, default="")
    alamat = models.TextField(blank=True, default="")
    telepon = models.CharField(max_length=20, blank=True, default="")
    email = models.EmailField(blank=True, default="")

    def __str__(self):
        return self.nama


class Pelanggan(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama = models.CharField(max_length=200)
    kontak = models.CharField(max_length=100, blank=True, default="")
    alamat = models.TextField(blank=True, default="")
    telepon = models.CharField(max_length=20, blank=True, default="")
    email = models.EmailField(blank=True, default="")

    def __str__(self):
        return self.nama


class Produk(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama = models.CharField(max_length=100)

    # 🔥 gunakan Decimal untuk uang
    harga = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="produks",
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="produks",
    )

    stok = models.PositiveIntegerField(default=0)  # 🔥 tidak bisa minus
    deskripsi = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama


class Pesanan(models.Model):
    id = models.BigAutoField(primary_key=True)

    STATUS_CHOICES = [
        ("pending", "Menunggu"),
        ("processing", "Diproses"),
        ("completed", "Selesai"),
        ("cancelled", "Dibatalkan"),
    ]

    pelanggan = models.ForeignKey(
        Pelanggan, on_delete=models.CASCADE, related_name="pesanans"
    )

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="pesanans"
    )

    total_harga = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pesanan #{self.id}"


class DetailPesanan(models.Model):
    id = models.BigAutoField(primary_key=True)

    pesanan = models.ForeignKey(
        Pesanan,
        on_delete=models.CASCADE,
        related_name="details"  # 🔥 ini penting
    )

    produk = models.ForeignKey(
        Produk,
        on_delete=models.CASCADE,
        related_name="detail_pesanans"
    )

    quantity = models.PositiveIntegerField(default=1)

    harga_saat_itu = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.pesanan} - {self.produk}"
