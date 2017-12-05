from django.conf.urls import url
from . import views
from dashboard.views import home
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from forms import LoginForm

urlpatterns = [

    url(r'^login/$', login, {'template_name': 'components/login.html', 'authentication_form': LoginForm}),
    url(r'^home/$', home, name="home"),
    url(r'^addwarehouse/$',login_required(views.AddWarehouse.as_view()), name='add_warehouse'),
    url(r'^editstore/(?P<pk>\d+)/$', views.EditStore.as_view(), name="edit_store"),
    url(r'^addstore/$', login_required(views.AddStore.as_view()), name='add_store'),
    url(r'^warehouselist', views.WarehouseList.as_view(), name='warehouse_list'),
    url(r'^storelist', views.StoreList.as_view(), name='store_list'),
    url(r'^editstore/(?P<pk>\d+)/$', views.EditStore.as_view(), name="edit_store"),
    url(r'^editwarehouse/(?P<pk>\d+)/$', views.EditWarehouse.as_view(), name="edit_warehouse"),
    url(r'^apikey', views.Apikeylist.as_view(), name="edit_apikey"),
    url(r'^editkey/(?P<pk>\d+)/$', views.EditKEY.as_view(), name="edit_key"),
    url(r'^exportcsv', views.ExportCSV.as_view(), name="export_csv"),
    url(r'^exportreport', views.ExportReport.as_view(), name="export_report"),
    url(r'^adduser', views.AddUser.as_view(), name="add_user"),
    url(r'^userlist', views.UserList.as_view(), name="list_user"),
    url(r'^delstore/(?P<pk>\d+)/$', views.DeleteStore.as_view(), name="store_delete"),
    url(r'^delwarehouse/(?P<pk>\d+)/$', views.DeleteWarehouse.as_view(), name="warehouse_delete"),
    url(r'^deluser/(?P<pk>\d+)/$', views.DeleteUser.as_view(), name="user_delete"),
    url(r'^edituser/(?P<pk>\d+)/$', views.EditUser.as_view(), name="user_delete"),

    #Product Edit

    url(r'^productlist', views.ProductList.as_view(), name='product_list'),
    url(r'^editproduct/(?P<pk>\d+)/$', views.EditProduct.as_view(), name="product_edit"),

    #sfoProduct Edit

    url(r'^sfoproductlist', views.SFOProductList.as_view(), name='sfoproduct_list'),
    url(r'^sfoeditproduct/(?P<pk>\d+)/$', views.SFOEditProduct.as_view(), name="sfoproduct_edit"),


]
#Apikeylist

