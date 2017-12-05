from dashboard.models import Warehouse, Store,Product,SFOProduct
from rest_framework import serializers


class WarehouseSerializer(serializers.ModelSerializer):
    warehouse_id = serializers.IntegerField(source='id')
    class Meta:
        model = Warehouse
        fields = ('warehouse_id','name','created_by',)

class StoreSerializer(serializers.ModelSerializer):
    store_id = serializers.IntegerField(source='id')
    class Meta:
        model = Store
        fields = ('store_id', 'name', 'created_by')


class ProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='id')
    class Meta:
        model = Product
        fields = ('product_id', 'vendor_product_id', 'warehouse', 'store','bin_location','product_name',
                  'barcode_num','description','quantity','quantityindisplay','user_id',
                  'picklist','sku','unit','tote','store_number','Conversion')


class ProductPickSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('store','picklist',)


class SFOProductSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField(source='id')

    class Meta:
        model = SFOProduct
        fields = ('product_id','bin','quantityinhand', 'primary_stock','Conversion','primary_vendor','name')