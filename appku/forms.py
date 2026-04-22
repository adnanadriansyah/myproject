from django import forms
from .models import Produk, Kategori, Supplier, Pelanggan, Pesanan, DetailPesanan


class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ["nama", "harga", "kategori", "supplier", "stok", "deskripsi"]
        widgets = {
            "nama": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nama produk"}
            ),
            "harga": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Harga"}
            ),
            "kategori": forms.Select(attrs={"class": "form-control"}),
            "supplier": forms.Select(attrs={"class": "form-control"}),
            "stok": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Stok"}
            ),
            "deskripsi": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Deskripsi"}
            ),
        }


class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ["nama", "deskripsi"]
        widgets = {
            "nama": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nama kategori"}
            ),
            "deskripsi": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "Deskripsi"}
            ),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["nama", "kontak", "alamat", "telepon", "email"]
        widgets = {
            "nama": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nama supplier"}
            ),
            "kontak": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nama kontak"}
            ),
            "alamat": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "Alamat"}
            ),
            "telepon": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Telepon"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
        }


class PelangganForm(forms.ModelForm):
    class Meta:
        model = Pelanggan
        fields = ["nama", "kontak", "alamat", "telepon", "email"]
        widgets = {
            "nama": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nama pelanggan"}
            ),
            "kontak": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nama kontak"}
            ),
            "alamat": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "Alamat"}
            ),
            "telepon": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Telepon"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
        }


class PesananForm(forms.ModelForm):
    class Meta:
        model = Pesanan
        fields = ["pelanggan", "status"]
        widgets = {
            "pelanggan": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class DetailPesananForm(forms.ModelForm):
    class Meta:
        model = DetailPesanan
        fields = ["produk", "quantity"]
        widgets = {
            "produk": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.harga_saat_itu = None

    def clean(self):
        cleaned_data = super().clean()
        produk = cleaned_data.get("produk")
        quantity = cleaned_data.get("quantity")
        if produk and quantity:
            cleaned_data["harga_saat_itu"] = produk.harga
            cleaned_data["subtotal"] = produk.harga * quantity
        return cleaned_data
