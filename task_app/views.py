from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from .serializers import Account_serializer,Destination_serializers
from .models import Account_Module,Destination_Module
from rest_framework.response import Response
import numpy as np
from django.http import QueryDict
def random_generate_id():
    number=np.random.randint(9999999999, size=1)
    print(number)
    if Account_Module.objects.filter(App_secret_token=number).exists():
        print("exists")
        number=np.random.randint(9999, size=1)
    
    return number


##### 

"""
POST DATA in account module and destination module
if the update using put api the token also be updated
"""
@api_view(['POST','PUT'])
def post_data(request):
    try:
        token=random_generate_id()

        if request.method == 'POST' or request.method == 'PUT':
            post_dict={}
            post_dict['email_id']=request.data['email_id']
            post_dict['account_id']=request.data['account_id']
            post_dict['account_name']=request.data['account_name']
            post_dict['App_secret_token']=str(token[0])
            post_dict['website']=request.data['website']
            query_dict = QueryDict('', mutable=True)
            query_dict.update(post_dict)

            if Account_Module.objects.filter(account_id=request.data['account_id']).exists()==False:

                serializers=Account_serializer(data=query_dict)
                
                if serializers.is_valid():
                    serializers.save()

                    headers_array={"APP_ID":request.META['HTTP_HOST'],"ACTION":request.META['REQUEST_METHOD'],"content-type":request.META['CONTENT_TYPE'],"Accept":request.META['HTTP_ACCEPT']}

                    Destination_Module.objects.create(URL='localhost:8000/get_account/?id='+str(post_dict['account_id'])
                    ,http_method=request.method,headers=headers_array,account_id=str(serializers.data['id']))
                    return Response({"data":"Registered successfully"})
                else:
                    return Response({"ERROR":serializers.error_messages})
            else:
                print("else")
                query=Account_Module.objects.get(account_id=request.data['account_id'])
                serializers=Account_serializer(instance=query,data=query_dict,partial=True)
                print(serializers.is_valid(),"Update")
                if serializers.is_valid():
                    serializers.save()
                    
                    headers_array={"APP_ID":request.META['HTTP_HOST'],"ACTION":request.META['REQUEST_METHOD'],"content-type":request.META['CONTENT_TYPE'],"Accept":request.META['HTTP_ACCEPT']}

                    Destination_Module.objects.filter(account_id=serializers.data['id']).update(URL='localhost:8000/get_destination/?id='+str(post_dict['account_id'])
                    ,http_method=request.method,headers=headers_array,account_id=str(serializers.data['id']))
                    return Response({"data":"Updated successfully"})
                else:
                    return Response({"ERROR":serializers.error_messages})

        # elif request.method == 'PUT':

    except Exception as e:
        return Response(str(e))


### 
"""
GET all data or get particular account id and copy the token for get destination api
"""
@api_view(['GET'])
def get_account(request):
    if request.method=='GET' and 'account_id' not in request.GET.keys():
            account_query=Account_Module.objects.all()
            serializer=Account_serializer(instance=account_query,many=True)
            print(serializer.data)
            return Response(serializer.data)
    else:
            if Account_Module.objects.filter(account_id=request.GET['account_id']).exists():
                account_query=Account_Module.objects.filter(account_id=request.GET['account_id'])
                serializer=Account_serializer(instance=account_query,many=True)
                print(serializer.data)
                return Response(serializer.data)
            else:
                return Response({"data":"Invalid data"})



"""
get destination data using auth token set in headers
"""
@api_view(['GET'])
def get_destination(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        if Account_Module.objects.filter(App_secret_token=request.META['HTTP_AUTHORIZATION']).exists():
            account_ids= Account_Module.objects.filter(App_secret_token=request.META['HTTP_AUTHORIZATION']).values()
            print(account_ids[0]['id'])
            if Destination_Module.objects.filter(account_id=account_ids[0]['id']).exists():
                query_des=Destination_Module.objects.filter(account_id=account_ids[0]['id']).values()
                print(query_des)
                # serializer=Destination_serializers(instance=query_des,many=True)
                return Response(query_des)
            
        else:
            return Response({"Token ":"Un Authenticate"})
    else:
        return Response({"error":"set Authorization in headers"})