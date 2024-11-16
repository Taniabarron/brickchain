from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from app.buyer.models import Token
from app.core.models import Country
from app.core.utilis import _decrypt, _encrypt, validate_data
from app.core.views import save_logbook
from app.seller.models import Property, PropertyBuilding, PropertyDocs, PropertyImages, PropertyLand

@login_required
def properties(request):
    data = []
    action = []
    action_unique = []
    for p in Property.objects.filter(user_id=request.user).order_by("-timestamp"):
        
        if p.status:
            val = "checked"
            color = "success"
        else:
            val = "unchecked"
            color = "danger"
        image = PropertyImages.objects.filter(property=p).order_by('timestamp').values('path')[:1]
        counter = Token.objects.filter(property=p).count()
        country = Country.objects.get(code=p.country)
        print(counter)
        stock = p.tokens - counter 
        print(stock)
        data.append(
            {
                "Id": _encrypt(p.id),
                "Title": p.title,
                "Country": country.name,
                "Image": image[0]['path'],
                "CreateDate": p.timestamp.strftime("%d/%m/%Y"),
                "Status": val,
                "Color": color,
                "Address": p.address,
                "Tokens": p.tokens,
                "Stock": stock,
                "Cost": p.cost,
                "Type": p.property_type,
            }
        )
        if p.property_type not in action_unique:
            action_unique.append(p.property_type)
            action.append({'id': p.property_type, 'action': p.property_type})

    response = {
        "templates": data,
        "action": action
    }
    return render(request, 'app/seller/templates/properties.html', response)

@login_required
def status_properties(request):
    values = {}
    return values

@login_required
def form_properties(request):
    countries = Country.objects.all()
    list = []
    for r in countries:
        list.append({'code': r.code, 'name': r.name})
    response = {'list': list}
    return render(request, 'app/seller/templates/new-property.html', response)

@login_required
def add_properties(request):
    try:
        data = request.POST
        files = request.FILES

        print("Datos del formulario:", data)
        print("Archivos recibidos:", files)
        if validate_data(data):
            print(1234)
            property = Property.objects.create(title=data.get('title'),
                                            address=data.get('address'),
                                            city=data.get('city'),
                                            state=data.get('state'),
                                            country=data.get('country'),
                                            zip_code=data.get('zip_code'),
                                            property_type=data.get('property_type'),
                                            description=data.get('description'),
                                            valuation=data.get('valuation'),
                                            tokens=data.get('tokens'),
                                            cost=data.get('cost'),
                                            status=False,
                                            user_id=request.user)
            
            if data.get("property_type") == "Land":
                PropertyLand.objects.create(property=property,
                                            m2=data.get('m2_total'),
                                            length=data.get('length'),
                                            width=data.get('width'))
            elif data.get("property_type") == "House":
                
                PropertyBuilding.objects.create(property=property,
                                            m2_land=data.get('m2_land'),
                                            m2_house=data.get('m2_house'),
                                            age=data.get('age'),
                                            bathrooms=data.get('bathrooms'),
                                            half_baths=data.get('half_baths'),
                                            bedrooms=data.get('bedrooms'),
                                            furnished=data.get('furnished')=="1",
                                            garden=data.get('garden')=="1",
                                            pool=data.get('pool')=="1",
                                            land_use=data.get('land_use'),
                                            parking=data.get('parking'),
                                            services=data.get('services')=="1")
            else:
                PropertyBuilding.objects.create(property=property,
                                            m2_land=0,
                                            m2_house=data.get('m2_apartment'),
                                            age=data.get('age_apartment'),
                                            bathrooms=data.get('bathrooms_apartment'),
                                            half_baths=data.get('half_baths_apartment'),
                                            bedrooms=data.get('bedrooms_apartment'),
                                            furnished=data.get('furnished_apartment')=="1",
                                            garden=False,
                                            pool=False,
                                            land_use=data.get('land_use_apartment'),
                                            parking=data.get('parking_apartment'),
                                            services=data.get('services_apartment')=="1")
            
            if 'images' in request.FILES:
                for file in request.FILES.getlist('images'):
                    PropertyImages.objects.create(
                        property=property,
                        path=file
                    )
        
            # Lista de archivos que deseas guardar
            file_keys = ['ownership', 'identification']

            # Itera sobre la lista de claves y crea los objetos
            for key in file_keys:
                if key in request.FILES:  # Verifica que el archivo esté presente
                    PropertyDocs.objects.create(
                        property=property,
                        path=request.FILES[key]
                    )
            
            #Blockchain
            
            save_logbook("New property listing.", request.user.id) 
            
            #change response
            response = {"code": 200, "msg": "User created, verify your account!"}
        else:
            response = {"code": 401, "msg": "Some of the information contains invalid characters"}
    except Exception as e:
        print(e)
        response = {"code": 500, "msg": "We have not been able to create your property"}
    return JsonResponse(response)

@login_required
def status_properties(request):
    try:
        data = request.POST
        #validations
        if data.get('id') and data.get('checkbox'):
            resale = Property.objects.get(id=_decrypt(data.get('id')))
            resale.status = True if data.get('checkbox') == 'true' else False
            resale.save()
            
            save_logbook("Change a status property.", request.user.id) 
            
            response = {"code": 200, "msg": "Chage status successful!"}
        else:
            response = {"code": 401, "msg": "Some of the information contains invalid characters"}
    except Exception as e:
        print(e)
        response = {"code": 500, "msg": "We have not been able to complete your offer"}
    return JsonResponse(response)