import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.views.generic import TemplateView
from django.views.generic import View
from django.contrib.auth import authenticate
from product.settings import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms import LoginForm
import urllib2
import json
from.models import *
from django.http import HttpResponse
import xlwt
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
import  datetime
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
import html
from html5lib import treebuilders, inputstream
import xlrd
from django.db.models import Q
#finalurl = apiurl + get_text + apikey

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    data = Context(context_dict)

    html  = template.render(data)
    html = html.encode("UTF-8")
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return HttpResponse('We had some errors<pre>%s</pre>' % html.escape(html))

@login_required(login_url="/")
def home(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            context = {}
            war = Warehouse.objects.filter(is_delete=False)
            str = Store.objects.filter(is_delete=False)
            context.update({"title":"warehouse", "store":str,"warehouse":war})
            return render(request, 'components/fetch_product.html', context)

    if request.method == "POST" and not 'xls' in request.POST and not 'uom' in request.POST:
        context = {}
        validate = True

        storeselect = request.POST.get('store', None)
        wareselect = request.POST.get('ware', None)
        get_text = request.POST.get('ponumber', None)


        if request.user.is_authenticated:

            if wareselect == "000":
                validate = False
                context.update({"houseware": "Please select  warehouse"})

            if storeselect == "00":
                validate = False
                context.update({"storeware": "Please select store"})

            if not get_text:
                validate=False
                context.update({"number":"Please enter purchaseorder number"})

            if validate:
                #urlfull = "https://pgconcessions.revelup.com/resources/PurchaseOrder/" + get_text + "/?api_key=d77d367b015049bb9cb931efcbbc2077&api_secret=97295c7b675a4644a906d3782462646f6254d1651b5a478a8594a8c67640ab79"
                urlfull = apiurl + get_text + apikey
                print urlfull
                try:
                    resp = urllib2.urlopen(urlfull)
                    print resp
                except:
                    war = Warehouse.objects.filter(is_delete=False)
                    strob = Store.objects.filter(is_delete=False)

                    context.update(
                        {"title": "warehouse", "store": strob, "warehouse": war, "Error": "Please enter Valid Po Number"})
                    return render(request, 'components/fetch_product.html', context)

                if resp.code != 200:
                    war = Warehouse.objects.filter(is_delete=False)
                    strob = Store.objects.filter(is_delete=False)

                    context.update({"title": "warehouse","store": strob,  "warehouse": war,"Error":"Please enter Valid Po Number"})
                    return render(request, 'components/fetch_product.html', context)

                b = json.load(resp)

                val = []
                Store_Number = ''
                for key, value in b.iteritems():
                    if key == 'id':
                        print key, value
                    if key == 'orderitems':
                        # print key,value
                        val.append(value)
                    if key == 'establishment':
                        valuestore = list(value)
                        print "wsew",valuestore
                        Store_Number_list = ''.join(valuestore)
                        Store_Number = (Store_Number_list)[26:-1]
                        print "prakash", Store_Number
                        #Store_Number = (list(value))[26:-1]

                # print "prakash", Store_Number
                data = {}
                final_data = []
                q = 0.0
                con = "unit"
                for li in val:
                    for h in li:
                        # data.update({'Id':get_text,'Vendor_Item_Id':h['vendor_item_id'],'Quantitiy': h['quantity'], 'Reorder_Unit': h['reorder_unit']})
                        if h['product']:
                            #if h['reorder_unit_type'] is not None:
                                #print "kk"
                                # urlconverse = apiurl2 + h['reorder_unit_type'] + apikey2
                                #
                                # respconverse = urllib2.urlopen(urlconverse)
                                # finldata = json.load(respconverse)
                                # if finldata.get('conversion') != 'null':
                                #     con = float(finldata.get('conversion'))
                                #     con = int(round(con))
                                # conversion = finldata.get('key') + '(' + str(con) + h['product']['uom'] + ')'
                                #
                                # q = float(h['quantity'])
                                # final_data.append({'id': get_text, 'Store_Number': Store_Number,
                                #                    'Vendor_Item_Id': h['vendor_item_id'], 'Quantitiy': round(q),
                                #                    'Reorder_Unit': conversion, 'Bin_Value': h['product']['bin_value'],
                                #                    'Sku': h['product']['sku'], 'Barcode': h['product']['barcode'],
                                #                    'Description': h['product']['name']})
                            print "if",h['quantity']
                            q = float(h['quantity'])
                            final_data.append(
                                {'id': get_text, 'Store_Number': Store_Number,
                                 'Vendor_Item_Id': h['vendor_item_id'],
                                 'Quantitiy': round(q), 'Reorder_Unit': "null",
                                 'Bin_Value': h['product']['bin_value'],
                                 'Sku': h['product']['sku'], 'Barcode': h['product']['barcode'],
                                 'Description': h['product']['name']})
                        else:
                            print "else",h['quantity']
                            q = float(h['quantity'])
                            final_data.append(
                                {'id': get_text, 'Store_Number': Store_Number, 'Vendor_Item_Id': h['vendor_item_id'],
                                 'Quantitiy': round(q), 'Reorder_Unit': "null", 'Bin_Value': "null", 'Sku': "null",
                                 'Barcode': "null", 'Description': "null"})

                print "finaldata",final_data

                storeobj = Store.objects.get(id=storeselect)
                warobj = Warehouse.objects.get(id=wareselect)
                userobj = User.objects.get(id=request.user.id)

                count = 0
                for item in final_data:

                    binvalue = None
                    if  not item['Barcode'] is None:
                        try:
                            sfproobj = SFOProduct.objects.get(Q(barcode=item['Barcode']) | Q(sku=item['Sku']))
                            print "sfofound", sfproobj
                            if not item['Bin_Value']:
                                print "sss",sfproobj
                                if sfproobj is not None:
                                    binvalue = sfproobj.bin
                            else:
                                 binvalue = item['Bin_Value']




                            if sfproobj:
                                # if binvalue:
                                #     print "bin try"
                                # if sfproobj.quantityinhand > 0:
                                #     print "sfproobj.quantityinhand"
                                # if item['Quantitiy'] > 0:
                                #     print "Quantiti"

                                print sfproobj.quantityinhand
                                if sfproobj.quantityinhand > 0 and item['Quantitiy'] > 0 and binvalue :

                                    count = count + 1
                                    print count

                                    poobj = Product.objects.filter(barcode_num = item['Barcode'],picklist= get_text)
                                    print poobj

                                    if len(poobj) > 0:
                                        print "update"
                                        for po in poobj:
                                           po.store_number = item['Store_Number'],
                                           po.bin_location= binvalue,
                                           po.vendor_product_id = item['Vendor_Item_Id'],
                                           po.sku = item['Sku'],
                                           po.barcode_num = item['Barcode'],
                                           po.description = item['Description'],
                                           po.quantityindisplay = item['Quantitiy'],
                                           po.unit = sfproobj.primary_stock,
                                           po.warehouse = warobj,
                                           po.user_id = userobj,
                                           po.primary_stock=sfproobj.primary_stock,
                                           po.Conversion=sfproobj.Conversion,
                                           po.store = storeobj
                                           po.save()
                                           # print "+++++++update"
                                    else:

                                        # print "create"


                                        Product.objects.create(picklist=item['id'],store_number = item['Store_Number'],
                                                               bin_location= binvalue,
                                                               vendor_product_id = item['Vendor_Item_Id'],
                                                               sku = item['Sku'],
                                                               barcode_num = item['Barcode'],
                                                               description = item['Description'],
                                                               quantityindisplay = item['Quantitiy'],
                                                               unit = sfproobj.primary_stock,
                                                               warehouse = warobj,
                                                               user_id = userobj,
                                                               primary_stock=sfproobj.primary_stock,
                                                               Conversion=sfproobj.Conversion,
                                                               store = storeobj)

                        except:
                            pass


                warpage = Warehouse.objects.filter(is_delete=False)
                strpage = Store.objects.filter(is_delete=False)

                MSG = "Sucessfully added"
                context.update({"title": "warehouse","store": strpage,  "warehouse": warpage, "success":MSG, "record":"record","count":count})
                return render(request, 'components/fetch_product.html', context)


            else:
                war = Warehouse.objects.filter(is_delete=False)
                str = Store.objects.filter(is_delete=False)

                context.update({"title": "warehouse", "store": str, "warehouse": war})
                return render(request, 'components/fetch_product.html', context)

    elif request.method == "POST" and 'uom' in request.POST:
        print "here uom"
        if request.FILES['prxls']:
            context = {}
            psu = ""
            cf = ""
            warpage = Warehouse.objects.filter(is_delete=False)
            strpage = Store.objects.filter(is_delete=False)
            try:
                input_excel = request.FILES['prxls']

                book = xlrd.open_workbook(file_contents=input_excel.read())

                sheet = book.sheet_by_index(0)
                keys = [sheet.cell(0, col_index).value for col_index in xrange(sheet.ncols)]
                #print "keys are", keys
                if len(keys) > 0:
                    userobj = User.objects.get(id=request.user.id)
                    dict_list = []
                    count = 0
                    for row_index in xrange(1, sheet.nrows):
                        d = {keys[col_index]: sheet.cell(row_index, col_index).value
                             for col_index in xrange(sheet.ncols)}

                        if d['Conversion factor']:
                            #count = count + 1

                            con = int(round(d['Conversion factor']))

                            uom =  (d['Unit of Measurement'].encode('ascii','ignore'))

                            re  = con.__str__() + uom


                            sfoproductobj = SFOProduct.objects.filter(Q(barcode=d['Barcode']) | Q(sku=d['SKU']))
                            if sfoproductobj:
                                #print "SFOproduct found"

                                if d['Conversion factor']:
                                    cf = int(d['Conversion factor'])
                                else:
                                    cf =d['Conversion factor']

                                for sfproobj in sfoproductobj:
                                    #print "inside SFOproduct found"

                                    sfproobj.reorder_unit = re
                                    sfproobj.primary_stock = d['Primary stock unit name']
                                    sfproobj.Conversion = cf
                                    sfproobj.save()
                                    count = count + 1

                            productobj = Product.objects.filter(Q(barcode_num=d['Barcode']) | Q(sku=d['SKU']))

                            if productobj:
                                #print "product found"
                                for pro in productobj:
                                    #print "product inside found"
                                    pro.unit = re
                                    pro.save()
                                    count = count + 1

                    MSG = "Sucessfully updated "
                    context.update(
                        {"title": "warehouse", "store": strpage, "warehouse": warpage, "successexcel": MSG,
                         "count": count,
                         })
                    return render(request, 'components/fetch_product.html', context)

                        # print d['Barcode']
                        # print d['SKU']
                        # # print type(d['Conversion factor'])
                        # print type(d['Unit of Measurement'])
                        # reunit = str(d['Conversion factor'])
                        # if d['Barcode'] or d['SKU']:
                        #     con = int(round(d['Conversion factor']))
                        #
                        #     uom =  (d['Unit of Measurement'].encode('ascii','ignore'))
                        #
                        #     re  = con.__str__() + uom
                        #     print "++", re
                        #     sfoproductobj = SFOProduct.objects.filter(Q(barcode=d['Barcode']) | Q(sku=d['SKU']))
                        #     if sfoproductobj:
                        #         #print "SFOproduct found"
                        #         for sfproobj in sfoproductobj:
                        #             #print "inside SFOproduct found"
                        #
                        #             sfproobj.reorder_unit = re
                        #             sfproobj.save()
                        #
                        #     productobj = Product.objects.filter(Q(barcode_num=d['Barcode']) | Q(sku=d['SKU']))
                        #
                        #     if productobj:
                        #         print "product found"
                        #         for pro in productobj:
                        #             print "product inside found"
                        #             pro.unit = re
                        #             pro.save()

                    # print count
                    # MSG = "Sucessfully update Total Record "
                    # context.update(
                    #     {"title": "warehouse", "store": strpage, "warehouse": warpage, "successexcel": MSG, "count": count,
                    #      })
                    # return render(request, 'components/fetch_product.html', context)

            except:
                context.update(
                    {"title": "warehouse", "store": strpage, "warehouse": warpage,
                     "excelwarn": "Please select xlx file",
                     })
                return render(request, 'components/fetch_product.html', context)


    elif request.method == "POST" and 'xls' in request.POST:
        if request.FILES['prxls']:
            context={}
            warpage = Warehouse.objects.filter(is_delete=False)
            strpage = Store.objects.filter(is_delete=False)
            input_excel = request.FILES['prxls']
            try:
                book = xlrd.open_workbook(file_contents=input_excel.read())
            # print book
            #
            # sheet_names = book.sheet_names()
            # print('Sheet Names', sheet_names)
            #
            # xl_sheet = book.sheet_by_name(sheet_names[0])
            # print xl_sheet
            # row = xl_sheet.row(0)
            # print row


                sheet = book.sheet_by_index(0)
                keys = [sheet.cell(0, col_index).value for col_index in xrange(sheet.ncols)]
                print "keys are", keys

                userobj = User.objects.get(id=request.user.id)
                dict_list = []
                count = 0
                for row_index in xrange(1, sheet.nrows):
                    d = {keys[col_index]: sheet.cell(row_index, col_index).value
                        for col_index in xrange(sheet.ncols)}

                    count = count + 1
                    # print d['Barcode']
                    # print d['SKU']
                    # print d['ID']
                    # print d['Name']
                    # print d['BIN']
                    # print d['Primary Vendor']
                    # print d['Active']
                    # print d['Export Unit']
                    # print d['Threshold']
                    # print d['Quantity in Hand']
                    # print d['Quantity in Layaway']
                    # print d['Quantity for Sale']
                    # print d['Current Cost']
                    # print d['Total Value']

                    print d['Barcode']
                    print d['SKU']
                    if d['Active'] == 1:
                        ac = True
                    else:
                        ac = False

                    if not d['Total Value']:
                        totalval = 0.0
                    else:
                        totalval = d['Total Value']

                    if not d['Current Cost']:
                        cost = 0.0
                    else:
                        cost = d['Current Cost']


                    if not d['Quantity in Layaway']:
                        ql = 0
                    else:
                        ql = d['Quantity in Layaway']


                    try:
                        sfoproductobj = SFOProduct.objects.filter(Q(barcode=d['Barcode']) | Q(sku=d['SKU']))

                        if sfoproductobj:

                            for sfproobj in sfoproductobj:

                                s = SFOProduct.objects.get(pk=sfproobj.id)


                                s.barcode =  d['Barcode']
                                s.sku = d['SKU']
                                s.sid = d['ID']
                                s.name = d['Name']
                                s.bin = d['BIN']
                                s.primary_vendor = d['Primary Vendor']
                                s.active = ac
                                s.export_unit = d['Export Unit']
                                s.threshold = d['Threshold']

                                qh = int(d['Quantity in Hand'])

                                s.quantityinhand = qh
                                s.quantityinlayaway = ql
                                s.quantityforsale = d['Quantity for Sale']
                                s.currentcost = cost
                                s.totalvalue = totalval

                                s.save()
                        else:
                            print "else"
                            qh = int(d['Quantity in Hand'])
                            SFOProduct.objects.create(sid=d['ID'], name=d['Name'], barcode=d['Barcode'],
                                                      sku=d['SKU'], bin=d['BIN'],
                                                      primary_vendor=d['Primary Vendor'],
                                                      active=ac,
                                                      export_unit=d['Export Unit'],
                                                      threshold=d['Threshold'],
                                                      quantityinhand=qh,
                                                      quantityinlayaway=d['Quantity in Layaway'],
                                                      quantityforsale=d['Quantity for Sale'],
                                                      currentcost=cost,
                                                      totalvalue=totalval,
                                                      user_id=userobj,
                                                      )
                    except:
                            pass


                print count
                MSG = "Sucessfully operation Total Record "
                context.update(
                        {"title": "warehouse", "store": strpage, "warehouse": warpage, "successexcel": MSG,"count":count,
                         })
                return render(request, 'components/fetch_product.html', context)
            except:
                context.update(
                    {"title": "warehouse", "store": strpage, "warehouse": warpage, "excelwarn": "Please select xlx file",
                     })
                return render(request, 'components/fetch_product.html', context)





# class LoginManage(View):
#     """
#     Login functionality
#     """
#
#     def get(self, request):
#         context = {}
#         context.update({'title': "Log In"})
#         return render(request, "components/login.html", context)
#
#     def post(self, request):
#         context = {}
#         validate = True
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#
#         if not username:
#             validate = False
#             context.update({"name": "Please enter  username"})
#
#         if not password:
#             validate = False
#             context.update({"password": "Please enter password"})
#
#         if validate:
#             user = authenticate(username=username, password=password)
#             if user:
#                 return render(request, 'components/fetch_product.html', context)
#             else:
#                 context.update({"up": "Please enter valid username and password"})
#                 return render(request, "components/login.html", context)
#         else:
#             print context
#             return render(request, "components/login.html", context)



class AddWarehouse(View):
    """
        Add warehouse
    """
    def get(self, request):
        context={}
        if request.user.is_authenticated:
            context.update({"title": "Add Warehouse"})
            return render(request, "components/addwarehouse.html", context)
        else:

            return HttpResponseRedirect('/admin/login')

    def post(self, request):

        context = {}
        validate = True
        name = request.POST.get('wname', None)
        number = request.POST.get('wnumber', None)

        if request.user.is_authenticated:
            if not name:
                validate = False
                context.update({"name": "Please enter  warehouse"})

            if not number:
                validate = False
                context.update({"password": "Please enter warehouse number"})

            if validate:
                Warehouse.objects.create(name=name, number=number, created_by=request.user.id)
                context.update({"success": "Sucessfully added Warehouse"})
                return render(request, "components/addwarehouse.html", context)
            else:
                return render(request, "components/addwarehouse.html", context)


class AddStore(View):
    """
        Add warehouse
    """
    def get(self, request):
        context={}
        if request.user.is_authenticated:
            war = Warehouse.objects.filter(is_delete=False)
            context.update({"title":"Store","warehouse":war})
            return render(request, "components/addstore.html", context)

    def post(self, request):
        context = {}
        if request.user.is_authenticated:
            name = request.POST.get('sname', None)
            number = request.POST.get('snumber', None)
            validate = True
            war = Warehouse.objects.filter(is_delete=False)
            context.update({"title": "Store", "warehouse": war})
            ware = request.POST.get('ware')
            if  ware == "00":
                validate = False
                context.update({"houseware":"Please Select Warehouse"})

            if not name:
                validate = False
                context.update({"name": "Please enter  store name"})


            if not number:
                validate = False
                context.update({"number": "Please enter  store number"})

            if validate:
                warobj = Warehouse.objects.get(id=ware)
                Store.objects.create(name=name, number=number, warehouse=warobj, created_by=request.user.id)
                context.update({"success": "Sucessfully added Store"})
                return render(request, "components/addstore.html", context)
            else:
                return render(request, "components/addstore.html", context)


class EditStore(View):
    """
        Edit Store
    """
    def get(self, request, pk):
        context={}
        if request.user.is_authenticated:
            war = Warehouse.objects.filter(is_delete=False)
            stro = Store.objects.get(id=pk)
            context.update({"title":"Edit Store","warehouse":war, "store":stro })
            return render(request, "components/editstore.html", context)

    def post(self, request, pk):

        context = {}
        if request.user.is_authenticated:
            validate = True
            context = {}
            name = request.POST.get('sname', None)
            number = request.POST.get('snumber', None)
            ware = request.POST.get('ware', None)
            if  ware == "00":
                validate = False
                context.update({"houseware":"Please Select Warehouse"})

            if not name:
                validate = False
                context.update({"name": "Please enter  store name"})


            if not number:
                validate = False
                context.update({"number": "Please enter  store number"})

            if validate:
                warobj = Warehouse.objects.get(id=ware)
                str = Store.objects.get(id=pk)
                str.name = name
                str.number = number
                str.warehouse = warobj
                str.created_by = request.user.id
                str.save()
                str = Store.objects.filter(is_delete=False)
                context.update({"title": "Storelist", "store": str})
                return render(request, "components/storelist.html", context)
            else:
                return render(request, "components/editstore.html", context)


class EditWarehouse(View):
    """
        Edit Store
    """
    def get(self, request, pk):
        context={}
        if request.user.is_authenticated:

            war = Warehouse.objects.get(id=pk)
            context.update({"title": "Edit Warehouse", "warehouse": war})
            return render(request, "components/editwarehouse.html", context)

    def post(self, request, pk):

        context = {}
        validate = True
        name = request.POST.get('wname', None)
        number = request.POST.get('wnumber', None)

        if request.user.is_authenticated:
            if not name:
                validate = False
                context.update({"name": "Please enter  warehouse"})

            if not number:
                validate = False
                context.update({"password": "Please enter warehouse number"})

            if validate:
                war = Warehouse.objects.get(id=pk)
                war.name = name
                war.number = number
                war.save()

                war = Warehouse.objects.filter(is_delete=False)
                context.update({"title": "Warehouselist", "warehouse": war})
                return render(request, "components/warehouselist.html", context)
            else:
                return render(request, "components/addwarehouse.html", context)


class FetchProductData(View):
    """
        this view is fetch data from revel system api and enter into our Product table
        based on Purchase order number
    """
    def get(self, request):
        context = {}
        return render(request, "components/fetch_product.html")
        #return render(request, "components/fetch_product.html", context)

    def post(self, request):
        print "mm"
        context = {}
        print request.POST
        ponumber = request.POST.get('ponumber', None)
        print ponumber
        print request.user
        if request.user.is_authenticated and request.user.is_superuser:

            validate = True
            ponumber = request.POST.get('ponumber', None)
            print ponumber
            return render(request, "components/fetch_product.html", context)
        else:
            return render(request, "components/login.html", LoginForm)


class WarehouseList(View):
    """
        List for warehouse List
    """
    def get(self, request):
        context = {}
        war = Warehouse.objects.filter(is_delete=False)
        context.update({"title":"Warehouselist", "warehouse":war})
        return render(request, "components/warehouselist.html", context)


class ExportCSV(View):
    """
        List of Product
    """
    def get(self, request):

        if request.user.is_authenticated:
            context = {}
            if request.user.is_superuser:
                productobj = Product.objects.all()
                war = Warehouse.objects.filter(is_delete=False)
                store = Store.objects.filter(is_delete=False)
            else:
                productobj = Product.objects.filter(user_id = request.user.id)
                ac = Acluser.objects.get(user=request.user.id)
                print "ggg",ac.warehouse.id
                war = Warehouse.objects.filter(is_delete=False, id=ac.warehouse.id)
                store = Store.objects.filter(is_delete=False, id=ac.store.id)
            context.update({"title":"ExportCSV", "Product": productobj, "warehouse":war, "store":store})
            return render(request, "components/exportcsvlist.html", context)

    def post(self, request):
        context = {}
        columns = ['Ingredient to Product','Update Cost','Source Establishment ID','Destination Establishment ID', 'Product Name','Barcode', 'SKU','Quantity','Unit','Is Ingredient']
        if request.user.is_authenticated:
            if request.method == "POST" and 'filter' in request.POST:

                validate = True
                ware = request.POST.get('wname',None)
                store = request.POST.get('store', None)
                sdate = request.POST.get('sdate', None)
                edate = request.POST.get('edate', None)
                pick = request.POST.get('pick', None)

                if ware != "000" and store != "00" and not sdate and not edate and not pick:
                    """
                        USE WHEN SELECT ONLY WARE HOUSE AND STORE
                    """
                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    productobj = Product.objects.filter(store_id = strobj.id, warehouse_id = warobj.id, quantityindisplay__gt=0)
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    context.update({"title": "ExportCSV", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportcsvlist.html", context)

                elif ware != "000" and store != "00" and not sdate is None and not edate is None and not pick:
                    """
                        use when select the ware house store and start date and end date
                    """


                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if edate:
                        warobj = Warehouse.objects.get(id=ware)
                        strobj = Store.objects.get(id=store)
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)

                        productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id, created_at__range=[sdate, edate], quantityindisplay__gt=0)
                        context.update({"title": "ExportCSV", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportcsvlist.html", context)
                    else:

                        context.update(
                            {"title": "ExportCSV", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportcsvlist.html", context)


                elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick:

                    """
                        its used only when start date and end date is select 
                        
                    """
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if edate:
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)
                        productobj = Product.objects.filter(created_at__range=[sdate, edate],quantityindisplay__gt=0)
                        context.update({"title": "ExportCSV", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportcsvlist.html", context)
                    else:

                        context.update(
                            {"title": "ExportCSV", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportcsvlist.html", context)


                elif ware == "000" and store == "00" and not sdate  and not edate  and not pick is None:

                    """
                        only used when picklsit number is used
                    """

                    productobj = Product.objects.filter(picklist=pick, quantityindisplay__gt=0 )
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    context.update({"title": "ExportCSV", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportcsvlist.html", context)

                elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick is None:

                    """
                        its used with startding date end date and picklist
                    """
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if edate:
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)

                        productobj = Product.objects.filter(picklist=pick, created_at__range=[sdate, edate],created_at=edate, quantityindisplay__gt=0)

                        context.update({"title": "ExportCSV", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportcsvlist.html", context)
                    context.update(
                        {"title": "ExportCSV", "Product": Product.objects.all(),
                         "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                    return render(request, "components/exportcsvlist.html", context)

            else:

                if request.method == "POST" and 'xls' in request.POST:

                    ware = request.POST.get('wname', None)
                    store = request.POST.get('store', None)
                    sdate = request.POST.get('sdate', None)
                    edate = request.POST.get('edate', None)
                    pick = request.POST.get('pick', None)

                    response = HttpResponse(content_type='application/ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="Product.xls"'

                    wb = xlwt.Workbook(encoding='utf-8')
                    ws = wb.add_sheet('Product')

                    # Sheet header, first row
                    row_num = 0

                    font_style = xlwt.XFStyle()
                    font_style.font.bold = True

                if ware != "000" and store != "00" and not sdate and not edate and not pick:
                    """
                        USE WHEN SELECT ONLY WARE HOUSE AND STORE
                    """
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)


                    # Sheet body, remaining rows
                    font_style = xlwt.XFStyle()

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id, quantityindisplay__gt = 0)
                    #values_list('id','picklist','store_number','warehouse','bin_location','vendor_product_id','sku', 'barcode_num',' unit','description')
                    quan = 0
                    unit = "Unit"
                    for row in productobj:
                        row_num += 1
                        print "ssssss", row.quantity
                        if row.quantity:
                            quan = ((float(row.quantity)) * (float(row.Conversion)))
                        else:
                            quan = ""
                        if row.unit == "Unit":
                            unit = row.unit
                        else:
                            unit

                        row = [
                            row.ingredienttoproduct,
                            row.updatecost,
                            row.warehouse.number,
                            row.store.number,
                            row.description,
                            row.barcode_num,
                            row.sku,
                            quan,
                            unit,
                            row.is_ingredient,


                        ]
                        # for col_num in range(len(row)):
                        #     ws.write(row_num, col_num, row[col_num], font_style)

                        for col_num in xrange(len(row)):
                            ws.write(row_num, col_num, str(row[col_num]), font_style)

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    wb.save(response)
                    return response
                    context.update({"title": "ExportCSV", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportcsvlist.html", context)

                elif ware != "000" and store != "00" and not sdate is None and not edate is None and not pick:
                    """
                        use when select the ware house store and start date and end date
                    """

                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if sdate and edate:
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)

                        warobj = Warehouse.objects.get(id=ware)
                        strobj = Store.objects.get(id=store)
                        productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                            created_at__range=[sdate, edate],quantityindisplay__gt = 0)
                        quan = 0
                        unit = "Unit"
                        for row in productobj:
                            row_num += 1
                            print "ssssss", row.quantity
                            if row.quantity:
                                quan = ((float(row.quantity)) * (float(row.Conversion)))
                            else:
                                quan = ""
                            if row.unit == "Unit":
                                unit = row.unit
                            else:
                                unit

                            row = [
                                row.ingredienttoproduct,
                                row.updatecost,
                                row.warehouse.number,
                                row.store.number,
                                row.description,
                                row.barcode_num,
                                row.sku,
                                quan,
                                unit,
                                row.is_ingredient,

                            ]
                            # for col_num in range(len(row)):
                            #     ws.write(row_num, col_num, row[col_num], font_style)

                            for col_num in xrange(len(row)):
                                ws.write(row_num, col_num, str(row[col_num]), font_style)

                        wb.save(response)
                        return response

                        context.update({"title": "ExportCSV", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportcsvlist.html", context)
                    else:

                        context.update(
                            {"title": "ExportCSV", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportcsvlist.html", context)


                elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick:

                    """
                        its used only when start date and end date is select 

                    """
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if edate and sdate:
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)


                        productobj = Product.objects.filter(created_at__range=[sdate, edate], quantityindisplay__gt = 0)
                        quan = 0
                        unit = "Unit"
                        for row in productobj:
                            row_num += 1
                            print "ssssss", row.quantity
                            if row.quantity:
                                tquantity = float(row.quantity)

                                if row.Conversion is not None:
                                    tConversion = float(row.Conversion)
                                    quan = (tquantity) * (tConversion)
                            else:
                                quan = ""
                            if row.unit == "Unit":
                                unit = row.unit
                            else:
                                unit

                            row = [
                                row.ingredienttoproduct,
                                row.updatecost,
                                row.warehouse.number,
                                row.store.number,
                                row.description,
                                row.barcode_num,
                                row.sku,
                                quan,
                                unit,
                                row.is_ingredient,

                            ]
                            # for col_num in range(len(row)):
                            #     ws.write(row_num, col_num, row[col_num], font_style)

                            for col_num in xrange(len(row)):
                                ws.write(row_num, col_num, str(row[col_num]), font_style)

                        wb.save(response)
                        return response


                        context.update({"title": "ExportCSV", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportcsvlist.html", context)
                    else:

                        context.update(
                            {"title": "ExportCSV", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportcsvlist.html", context)


                elif ware == "000" and store == "00" and not sdate and not edate and not pick is None:

                    """
                        only used when picklsit number is used
                    """
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)


                    productobj = Product.objects.filter(picklist=pick, quantityindisplay__gt = 0)
                    quan = 0
                    unit = "Unit"
                    for row in productobj:
                        row_num += 1
                        print "ssssss",row.quantity
                        if row.quantity:
                            quan = ((float(row.quantity)) * (float(row.Conversion)))
                        else:
                            quan = ""
                        if row.unit == "Unit":
                            unit=row.unit
                        else:
                            unit

                        row = [
                            row.ingredienttoproduct,
                            row.updatecost,
                            row.warehouse.number,
                            row.store.number,
                            row.description,
                            row.barcode_num,
                            row.sku,
                            quan,
                            unit,
                            row.is_ingredient,

                        ]
                        # for col_num in range(len(row)):
                        #     ws.write(row_num, col_num, row[col_num], font_style)

                        for col_num in xrange(len(row)):
                            ws.write(row_num, col_num, str(row[col_num]), font_style)

                    wb.save(response)
                    return response
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    context.update({"title": "ExportCSV", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportcsvlist.html", context)

                elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick is None:

                    """
                        its used with startding date end date and picklist
                    """
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)


                    productobj = Product.objects.filter(picklist=pick, created_at__range=[sdate, edate],
                                                        created_at=edate, quantityindisplay__gt = 0)
                    quan = 0
                    unit = "Unit"
                    for row in productobj:
                        row_num += 1
                        print "ssssss", row.quantity
                        if row.quantity:
                            quan = ((float(row.quantity)) * (float(row.Conversion)))
                        else:
                            quan = ""
                        if row.unit == "Unit":
                            unit = row.unit
                        else:
                            unit

                        row = [
                            row.ingredienttoproduct,
                            row.updatecost,
                            row.warehouse.number,
                            row.store.number,
                            row.description,
                            row.barcode_num,
                            row.sku,
                            quan,
                            unit,
                            row.is_ingredient,

                        ]
                        # for col_num in range(len(row)):
                        #     ws.write(row_num, col_num, row[col_num], font_style)

                        for col_num in xrange(len(row)):
                            ws.write(row_num, col_num, str(row[col_num]), font_style)

                    wb.save(response)
                    return response
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    context.update({"title": "ExportCSV", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportcsvlist.html", context)


class StoreList(View):
    """
        List for Store
    """
    def get(self, request):
        context = {}
        str = Store.objects.filter(is_delete=False)
        context.update({"title":"Storelist", "store":str})
        return render(request, "components/storelist.html", context)


def StoreUpdate(self, request, pk):
    context={}
    if request.method == "GET":
        if request.user.is_authenticated:
            war = Warehouse.objects.filter(is_delete=False)
            context.update({"title":"Store","warehouse":war})
            return render(request, "components/editstore.html", context)



class Apikeylist(View):
    """
        Edit Store
    """
    def get(self, request):
        context={}
        if request.user.is_authenticated:
            apikey = ApiKey.objects.all()

            context.update({"title":"Edit Key","key":apikey})
            return render(request, "components/apikeylist.html", context)


class EditKEY(View):
    """
        Edit APIKEY
    """
    def get(self, request, pk):
        context={}
        if request.user.is_authenticated:
            apikey = ApiKey.objects.get(id=pk)
            print apikey
            context.update({"title":"Edit Key", "obj":apikey})
            return render(request, "components/editkey.html", context)

    def post(self, request, pk):

        context = {}
        if request.user.is_authenticated:
            validate = True
            context = {}
            key = request.POST.get('key', None)
            seckey = request.POST.get('seckey', None)

            print key
            print seckey
            if not key:
                validate = False
                context.update({"name": "Please enter  Api Key"})


            if not seckey:
                validate = False
                context.update({"number": "Please enter  secret key "})

            if validate:
                key = ApiKey.objects.get(id=pk)
                key.apikey = str(key)
                key.apisec = str(seckey)
                key.save()

                apiobj = ApiKey.objects.all()

                context.update({"title": "Edit Key", "key": apiobj})
                return render(request, "components/apikeylist.html", context)
            else:
                return render(request, "components/editstore.html", context)


class ExportReport(View):
    """
        List of Product
    """
    def get(self, request):

        if request.user.is_authenticated:
            context = {}
            if request.user.is_superuser:
                productobj = Product.objects.all()
                war = Warehouse.objects.filter(is_delete=False)
                store = Store.objects.filter(is_delete=False)
            else:
                productobj = Product.objects.filter(user_id=request.user.id)
                ac = Acluser.objects.get(user=request.user.id)
                war = Warehouse.objects.filter(is_delete=False, id=ac.warehouse.id)
                store = Store.objects.filter(is_delete=False, id=ac.store.id)
            context.update({"title":"ExportReport", "Product": productobj, "warehouse":war, "store":store})
            return render(request, "components/exportreportlist.html", context)

    def post(self, request):

        ware = request.POST.get('wname', None)
        store = request.POST.get('store', None)
        sdate = request.POST.get('sdate', None)
        edate = request.POST.get('edate', None)
        pick = request.POST.get('pick', None)
        tote = request.POST.get('tote', None)
        context= {}
        columns = ['Picklist', 'Warehouse Number', 'Store Number', 'Store Name', 'Tote Number']

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Product_Report.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Product_Report')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        if request.user.is_authenticated:

            if request.method == "POST" and 'filter' in request.POST:


                if ware != "000" and store != "00" and not sdate and not edate and not pick and not tote:
                    """
                        USE WHEN SELECT ONLY WARE HOUSE AND STORE
                    """

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    if request.user.is_superuser:
                        productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                        quantityindisplay__gt=0)
                    else:
                        productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                            quantityindisplay__gt=0,user_id=request.user.id)

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)

                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware != "000" and store != "00" and not sdate is None and not edate is None and not pick and not tote:
                    """
                        use when select the ware house store and start date and end date
                    """

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)

                    edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                    edate = edate + datetime.timedelta(days=1)

                    productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                        created_at__range=[sdate, edate], quantityindisplay__gt=0)
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick and not tote:

                    """
                        its used only when start date and end date is select 

                    """
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if edate:
                        print "hhh"
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)
                        productobj = Product.objects.filter(created_at__range=[sdate, edate],quantityindisplay__gt=0)

                        context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)
                    else:
                        context.update(
                            {"title": "ExportReport", "Product": Product.objects.all(),"eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)


                elif ware == "000" and store == "00" and not sdate and not edate and not pick is None and not tote:

                    """
                        only used when picklsit number is used
                    """

                    productobj = Product.objects.filter(picklist=pick, quantityindisplay__gt=0)
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware == "000" and store == "00" and not sdate and not edate and not pick  and not tote is None:

                    """
                        only used when tote number is used
                    """

                    productobj = Product.objects.filter(tote=tote, quantityindisplay__gt=0)
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick is None and not tote:

                    """
                        its used with startding date end date and picklist
                    """
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if edate:
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)

                        productobj = Product.objects.filter(picklist=pick, created_at__range=[sdate, edate],
                                                        created_at=edate, quantityindisplay__gt=0)

                        context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)
                    else:

                        context.update(
                            {"title": "ExportReport", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)


                elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick  and not tote is None:

                    """
                        its used with startding date end date and tote
                    """
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)

                    if edate:

                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)

                        productobj = Product.objects.filter(quantityindisplay__gt=0,tote=tote, created_at__range=[sdate, edate])

                        context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)
                    else:
                        context.update(
                            {"title": "ExportReport", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)


                elif ware != "000" and store != "00" and not sdate and not edate and not pick is None and not tote:
                    """
                        USE WHEN SELECT ONLY WARE HOUSE AND STORE and  Picklist
                    """

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                        picklist=pick, quantityindisplay__gt=0)

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)

                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware != "000" and store != "00" and not sdate and not edate and not pick  and not tote is None:
                    """
                        USE WHEN SELECT ONLY WARE HOUSE AND STORE and  tote
                    """

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                        tote=tote, quantityindisplay__gt=0)

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)

                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware != "000" and store != "00" and not sdate is None and not edate is None and not pick is None and not tote is None :
                    """
                        USE WHEN all Option
                    """

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if edate and sdate:
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)

                        productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                        tote=tote, picklist=pick,
                                                        quantityindisplay__gt=0, created_at__range=[sdate, edate])



                        context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)
                    else:
                        context.update(
                            {"title": "ExportReport", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)




            elif request.method == "POST" and 'xlsreport' in request.POST:

                if ware != "000" and store != "00" and not sdate and not edate and not pick and not tote:
                    """
                        USE WHEN SELECT ONLY WARE HOUSE AND STORE
                    """
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                        quantityindisplay__gt=0)
                    for row in productobj:
                        row_num += 1
                        row = [

                            row.picklist,
                            row.warehouse.number,
                            row.store.number,
                            row.store.name,
                            row.tote,
                        ]
                        # for col_num in range(len(row)):
                        #     ws.write(row_num, col_num, row[col_num], font_style)

                        for col_num in xrange(len(row)):
                            ws.write(row_num, col_num, str(row[col_num]), font_style)

                    wb.save(response)
                    return response


                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)

                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware != "000" and store != "00" and not sdate is None and not edate is None and not pick and not tote:
                    """
                        use when select the ware house store and start date and end date
                    """
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)

                    edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                    edate = edate + datetime.timedelta(days=1)

                    productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                        created_at__range=[sdate, edate], quantityindisplay__gt=0)

                    for row in productobj:
                        row_num += 1
                        row = [

                            row.picklist,
                            row.warehouse.number,
                            row.store.number,
                            row.store.name,
                            row.tote,
                        ]
                        # for col_num in range(len(row)):
                        #     ws.write(row_num, col_num, row[col_num], font_style)

                        for col_num in xrange(len(row)):
                            ws.write(row_num, col_num, str(row[col_num]), font_style)

                    wb.save(response)
                    return response

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick and not tote:

                    """
                        its used only when start date and end date is select 

                    """
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if edate:
                        print "hhh"
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)
                        productobj = Product.objects.filter(created_at__range=[sdate, edate], quantityindisplay__gt=0)

                        for row in productobj:
                            row_num += 1
                            row = [

                                row.picklist,
                                row.warehouse.number,
                                row.store.number,
                                row.store.name,
                                row.tote,
                            ]
                            # for col_num in range(len(row)):
                            #     ws.write(row_num, col_num, row[col_num], font_style)

                            for col_num in xrange(len(row)):
                                ws.write(row_num, col_num, str(row[col_num]), font_style)

                        wb.save(response)
                        return response

                        context.update(
                            {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)
                    else:
                        context.update(
                            {"title": "ExportReport", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)


                elif ware == "000" and store == "00" and not sdate and not edate and not pick is None and not tote:

                    """
                        only used when picklsit number is used
                    """
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)

                    productobj = Product.objects.filter(picklist=pick, quantityindisplay__gt=0)
                    for row in productobj:
                        row_num += 1
                        row = [

                            row.picklist,
                            row.warehouse.number,
                            row.store.number,
                            row.store.name,
                            row.tote,
                        ]
                        # for col_num in range(len(row)):
                        #     ws.write(row_num, col_num, row[col_num], font_style)

                        for col_num in xrange(len(row)):
                            ws.write(row_num, col_num, str(row[col_num]), font_style)

                    wb.save(response)
                    return response

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware == "000" and store == "00" and not sdate and not edate and not pick and not tote is None:

                    """
                        only used when tote number is used
                    """
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)

                    productobj = Product.objects.filter(tote=tote, quantityindisplay__gt=0)
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick is None and not tote:

                    """
                        its used with startding date end date and picklist
                    """
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if edate:
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)

                        productobj = Product.objects.filter(picklist=pick, created_at__range=[sdate, edate],
                                                            created_at=edate, quantityindisplay__gt=0)

                        for row in productobj:
                            row_num += 1
                            row = [

                                row.picklist,
                                row.warehouse.number,
                                row.store.number,
                                row.store.name,
                                row.tote,
                            ]
                            # for col_num in range(len(row)):
                            #     ws.write(row_num, col_num, row[col_num], font_style)

                            for col_num in xrange(len(row)):
                                ws.write(row_num, col_num, str(row[col_num]), font_style)

                        wb.save(response)
                        return response

                        context.update(
                            {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)
                    else:

                        context.update(
                            {"title": "ExportReport", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)


                elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick and not tote is None:

                    """
                        its used with startding date end date and tote
                    """
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)

                    if edate:

                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)

                        productobj = Product.objects.filter(quantityindisplay__gt=0, tote=tote,
                                                            created_at__range=[sdate, edate])

                        for row in productobj:
                            row_num += 1
                            row = [

                                row.picklist,
                                row.warehouse.number,
                                row.store.number,
                                row.store.name,
                                row.tote,
                            ]
                            # for col_num in range(len(row)):
                            #     ws.write(row_num, col_num, row[col_num], font_style)

                            for col_num in xrange(len(row)):
                                ws.write(row_num, col_num, str(row[col_num]), font_style)

                        wb.save(response)
                        return response

                        context.update(
                            {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)
                    else:
                        context.update(
                            {"title": "ExportReport", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)


                elif ware != "000" and store != "00" and not sdate and not edate and not pick is None and not tote:
                    """
                        USE WHEN SELECT ONLY WARE HOUSE AND STORE and  Picklist
                    """
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                        picklist=pick, quantityindisplay__gt=0)


                    for row in productobj:
                        row_num += 1
                        row = [

                            row.picklist,
                            row.warehouse.number,
                            row.store.number,
                            row.store.name,
                            row.tote,
                        ]
                        # for col_num in range(len(row)):
                        #     ws.write(row_num, col_num, row[col_num], font_style)

                        for col_num in xrange(len(row)):
                            ws.write(row_num, col_num, str(row[col_num]), font_style)

                    wb.save(response)
                    return response

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)

                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware != "000" and store != "00" and not sdate and not edate and not pick and not tote is None:
                    """
                        USE WHEN SELECT ONLY WARE HOUSE AND STORE and  tote
                    """
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                        tote=tote, quantityindisplay__gt=0)

                    for row in productobj:
                        row_num += 1
                        row = [

                            row.picklist,
                            row.warehouse.number,
                            row.store.number,
                            row.store.name,
                            row.tote,
                        ]
                        # for col_num in range(len(row)):
                        #     ws.write(row_num, col_num, row[col_num], font_style)

                        for col_num in xrange(len(row)):
                            ws.write(row_num, col_num, str(row[col_num]), font_style)

                    wb.save(response)
                    return response

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)

                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware != "000" and store != "00" and not sdate is None and not edate is None and not pick is None and not tote is None:
                    """
                        USE WHEN all Option
                    """

                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num, columns[col_num], font_style)

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if edate and sdate:
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)

                        productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                            tote=tote, picklist=pick,
                                                            quantityindisplay__gt=0, created_at__range=[sdate, edate])

                        for row in productobj:
                            row_num += 1
                            row = [

                                row.picklist,
                                row.warehouse.number,
                                row.store.number,
                                row.store.name,
                                row.tote,
                            ]
                            # for col_num in range(len(row)):
                            #     ws.write(row_num, col_num, row[col_num], font_style)

                            for col_num in xrange(len(row)):
                                ws.write(row_num, col_num, str(row[col_num]), font_style)

                        wb.save(response)
                        return response


                        context.update(
                            {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)
                    else:
                        context.update(
                            {"title": "ExportReport", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)

                print "xlsreport"
            elif request.method == "POST" and 'Delivery' in request.POST:

                print "Delivery"
                if ware != "000" and store != "00" and not sdate and not edate and not pick and not tote:
                    """
                        USE WHEN SELECT ONLY WARE HOUSE AND STORE
                    """
                    print "warehouse  ans store"
                    context = {}
                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                        quantityindisplay__gt=0, tote__gt=0).distinct('tote')

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render_to_pdf(
                        'components/deliveryreport.html',
                        {
                            'pagesize': 'A4',
                            'mylist': productobj,
                        }
                    )

                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware != "000" and store != "00" and not sdate is None and not edate is None and not pick and not tote:
                    """
                        use when select the ware house store and start date and end date
                    """

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)

                    edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                    edate = edate + datetime.timedelta(days=1)

                    productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                        created_at__range=[sdate, edate], quantityindisplay__gt=0,tote__gt=0).distinct('tote')
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    return render_to_pdf(
                        'components/deliveryreport.html',
                        {
                            'pagesize': 'A4',
                            'mylist': productobj,
                        }
                    )
                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick and not tote:

                    """
                        its used only when start date and end date is select 

                    """
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if edate:
                        print "hhh"
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)
                        productobj = Product.objects.filter(created_at__range=[sdate, edate], quantityindisplay__gt=0,tote__gt=0).distinct('tote')

                        return render_to_pdf(
                            'components/deliveryreport.html',
                            {
                                'pagesize': 'A4',
                                'mylist': productobj,
                            }
                        )
                        context.update(
                            {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)
                    else:
                        context.update(
                            {"title": "ExportReport", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)


                elif ware == "000" and store == "00" and not sdate and not edate and not pick is None and not tote:

                    """
                        only used when picklsit number is used
                    """

                    productobj = Product.objects.filter(picklist=pick, quantityindisplay__gt=0,tote__gt=0).distinct('tote')
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    return render_to_pdf(
                        'components/deliveryreport.html',
                        {
                            'pagesize': 'A4',
                            'mylist': productobj,
                        }
                    )
                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware == "000" and store == "00" and not sdate and not edate and not pick and not tote is None:

                    """
                        only used when tote number is used
                    """

                    productobj = Product.objects.filter(tote=tote, quantityindisplay__gt=0,tote__gt=0).distinct('tote')
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    return render_to_pdf(
                        'components/deliveryreport.html',
                        {
                            'pagesize': 'A4',
                            'mylist': productobj,
                        }
                    )
                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick is None and not tote:

                    """
                        its used with startding date end date and picklist
                    """
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if edate:
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)

                        productobj = Product.objects.filter(picklist=pick, created_at__range=[sdate, edate],
                                                            created_at=edate, quantityindisplay__gt=0,tote__gt=0).distinct('tote')
                        return render_to_pdf(
                            'components/deliveryreport.html',
                            {
                                'pagesize': 'A4',
                                'mylist': productobj,
                            }
                        )
                        context.update(
                            {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)
                    else:

                        context.update(
                            {"title": "ExportReport", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)


                elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick and not tote is None:

                    """
                        its used with startding date end date and tote
                    """
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)

                    if edate:

                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)

                        productobj = Product.objects.filter(quantityindisplay__gt=0, tote=tote,
                                                            created_at__range=[sdate, edate],tote__gt=0).distinct('tote')

                        return render_to_pdf(
                            'components/deliveryreport.html',
                            {
                                'pagesize': 'A4',
                                'mylist': productobj,
                            }
                        )
                        context.update(
                            {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)
                    else:
                        context.update(
                            {"title": "ExportReport", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)


                elif ware != "000" and store != "00" and not sdate and not edate and not pick is None and not tote:
                    """
                        USE WHEN SELECT ONLY WARE HOUSE AND STORE and  Picklist
                    """

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                        picklist=pick, quantityindisplay__gt=0,tote__gt=0).distinct('tote')

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)

                    return render_to_pdf(
                        'components/deliveryreport.html',
                        {
                            'pagesize': 'A4',
                            'mylist': productobj,
                        }
                    )
                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware != "000" and store != "00" and not sdate and not edate and not pick and not tote is None:
                    """
                        USE WHEN SELECT ONLY WARE HOUSE AND STORE and  tote
                    """

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                        tote=tote, quantityindisplay__gt=0,tote__gt=0).distinct('tote')

                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)

                    return render_to_pdf(
                        'components/deliveryreport.html',
                        {
                            'pagesize': 'A4',
                            'mylist': productobj,
                        }
                    )
                    context.update({"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                    return render(request, "components/exportreportlist.html", context)

                elif ware != "000" and store != "00" and not sdate is None and not edate is None and not pick is None and not tote is None:
                    """
                        USE WHEN all Option
                    """

                    warobj = Warehouse.objects.get(id=ware)
                    strobj = Store.objects.get(id=store)
                    war = Warehouse.objects.filter(is_delete=False)
                    store = Store.objects.filter(is_delete=False)
                    if edate and sdate:
                        edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                        edate = edate + datetime.timedelta(days=1)

                        productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                            tote__gte=tote, picklist=pick,
                                                            quantityindisplay__gt=0, created_at__range=[sdate, edate],tote__gt=0).distinct('tote')

                        return render_to_pdf(
                            'components/deliveryreport.html',
                            {
                                'pagesize': 'A4',
                                'mylist': productobj,
                            }
                        )

                        context.update(
                            {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)
                    else:
                        context.update(
                            {"title": "ExportReport", "Product": Product.objects.all(),
                             "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                        return render(request, "components/exportreportlist.html", context)



            elif request.method == "POST" and 'Container' in request.POST:

                   print "Container"
                   if ware != "000" and store != "00" and not sdate and not edate and not pick and not tote:
                       """
                           USE WHEN SELECT ONLY WARE HOUSE AND STORE
                       """

                       warobj = Warehouse.objects.get(id=ware)
                       strobj = Store.objects.get(id=store)
                       productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                           quantityindisplay__gt=0,tote__gt=0).distinct('tote')

                       li = []
                       for product in productobj:
                           productnew = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj,picklist=product.picklist, quantityindisplay__gt=0,
                                                               tote=product.tote)
                           li.append(productnew)
                       war = Warehouse.objects.filter(is_delete=False)
                       store = Store.objects.filter(is_delete=False)
                       return render_to_pdf(
                           'components/containerreport.html',
                           {
                               'pagesize': 'A4',
                               'mylist': li,
                           }
                       )

                       context.update(
                           {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                       return render(request, "components/exportreportlist.html", context)

                   elif ware != "000" and store != "00" and not sdate is None and not edate is None and not pick and not tote:
                       """
                           use when select the ware house store and start date and end date
                       """

                       warobj = Warehouse.objects.get(id=ware)
                       strobj = Store.objects.get(id=store)

                       edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                       edate = edate + datetime.timedelta(days=1)

                       productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                           created_at__range=[sdate, edate], quantityindisplay__gt=0,tote__gt=0).distinct('tote')
                       li = []
                       for product in productobj:
                           productnew = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,picklist=product.picklist, quantityindisplay__gt=0,
                                                               created_at__range=[sdate, edate],tote=product.tote)
                           li.append(productnew)
                       war = Warehouse.objects.filter(is_delete=False)
                       store = Store.objects.filter(is_delete=False)
                       return render_to_pdf(
                           'components/containerreport.html',
                           {
                               'pagesize': 'A4',
                               'mylist': li,
                           }
                       )

                       context.update(
                           {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                       return render(request, "components/exportreportlist.html", context)

                   elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick and not tote:

                       """
                           its used only when start date and end date is select 

                       """
                       war = Warehouse.objects.filter(is_delete=False)
                       store = Store.objects.filter(is_delete=False)
                       if edate:
                           print "hhh"
                           edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                           edate = edate + datetime.timedelta(days=1)
                           productobj = Product.objects.filter(created_at__range=[sdate, edate],
                                                               quantityindisplay__gt=0,tote__gt=0).distinct('tote')

                           li = []
                           for product in productobj:
                               productnew = Product.objects.filter(created_at__range=[sdate, edate],picklist=product.picklist, quantityindisplay__gt=0,
                                                                   tote=product.tote)
                               li.append(productnew)

                           return render_to_pdf(
                               'components/containerreport.html',
                               {
                                   'pagesize': 'A4',
                                   'mylist': li,
                               }
                           )
                           context.update(
                               {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                           return render(request, "components/exportreportlist.html", context)
                       else:
                           context.update(
                               {"title": "ExportReport", "Product": Product.objects.all(),
                                "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                           return render(request, "components/exportreportlist.html", context)


                   elif ware == "000" and store == "00" and not sdate and not edate and not pick is None and not tote:

                       """
                           only used when picklsit number is used
                       """

                       productobj = Product.objects.filter(picklist=pick, quantityindisplay__gt=0,tote__gt=0).distinct('tote')

                       war = Warehouse.objects.filter(is_delete=False)
                       store = Store.objects.filter(is_delete=False)
                       li = []
                       for product in productobj:

                           productnew = Product.objects.filter(picklist=pick, quantityindisplay__gt=0, tote=product.tote)
                           li.append(productnew)

                       return render_to_pdf(
                               'components/containerreport.html',
                               {
                                   'pagesize': 'A4',
                                   'mylist': li,
                               }
                           )
                       context.update(
                           {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                       return render(request, "components/exportreportlist.html", context)

                   elif ware == "000" and store == "00" and not sdate and not edate and not pick and not tote is None:

                       """
                           only used when tote number is used
                       """

                       productobj = Product.objects.filter(tote=tote, quantityindisplay__gt=0,tote__gt=0).distinct('tote')
                       li = []
                       for product in productobj:
                           productnew = Product.objects.filter(picklist=product.picklist, quantityindisplay__gt=0,
                                                               tote=product.tote)
                           li.append(productnew)
                       war = Warehouse.objects.filter(is_delete=False)
                       store = Store.objects.filter(is_delete=False)
                       return render_to_pdf(
                           'components/containerreport.html',
                           {
                               'pagesize': 'A4',
                               'mylist': li,
                           }
                       )
                       context.update(
                           {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                       return render(request, "components/exportreportlist.html", context)

                   elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick is None and not tote:

                       """
                           its used with startding date end date and picklist
                       """
                       war = Warehouse.objects.filter(is_delete=False)
                       store = Store.objects.filter(is_delete=False)
                       if edate:
                           edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                           edate = edate + datetime.timedelta(days=1)

                           productobj = Product.objects.filter(picklist=pick, created_at__range=[sdate, edate],
                                                               created_at=edate, quantityindisplay__gt=0,tote__gt=0).distinct('tote')

                           li = []
                           for product in productobj:
                               productnew = Product.objects.filter(picklist=pick,created_at__range=[sdate, edate],created_at=edate, quantityindisplay__gt=0,
                                                                   tote=product.tote)
                               li.append(productnew)
                           return render_to_pdf(
                               'components/containerreport.html',
                               {
                                   'pagesize': 'A4',
                                   'mylist': li,
                               }
                           )
                           context.update(
                               {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                           return render(request, "components/exportreportlist.html", context)
                       else:

                           context.update(
                               {"title": "ExportReport", "Product": Product.objects.all(),
                                "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                           return render(request, "components/exportreportlist.html", context)


                   elif ware == "000" and store == "00" and not sdate is None and not edate is None and not pick and not tote is None:

                       """
                           its used with startding date end date and tote
                       """
                       war = Warehouse.objects.filter(is_delete=False)
                       store = Store.objects.filter(is_delete=False)

                       if edate:

                           edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                           edate = edate + datetime.timedelta(days=1)

                           productobj = Product.objects.filter(quantityindisplay__gt=0, tote=tote,
                                                               created_at__range=[sdate, edate],tote__gt=0).distinct('tote')

                           li = []
                           for product in productobj:
                               productnew = Product.objects.filter(picklist=product.picklist, quantityindisplay__gt=0,
                                                                   created_at__range=[sdate, edate],tote=product.tote)
                               li.append(productnew)
                           return render_to_pdf(
                               'components/containerreport.html',
                               {
                                   'pagesize': 'A4',
                                   'mylist': productobj,
                               }
                           )
                           context.update(
                               {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                           return render(request, "components/exportreportlist.html", context)
                       else:
                           context.update(
                               {"title": "ExportReport", "Product": Product.objects.all(),
                                "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                           return render(request, "components/exportreportlist.html", context)


                   elif ware != "000" and store != "00" and not sdate and not edate and not pick is None and not tote:
                       """
                           USE WHEN SELECT ONLY WARE HOUSE AND STORE and  Picklist
                       """

                       warobj = Warehouse.objects.get(id=ware)
                       strobj = Store.objects.get(id=store)
                       productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                           picklist=pick, quantityindisplay__gt=0,tote__gt=0).distinct('tote')

                       li = []
                       for product in productobj:
                           productnew = Product.objects.filter(picklist=product.picklist, quantityindisplay__gt=0,
                                                               store_id=strobj.id, warehouse_id=warobj.id, tote=product.tote)
                           li.append(productnew)
                       return render_to_pdf(
                           'components/containerreport.html',
                           {
                               'pagesize': 'A4',
                               'mylist': li,
                           }
                       )
                       war = Warehouse.objects.filter(is_delete=False)
                       store = Store.objects.filter(is_delete=False)

                       context.update(
                           {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                       return render(request, "components/exportreportlist.html", context)

                   elif ware != "000" and store != "00" and not sdate and not edate and not pick and not tote is None:
                       """
                           USE WHEN SELECT ONLY WARE HOUSE AND STORE and  tote
                       """

                       warobj = Warehouse.objects.get(id=ware)
                       strobj = Store.objects.get(id=store)
                       productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                           tote=tote, quantityindisplay__gt=0,tote__gt=0).distinct('tote')

                       li = []
                       for product in productobj:
                           productnew = Product.objects.filter(picklist=product.picklist, quantityindisplay__gt=0,
                                                               store_id=strobj.id, warehouse_id=warobj.id,
                                                               tote=product.tote)
                           li.append(productnew)
                       return render_to_pdf(
                           'components/containerreport.html',
                           {
                               'pagesize': 'A4',
                               'mylist': li,
                           }
                       )
                       war = Warehouse.objects.filter(is_delete=False)
                       store = Store.objects.filter(is_delete=False)

                       context.update(
                           {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                       return render(request, "components/exportreportlist.html", context)

                   elif ware != "000" and store != "00" and not sdate is None and not edate is None and not pick is None and not tote is None:
                       """
                           USE WHEN all Option
                       """

                       warobj = Warehouse.objects.get(id=ware)
                       strobj = Store.objects.get(id=store)
                       war = Warehouse.objects.filter(is_delete=False)
                       store = Store.objects.filter(is_delete=False)
                       if edate and sdate:
                           edate = datetime.datetime.strptime(edate, "%Y-%m-%d")
                           edate = edate + datetime.timedelta(days=1)

                           productobj = Product.objects.filter(store_id=strobj.id, warehouse_id=warobj.id,
                                                               tote=tote, picklist=pick,
                                                               quantityindisplay__gt=0,
                                                               created_at__range=[sdate, edate],tote__gt=0).distnict('tote')

                           li = []
                           for product in productobj:
                               productnew = Product.objects.filter(store_id=strobj.id,picklist=product.picklist, quantityindisplay__gt=0,
                                                                   warehouse_id=warobj.id,
                                                                   tote=tote,created_at__range=[sdate, edate])
                               li.append(productnew)
                           return render_to_pdf(
                               'components/containerreport.html',
                               {
                                   'pagesize': 'A4',
                                   'mylist': li,
                               }
                           )
                           context.update(
                               {"title": "ExportReport", "Product": productobj, "warehouse": war, "store": store})
                           return render(request, "components/exportreportlist.html", context)
                       else:
                           context.update(
                               {"title": "ExportReport", "Product": Product.objects.all(),
                                "eroor": "Plese select Valid filter option", "warehouse": war, "store": store})
                           return render(request, "components/exportreportlist.html", context)


class AddUser(View):

    def get(self, request):
        if  request.user.is_superuser:
            context= {}
            war = Warehouse.objects.filter(is_delete=False)
            storelist = Store.objects.filter(is_delete=False)

            context.update({"warehouse":war,"store":storelist,"title":"Add User"})
            return render(request, "components/adduser.html", context)

    def post(self, request):

        if request.user.is_superuser:
            context = {}
            validate = True
            war = Warehouse.objects.filter(is_delete=False)
            storelist = Store.objects.filter(is_delete=False)

            storeselect = request.POST.get('store', None)
            wareselect = request.POST.get('ware', None)
            password = request.POST.get('pwd', None)
            email = request.POST.get('email', None)
            lname = request.POST.get('lname', None)
            fname = request.POST.get('fname', None)
            uname = request.POST.get('uname', None)
            cnumber = request.POST.get('cnumber', None)
            print storeselect
            print wareselect
            print password
            print email
            print lname
            print fname
            print uname

            if storeselect=="000":
                validate=False
                context.update({"storeerror":"Please select store"})


            if wareselect=="00":
                validate=False
                context.update({"houseware":"Please select warehouse"})
                

            if not password:
                validate=False
                context.update({"pwde":"Please enter password"})

            if not email:
                validate=False
                context.update({"emaile":"Please enter email"})

            if not lname:
                validate=False
                context.update({"lnamee":"Please enter lastname "})

            if not fname:
                validate=False
                context.update({"fnamee":"Please enter firstname "})

            if not uname:
                validate=False
                context.update({"username":"Please enter username "})

            if not cnumber:
                validate=False
                context.update({"cnumbere":"Please enter contactnumber "})


            if validate:

                exist = User.objects.filter(username=uname)
                if len(exist) != 0:
                    context.update({"warehouse": wareselect, "store": storeselect, "title": "Add User",
                                    "error": "Username already exist"})
                    return render(request, "components/adduser.html", context)

                usr = User.objects.create_user(password=password,username=uname,email=email,first_name=fname,last_name=lname)

                if usr:
                    storeobj = Store.objects.get(id=storeselect)
                    warobj = Warehouse.objects.get(id=wareselect)
                    Acluser.objects.create(user=usr,warehouse=warobj, store=storeobj, contactnumber=cnumber)

                    context.update({"warehouse": wareselect, "store": storeselect, "title": "Add User","success":"Successfully created new user"})
                    return render(request, "components/adduser.html", context)

            else:
                context.update({"warehouse": wareselect, "store": storeselect, "title": "Add User"})
                return render(request, "components/adduser.html", context)



class UserList(View):
    """
        List for useList
    """
    def get(self, request):
        if request.user.is_superuser:
            context = {}
            usr = Acluser.objects.filter(user__is_active=True)
            context.update({"title":"Userlist", "userlist":usr})
            return render(request, "components/userlist.html", context)


class DeleteStore(View):
    """
        Delete Store
    """
    def get(self, request, pk):
        context={}
        if request.user.is_authenticated:

            stro = Store.objects.get(id=pk)
            stro.is_delete = True
            stro.save()
            str = Store.objects.filter(is_delete=False)

            context.update({"title": "Storelist", "store": str,"sucess":"Store record sucessfullly delete"})
            return render(request, "components/storelist.html", context)


class DeleteWarehouse(View):
    """
    Delete Warehouse
    """
    def get(selfself, request,pk):
        context={}
        if request.user.is_authenticated:
            war = Warehouse.objects.get(id=pk)
            war.is_delete=True
            war.save()
            ware = Warehouse.objects.filter(is_delete=False)
            context.update({"title": "Warehouselist", "warehouse": ware, "sucess":"Warehouse record sucessfullly delete"})
            return render(request, "components/warehouselist.html", context)


class DeleteUser(View):
    """
    Delete User
    """
    def get(selfself, request,pk):
        context={}
        if request.user.is_superuser:
            usr = User.objects.get(id=pk)
            usr.is_active=False
            usr.save()
            usrobj = Acluser.objects.filter(user__is_active=True)
            context.update({"title": "Userlist", "userlist": usrobj,"sucess":"Sucessfully Delete User"})
            return render(request, "components/userlist.html", context)



class EditUser(View):
    """
        Edit User
    """
    def get(self, request, pk):
        context={}
        if request.user.is_superuser:

            usr = Acluser.objects.get(user__is_active=True, user__id=pk)

            war = Warehouse.objects.filter(is_delete=False)

            store = Store.objects.filter(is_delete=False)
            context.update({"title": "Edit User", "warehouse": war, "storeobj":store,"user":usr})
            print store

            return render(request, "components/edituser.html", context)

    def post(self, request, pk):

        context = {}
        validate = True
        war = Warehouse.objects.filter(is_delete=False)
        storelist = Store.objects.filter(is_delete=False)

        storeselect = request.POST.get('store', None)
        wareselect = request.POST.get('ware', None)
        email = request.POST.get('email', None)
        lname = request.POST.get('lname', None)
        fname = request.POST.get('fname', None)
        uname = request.POST.get('uname', None)
        cnumber = request.POST.get('cnumber', None)
        print storeselect
        print wareselect
        print email
        print lname
        print fname
        print uname

        if storeselect == "000":
            validate = False
            context.update({"storeerror": "Please select store"})

        if wareselect == "00":
            validate = False
            context.update({"houseware": "Please select warehouse"})


        if not email:
            validate = False
            context.update({"emaile": "Please enter email"})

        if not lname:
            validate = False
            context.update({"lnamee": "Please enter lastname "})

        if not fname:
            validate = False
            context.update({"fnamee": "Please enter firstname "})

        if not uname:
            validate = False
            context.update({"username": "Please enter username "})

        if not cnumber:
            validate = False
            context.update({"cnumbere": "Please enter contactnumber "})

        if validate:

            # exist = User.objects.filter(username=uname)
            # if len(exist) != 0:
            #     context.update({"warehouse": wareselect, "store": storeselect, "title": "Add User",
            #                     "error": "Username already exist"})
            #     return render(request, "components/adduser.html", context)

            usr = User.objects.get(id=pk)
            usr.email = email
            usr.first_name = fname
            usr.last_name =  lname
            usr.username = uname
            usr.save()

            if usr:
                print storeselect
                storeobj = Store.objects.get(number=storeselect)
                warobj = Warehouse.objects.get(number=wareselect)
                acl = Acluser.objects.get(user_id=pk)
                acl.warehouse = warobj
                acl.store = storeobj
                acl.save()
                usrobj = Acluser.objects.filter(user__is_active=True)
                context.update({"title": "Userlist", "userlist": usrobj, "sucess": "Sucessfully Edit User Detail"})
                return render(request, "components/userlist.html", context)


        else:
            context.update({"warehouse": wareselect, "store": storeselect, "title": "Add User"})
            return render(request, "components/adduser.html", context)


class ProductList(View):
    """
        its all Data downloaded using Po Number
    """
    def get(self, request):
        context={}
        if request.user.is_authenticated:
            productdata = Product.objects.all()
            context.update({"title":"All Product","productobj":productdata })
            return render(request, "components/productlist.html", context)


class EditProduct(View):
    """
        Edit Product from Product list
    """
    def get(self, request, pk):
        context={}
        if request.user.is_authenticated:
            productdata = Product.objects.get(id=pk)
            context.update({"title":"Edit Product", "productobj":productdata })
            return render(request, "components/editproduct.html", context)


    def post(self, request, pk):

        context = {}
        if request.user.is_authenticated:
            validate = True
            vendorproductid = request.POST.get('vendorproductid', None)
            bin_loc = request.POST.get('bin_loc', None)
            pro_name = request.POST.get('pro_name', None)
            desc = request.POST.get('desc', None)
            quantity = request.POST.get('quantity', None)
            quantityindisplay = request.POST.get('quantityindisplay', None)
            picklist = request.POST.get('picklist', None)
            unit = request.POST.get('unit', None)
            tote = request.POST.get('tote', None)
            store_number = request.POST.get('store_number', None)

            # print vendorproductid
            # print bin_loc
            # print pro_name
            # print desc
            # print quantity
            # print quantityindisplay
            # print picklist
            # print unit
            # print tote
            # print store_number

            probj = Product.objects.get(id=pk)
            probj.vendor_product_id = vendorproductid
            probj.bin_location = bin_loc
            probj.product_name = pro_name
            probj.description = desc
            probj.quantity = quantity
            probj.quantityindisplay = quantityindisplay
            probj.picklist = picklist
            probj.unit = unit
            probj.tote = tote
            probj.store_number = store_number
            probj.save()
            productdata = Product.objects.all()
            context.update({"title": "All Product", "productobj": productdata})
            return render(request, "components/productlist.html", context)


class SFOProductList(View):
    """
        its all Data downloaded using Po Number
    """
    def get(self, request):
        context={}
        if request.user.is_authenticated:
            productdata = SFOProduct.objects.all()
            context.update({"title":"All SFOProduct","productobj":productdata })
            return render(request, "components/sfoproductlist.html", context)


class SFOEditProduct(View):
    """
        Edit Product from Product list
    """
    def get(self, request, pk):
        context={}
        if request.user.is_authenticated:
            productdata = SFOProduct.objects.get(id=pk)
            context.update({"title":"Edit SFOProduct", "productobj":productdata })
            return render(request, "components/sfoeditproduct.html", context)


    def post(self, request, pk):

        context = {}
        if request.user.is_authenticated:
            validate = True

            name = request.POST.get('name', None)
            bin = request.POST.get('bin', None)
            primary_vendor = request.POST.get('pri_vendor', None)
            export_unit = request.POST.get('export_unit', None)
            threshold = request.POST.get('threshold', None)
            quantityinhand = request.POST.get('quantityinhand', None)
            quantityinlayaway = request.POST.get('quantityinlayaway', None)
            quantityforsale = request.POST.get('quantityforsale', None)
            currentcost = request.POST.get('currentcost', None)
            primary_stock = request.POST.get('primary_stock', None)
            Conversion = request.POST.get('Conversion', None)

            # print name
            # print bin
            # print primary_vendor
            #
            # print export_unit
            # print threshold
            # print quantityinhand
            # print quantityinlayaway
            # print quantityforsale
            # print currentcost
            # print totalvalue
            # print primary_stock
            # print Conversion

            probj = SFOProduct.objects.get(id=pk)
            print float(quantityinhand)
            print quantityinhand
            probj.name = name
            probj.bin = bin
            probj.primary_vendor = primary_vendor
            probj.export_unit = export_unit
            probj.quantityinhand = float(quantityinhand)
            probj.threshold = threshold
            probj.quantityinlayaway = quantityinlayaway
            probj.quantityforsale = quantityforsale
            probj.currentcost = currentcost
            probj.primary_stock = primary_stock
            probj.Conversion = int(Conversion)
            probj.save()
            productdata = SFOProduct.objects.all()
            context.update({"title": "All SFOProduct", "productobj": productdata})
            return render(request, "components/sfoproductlist.html", context)

