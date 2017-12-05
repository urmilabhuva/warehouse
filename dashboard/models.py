from django.db import models
from django.contrib.auth.models import *


class Warehouse(models.Model):
    """
        Warehosue Detail
    """
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=200,blank=True, null= True)
    is_delete = models.BooleanField(default=False)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Warehouse"


class Store(models.Model):
    """
        Maintain Store Detail
    """
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    is_delete = models.BooleanField(default=False)
    warehouse =  models.ForeignKey(Warehouse)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Store"


class ApiKey(models.Model):
    """
        This model is used hold key and  and secret key
    """
    apikey = models.TextField(max_length=300)
    apisec = models.TextField(max_length=300)

    class Meta:
        db_table = "ApiKey"


class Product(models.Model):

    """
        Product Detail Fetch from api
    """
    vendor_product_id = models.CharField(max_length=200)
    warehouse = models.ForeignKey(Warehouse)
    store = models.ForeignKey(Store)
    bin_location = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    barcode_num = models.CharField(max_length=60)
    description = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.CharField(max_length=255)
    quantityindisplay = models.CharField(max_length=50,blank=True,null=True)
    user_id  = models.ForeignKey(User)
    picklist = models.CharField(max_length=255)
    sku =  models.CharField(max_length=255)
    unit = models.CharField(max_length=255,blank=True, null=True)
    tote = models.CharField(max_length=30, null=True, blank=True)
    store_number = models.CharField(max_length=30)
    primary_stock = models.CharField(max_length=255, blank=True, null=True)  # fetch from SFO table
    Conversion = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    ingredienttoproduct = models.CharField(max_length=200,default='No')
    updatecost =  models.CharField(max_length=200,default='Yes')
    is_ingredient =   models.CharField(max_length=200,default='No')



    class Meta:
        db_table = "Product"


class Acluser(models.Model):
    """
        This model is used hold key and  and secret key
    """
    user = models.ForeignKey(User)
    warehouse = models.ForeignKey(Warehouse)
    store = models.ForeignKey(Store)
    contactnumber = models.CharField(max_length=255)

    class Meta:
        db_table = "Acluser"


class SFOProduct(models.Model):

    sid = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    bin = models.CharField(max_length=255, blank=True, null=True)
    primary_vendor = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=False)
    export_unit = models.CharField(max_length=255, blank=True, null=True)
    threshold = models.IntegerField(blank=True, null=True)
    quantityinhand = models.IntegerField(blank=True, null=True)
    quantityinlayaway = models.CharField(max_length=255, blank=True, null=True)
    quantityforsale = models.IntegerField(blank=True, null=True)
    currentcost = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, default=0)
    totalvalue = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, default=0)
    reorder_unit = models.CharField(max_length=255, blank=True, null=True)
    primary_stock = models.CharField(max_length=255, blank=True, null=True)#fetch from uom
    Conversion = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "SFOProduct"

class Device(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    dtoken = models.CharField(max_length=255, blank=True, null=True)
    did = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


