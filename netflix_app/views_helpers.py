from django.http import JsonResponse
import json


## error helper methods

def error_on_request(error):
    return JsonResponse(data={"error": error}, status=400)

def bad_request():
    return error_on_request("Bad Request.")


## request helper methods

def get_items(ModelType, SerializerType):
    try:
        items = ModelType.objects.all()
        serialized_data = SerializerType().serialize_all(items)
        return JsonResponse(data=serialized_data, status=200, safe=False)
    
    except Exception as e:
        return error_on_request(str(e))

def get_item(ModelType, SerializerType, item_id):
    try: 
        item = ModelType.objects.get(id=item_id)
        serialized_data = SerializerType().serialize(item)
        return JsonResponse(data=serialized_data, status=200) 
    
    except Exception as e:
        return error_on_request(str(e))

def save_create_item(form_data, ModelType, FormType, SerializerType, item_id=None, disabled_fields_for_update=None):
    try: 
        item = ModelType.objects.get(id=item_id) if item_id else None
        form = FormType(form_data, instance=item) # handles data extraction and validation!

        # silently (i.e. don't raise an error) ignore data updates for specified fields
        if disabled_fields_for_update:
            for field_name in disabled_fields_for_update:
                form.fields[field_name].disabled = True

        if form.is_valid():
            item = form.save()
            serialized_data = SerializerType().serialize(item)
            return JsonResponse(data=serialized_data, status=200)
        else:
            errors = json.dumps(form.errors)
            raise Exception(errors)
    
    except Exception as e:
        return error_on_request(str(e))

def delete_item(ModelType, item_id):
    try: 
        item = ModelType.objects.get(id=item_id)
        item.delete()
        return JsonResponse(data={"result": f"Successfully Deleted {type(item).__name__}."}, status=203)
    
    except Exception as e:
        return error_on_request(str(e))


## view helper methods

def list_view(request, ModelType, FormType, SerializeType):
    if request.method == "GET":
        return get_items(ModelType, SerializeType)
    
    if request.method == "POST":
        return save_create_item(json.load(request), ModelType, FormType, SerializeType)

    return bad_request()


def detail_view(request, ModelType, FormType, SerializerType, item_id, disabled_fields_for_update=None):    
    if request.method == "GET":
        return get_item(ModelType, SerializerType, item_id)

    if request.method == "PUT":
        return save_create_item(json.load(request), ModelType, FormType, SerializerType, item_id, disabled_fields_for_update)

    if request.method == "DELETE":
        return delete_item(ModelType, item_id)

    return bad_request()