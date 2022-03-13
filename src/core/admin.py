import json

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from core.models import Cve, Cwe, Product, Vendor


class BaseReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Cve)
class CveAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    search_fields = ['cve_id', 'summary']
    list_display = (
        "cve_id",
        "summary",
        "updated_at",
        "cvss2",
        "cvss3",
    )
    ordering = ("-updated_at",)
    fields = (
        "cve_id",
        "summary",
        "created_at",
        "updated_at",
        "cvss2",
        "cvss3",
        "vendors",
        "cwes",
        "json_pre",
    )

    def view_on_site(self, obj):
        return reverse("cve", kwargs={"cve_id": obj.cve_id})

    @admin.display(description="Json")
    def json_pre(self, obj):
        return format_html(
            "<pre>{}</pre>", json.dumps(obj.json, indent=2, sort_keys=True)
        )


@admin.register(Cwe)
class CweAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    search_fields = ['cwe_id', 'name', 'description']
    list_display = (
        "cwe_id",
        "name",
    )
    fields = (
        "cwe_id",
        "name",
        "description",
        "created_at",
        "updated_at",
    )


@admin.register(Vendor)
class VendorAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    ordering = ("name",)
    search_fields = ['name']
    list_display = (
        "name",
        "human_name",
        "created_at"
    )
    fields = (
        "name",
        "human_name",
        "created_at",
        "updated_at",
    )


@admin.register(Product)
class ProductAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    ordering = ("name",)
    search_fields = ['name']
    list_display = (
        "human_name",
        "get_vendor_name",
        "created_at"
    )
    fields = (
        "name",
        "human_name",
        "created_at",
        "updated_at",
    )

    def get_vendor_name(self, obj):
        return obj.vendor.human_name

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("vendor")