from dashboard.models import *
from dashboard.api.serializer import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, login, logout
from operator import itemgetter


class Warehouselist(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = WarehouseSerializer(queryset, many=True)
        context={"success":1,"warehouseList":serializer.data}
        return Response(context)


class Storelist(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, warehouse):
        queryset = Store.objects.filter(warehouse=warehouse)
        serializer = StoreSerializer(queryset, many=True)
        context = {"success": 1, "storeList": serializer.data}
        return Response(context)


class getfirstrecord(APIView):
    """
        get first record .
    """
    def get(self, request, user_id,s_id,w_id,picklist):
        print user_id
        print s_id
        print w_id
        #user_id = user_id
        print picklist
        queryset = Product.objects.filter(warehouse=w_id,
                                         store=s_id,
                                         picklist=picklist)

        #serializer = ProductSerializer(queryset, many=True)
        serializer = ProductSerializer(queryset, many=True)
        newlist = sorted(serializer.data, key=itemgetter('bin_location'))

        context = {"success": 1, "Productlist": [newlist[0]]}
        return Response(context)


class getpicklist(APIView):
    """
        get picklist base on store .
    """
    def get(self, request, s_id):
        now = datetime.datetime.now()
        print "sss",s_id
        print now.day
        print now.year
        print now.month
        queryset = Product.objects.distinct('picklist').filter(store=s_id,created_at__day=now.day,created_at__month=now.month,created_at__year=now.year)
        serializer = ProductPickSerializer(queryset, many=True)
        context = {"success": 1, "picklist": serializer.data}
        return Response(context)


class getproduct(APIView):
    """
        get product filter .
    """
    def get(self, request, bin_location,barcode_num,user_id, s_id, w_id):
        print "sss",bin_location
        print barcode_num
        print user_id
        print s_id
        print w_id
        #user_id = user_id,
        queryset = list(Product.objects.filter(bin_location=bin_location,barcode_num=barcode_num,store=s_id,warehouse=w_id).order_by('bin_location'))
        serializer = ProductSerializer(queryset, many=True)
        context = {"success": 1, "productlist": serializer.data}
        return Response(context)


class getreport(APIView):
    """
        get product filter .
    """
    def get(self, request, user_id, tote):

        print user_id
        print tote
        #user_id = user_id
        queryset = Product.objects.filter(tote=tote,)
        serializer = ProductSerializer(queryset, many=True)
        context = {"success": 1, "toteproductlist": serializer.data}
        return Response(context)


class userlogin(APIView):

    """
        userlogin
    """

    def get(self, request, username, password,dtoken,did):
        print username
        print password
        print dtoken
        print did
        context={}
        user = authenticate(username=username, password=password)
        if user is not None:
            print "hii"
            if user.is_superuser:
                context.update({'user_data': {'user_id': user.id, 'username': user.username,
                                              
                                              }})
                context.update({"success": 1, "message": "login successfull"})
                return Response(context)
            else:

                aclobj = Acluser.objects.get(user=user.id)
                Device.objects.create(user_id=user.id,dtoken=dtoken,did=did)
                context.update({'user_data':{'user_id':user.id,'username':user.username,
                                             'firstname':user.first_name,
                                             'lastname':user.last_name,
                                             'email':user.email,
                                             'device_tocken':dtoken,
                                             'phone':aclobj.contactnumber
                                             }})
                context.update({"success":1,"message":"login successfull"})


        else:
            context.update({"success": 0, "message": "invalid username and password"})

        return Response(context)


class getnextproduct(APIView):

    def get(self, request, product_id, user_id, picklist, bin_location):

            print bin_location
            binobj = Product.objects.filter(bin_location=bin_location, picklist=picklist).exclude(id=product_id).order_by('id')
            print "dddddd",binobj
            list_bin=[]
            if len(binobj) >= 1:

                for bin in binobj:
                    print "binnnnnnnnn",bin.id
                    if bin.id > int(product_id):
                        print "ttt"
                        list_bin.append(bin.id)
                    else:
                        print "moo"


                for lid in list_bin:
                    print "lid"
                    if lid <= int(product_id):
                        print "rrrlid"
                        list_bin.remove(lid)
                print "fffffffffff",list_bin

                print "final id",list_bin
                if len(list_bin) >= 1:
                    newquery = Product.objects.filter(picklist=picklist,id__in=list_bin).order_by('id')
                    print newquery
                    serializer = ProductSerializer(newquery, many=True)
                    context = {"success":1, "nextproductlist": [serializer.data[0]]}
                    return Response(context)
                else:
                    newquery = Product.objects.filter(picklist=picklist, bin_location__gt=bin_location).order_by('bin_location')
                    print newquery

                    serializer = ProductSerializer(newquery, many=True)
                    newlist = sorted(serializer.data, key=itemgetter('bin_location'))
                    temp_check = serializer.data[0]
                    bin = temp_check['bin_location']
                    print bin
                    binduplicate = Product.objects.filter(picklist=picklist, bin_location=bin).order_by('id')
                    if len(binduplicate) > 1:
                        serializer = ProductSerializer(binduplicate, many=True)
                        newlist = sorted(serializer.data, key=itemgetter('product_id'))

                    context = {"success": 1, "nextproductlist": [newlist[0]]}
                    return Response(context)


            newquery = Product.objects.filter(picklist=picklist, bin_location__gt=bin_location).exclude(id=product_id).order_by(
                'bin_location')


            serializer = ProductSerializer(newquery, many=True)
            newlist = sorted(serializer.data, key=itemgetter('bin_location'))
            a = serializer.data[0]
            print a['bin_location']
            newid = []
            holdid = []
            dubobj = Product.objects.filter(picklist=picklist, bin_location=a['bin_location']).order_by('id')
            if len(dubobj) > 1:
                print "morethan1"
                serializer = ProductSerializer(dubobj, many=True)
                newlist = sorted(serializer.data, key=itemgetter('product_id'))
                #print newlist
                temp = newlist[0]

                for obj in dubobj:
                    newid.append(obj.id)


                print newid[0]
                print "ssssssss",product_id


                if newid[0] != int(product_id):
                    if int(product_id) not in newid:
                        print "yes",newid
                        context = {"success": 1, "nextproductlist": [newlist[0]]}
                        return Response(context)
                    else:

                        for ids in newid:
                            if ids > int(product_id):
                                holdid.append(ids)
                        print holdid
                        if len(holdid) > 0:
                            print "ggg", holdid
                            muldupli = Product.objects.filter(picklist=picklist, bin_location=bin_location,
                                                              id__in=holdid).order_by('bin_location')
                            serializer = ProductSerializer(muldupli, many=True)
                            duplist = sorted(serializer.data, key=itemgetter('product_id'))
                            context = {"success": 1, "nextproductlist": [duplist[0]]}
                            return Response(context)
                        else:
                            context = {"success": 1, "nextproductlist": [newlist[0]]}
                            return Response(context)


                else:
                    for ids in newid:
                        if ids > int(product_id):
                            holdid.append(ids)
                    print holdid
                    if len(holdid) > 0:
                        print "ggg",holdid
                        muldupli = Product.objects.filter(picklist=picklist, bin_location=bin_location,
                                                        id__in=holdid).order_by('bin_location')
                        serializer = ProductSerializer(muldupli, many=True)
                        duplist = sorted(serializer.data, key=itemgetter('product_id'))
                        context = {"success": 1, "nextproductlist": [duplist[0]]}
                        return Response(context)
            else:

                context = {"success": 1, "nextproductlist": [newlist[0]]}
                return Response(context)

class getnextproductq(APIView):
    """
        get next product filter .
    """

    def get(self, request, product_id, user_id,  picklist, bin_location):


        try:
            binobj = Product.objects.filter(bin_location=bin_location,picklist=picklist)
            #print binobj
            if len(binobj) > 1:

                newquery = Product.objects.filter(picklist=picklist,bin_location=bin_location,  id__gt=product_id).order_by('bin_location')
                #print "dd", newquery

                serializer = ProductSerializer(newquery, many=True)
                newlist = sorted(serializer.data, key=itemgetter('bin_location'))
                if len(newlist) < 1:
                    queryset = Product.objects.filter(id=product_id, picklist=picklist, bin_location=bin_location).order_by(
                        'bin_location')[0]
                    print "ssssss", queryset

                    newquery = Product.objects.filter(id__gte=product_id,picklist=picklist, bin_location__gt=bin_location).order_by(
                        'bin_location')
                    print "dd", newquery

                    serializer = ProductSerializer(newquery, many=True)
                    new = sorted(serializer.data, key=itemgetter('bin_location'))
                    if new >=1:
                        context = {"success": 1, "nextproductlist": [new[0]]}
                        return Response(context)
                    else:
                        context = {"success": 0, "message": "please  select another picklsit"}
                        return Response(context)


                context = {"success": 1, "nextproductlist": [newlist[0]]}
                return Response(context)

            queryset = Product.objects.filter(id=product_id, picklist=picklist, bin_location=bin_location).order_by(
                'bin_location')[0]
            print "ssssss", queryset

            newquery = Product.objects.filter(picklist=picklist, bin_location__gt=bin_location).order_by('bin_location')
            print "dd", newquery

            serializer = ProductSerializer(newquery, many=True)
            newlist = sorted(serializer.data, key=itemgetter('bin_location'))
            context = {"success": 1, "nextproductlist": [newlist[0]]}
            return Response(context)
        except:
            context={}
            context = {"success": 0, "message": "please  select another picklsit"}
            return Response(context)

class UpdateProduct(APIView):

    def get(self, request,product_id,barcode_num,quntity,bin_location,user_id,tote,picklist):

        # print product_id
        # print barcode_num
        print quntity
        # print bin_location
        # print user_id
        # print tote
        # print picklist

        try:
            objlist = Product.objects.filter(barcode_num=barcode_num,id=product_id, picklist=picklist, bin_location=bin_location).order_by('bin_location')[0]
            print objlist
            objlist.tote = str(tote)
            objlist.quantity = str(quntity)
            objlist.save()

            # for obj in objlist:
            #     obj.tote = str(tote)
            #
            #     obj.quantity = str(quntity)
            #     obj.save()
            binobj = Product.objects.filter(bin_location=bin_location, picklist=picklist)
            # print binobj
            # if len(binobj) > 1:
            #     print "hiii"
            #     newquery = Product.objects.filter(picklist=picklist,bin_location=bin_location, id__gt=product_id).order_by('bin_location')
            #     # print "dd", newquery
            #
            #     serializer = ProductSerializer(newquery, many=True)
            #     newlist = sorted(serializer.data, key=itemgetter('bin_location'))
            #     if len(newlist) < 1:
            #         context = {"success": 0, "message": "please  select another picklsit"}
            #         return Response(context)
            #
            #     context = {"success": 1, "updateproductlist": [newlist[0]]}
            #     return Response(context)

            list_bin = []
            if len(binobj) >= 1:

                for bin in binobj:
                    print "binnnnnnnnn", bin.id
                    if bin.id > int(product_id):
                        print "ttt"
                        list_bin.append(bin.id)
                    else:
                        print "moo"

                for lid in list_bin:
                    print "lid"
                    if lid <= int(product_id):
                        print "rrrlid"
                        list_bin.remove(lid)
                print "fffffffffff", list_bin

                print "final id", list_bin
                if len(list_bin) >= 1:
                    newquery = Product.objects.filter(picklist=picklist, id__in=list_bin).order_by('id')
                    print newquery
                    serializer = ProductSerializer(newquery, many=True)
                    context = {"success": 1, "updateproductlist": [serializer.data[0]]}
                    return Response(context)
                else:
                    newquery = Product.objects.filter(picklist=picklist, bin_location__gt=bin_location).order_by(
                        'bin_location')
                    print newquery

                    serializer = ProductSerializer(newquery, many=True)
                    newlist = sorted(serializer.data, key=itemgetter('bin_location'))
                    temp_check = serializer.data[0]
                    bin = temp_check['bin_location']
                    print bin
                    binduplicate = Product.objects.filter(picklist=picklist, bin_location=bin).order_by('id')
                    if len(binduplicate) > 1:
                        serializer = ProductSerializer(binduplicate, many=True)
                        newlist = sorted(serializer.data, key=itemgetter('product_id'))

                    context = {"success": 1, "updateproductlist": [newlist[0]]}
                    return Response(context)
            else:

                newquery = \
                Product.objects.filter(picklist=picklist, bin_location__gt=bin_location).order_by('bin_location')

                serializer = ProductSerializer(newquery,many=True)
                newlist = sorted(serializer.data, key=itemgetter('bin_location'))
                temp_check = serializer.data[0]
                bin = temp_check['bin_location']
                print bin
                binduplicate = Product.objects.filter(picklist=picklist, bin_location=bin).order_by('id')
                if len(binduplicate) > 1:
                    serializer = ProductSerializer(binduplicate, many=True)
                    newlist = sorted(serializer.data, key=itemgetter('product_id'))

                    context = {"success": 1, "updateproductlist": [newlist[0]]}
                    return Response(context)


                context = {"success": 1, "updateproductlist": [newlist[0]]}
                return Response(context)

        except:
            context={}
            context = {"success": 0, "message": "please  select another picklsit"}
            return Response(context)



class getpreviousproduct(APIView):
    """
        get next product filter .
    """

    def get(self, request, product_id, user_id,  picklist, bin_location):

        try:
            print "previous"
            #user_id = user_id
            queryset = Product.objects.filter(id=product_id,  picklist=picklist, bin_location=bin_location).order_by('bin_location')[0]
            binobj = Product.objects.filter(bin_location=bin_location, picklist=picklist)
            # print binobj
            if len(binobj) > 1:
                print "hiii"
                newquery = Product.objects.filter(bin_location=bin_location, id__lt=product_id).order_by(
                    'bin_location')
                # print "dd", newquery

                serializer = ProductSerializer(newquery, many=True)
                newlist = sorted(serializer.data, key=itemgetter('bin_location'))
                context = {"success": 1, "previousproductlist": [newlist[0]]}
                return Response(context)

            newquery = Product.objects.filter(picklist=picklist,bin_location__lt=bin_location).order_by('-bin_location')[0]


            serializer = ProductSerializer(newquery)
            context = {"success": 1, "previousproductlist": [serializer.data]}
            return Response(context)
        except:
            context={}
            context = {"success": 0, "message": "please  select another picklsit"}
            return Response(context)


class SFOData(APIView):

    """
        
    """
    def post(self, request):
        data = request.data
        sku =  data.get('sku')


        if not sku:
            context = {"success": 0, "Message": "Please enter valid Barcode or SKU"}
            return Response(context)
        else:
            try:
                queryset = SFOProduct.objects.get(sku=sku)
                if queryset:
                    serializer = SFOProductSerializer(queryset)
                    context = {"success": 1, "SFOProduct": [serializer.data]}
                    return Response(context)
            except:
                pass
            try:
                queryset = SFOProduct.objects.get(barcode=sku)
                serializer = SFOProductSerializer(queryset)
                context = {"success": 1, "SFOProduct": [serializer.data]}
                return Response(context)
            except:
                context = {"success": 0, "Message": "Please enter valid Barcode or SKU"}
                return Response(context)

