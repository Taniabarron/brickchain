import uuid
from django.contrib.auth import authenticate, login, logout as do_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect

from app.core.models import *
from app.core.utilis import SendMailMailJet, _checkVarchar, render_template, validate_data


def index(request):
    values = {}
    return render(request, 'app/core/templates/onboarding/index.html', values)

def sing_in(request):
    values = {}
    return render(request, 'app/core/templates/onboarding/login.html', values)

def user_exists(email):
    return User.objects.filter(username=email).exists()

def save_logbook(action, user): 
    return Logbook.objects.create(action=action,user_id=user)

@csrf_exempt
def account_create(request):
    try:
        data = request.POST
        if validate_data(data):
            if not user_exists(data.get('email').lower()):
                user = User.objects.create_user(username=data.get('email').lower(),
                                            email=data.get('email').lower(),
                                            first_name=data.get('fullname'),
                                            password=data.get('password'))

                token_pass = uuid.uuid4()
                Profile.objects.create(user=user,
                                       account_status=False,
                                       token_pass=token_pass,
                                       user_type=data.get('type'),
                                       terms=data.get('agree') == "on")
                
                #check email
                html = render_template('check-email')
                content = html.replace('{{email}}',data.get('email').lower()).replace('{{BASE_URL_PAGE}}', str(request.headers.get('Origin'))).replace(
                '{{token}}', str(token_pass))
                SendMailMailJet(subject="Verify your account", 
                                body=content, 
                                email_to=[{"Email": data.get('email').lower(), 
                                           "Name": data.get('fullname')}])
                save_logbook("Account creation", user.id)
                response = {"code": 200, "msg": "User created, verify your account!"}
            else:
                response = {"code": 400, "msg": "User previously registered."}
        else:
           
            response = {"code": 401, "msg": "We have not been able to create your user. 1"}
    except Exception as e:
        print(e)
        response = {"code": 500, "msg": "We have not been able to create your user. 2"}
    return JsonResponse(response)
    

@csrf_exempt
def user_authenticate(request):
    try:
        data = request.POST
        if not _checkVarchar(data.get('username').lower()):
            user = authenticate(username=data.get('username').lower(), password=data.get('password'))
            my_old_sessions = Session.objects.all()
            for row in my_old_sessions:
                if row.get_decoded().get("username") == data.get('username'):
                    row.delete()
            if user:
                profile = Profile.objects.get(user=user)
                if profile.account_status:
                    save_logbook("Login", user.id)
                    login(request, user)
                    request.session['username'] = user.username
                    request.session['userid'] = user.id
                    request.session['name'] = user.first_name
                    request.session['rol'] = profile.user_type
                    request.session['initial'] = user.username[0].upper()
                    response = {"code": 200, "msg": ""}
                else:
                    response = {"code": 400, "msg": "Unverified account."}
            else:
               response = {"code": 400, "msg": "Incorrect username or password."}
        else:
           
            response = {"code": 401, "msg": "We have not been able to create your user."}
    except Exception as e:
        print(e)
        response = {"code": 500, "msg": "We have not been able to create your user."}
    return JsonResponse(response)

def logout(request):
    save_logbook("Logout.", request.session['userid'])
    do_logout(request)
    return redirect('/')

@csrf_exempt
def user_verify(request, token):
    if not _checkVarchar(token) and Profile.objects.filter(token_pass=token).exists():
        profile = Profile.objects.get(token_pass=token)
        if profile.account_status == False:
            profile.account_status = True
            profile.save()
        #succes page (no time)
        return redirect('/login')
    else:
        #404 error page (no time)
        return redirect('/')

@csrf_exempt
def reset_password_send(request):
    data = request.POST
    try:
        if not User.objects.filter(username=data.get('email').lower()).exists():
            response = {"code": 500, "msg": "No hemos podido encontrar tu usuario."}
        else:
            user = User.objects.get(username=data.get('email'))
            token_pass = uuid.uuid4()
            profile = Profile.objects.get(user=user.id)
            profile.token_pass = token_pass
            profile.save()
            #check email
            html = render_template('change-password')
            content = html.replace('{{BASE_URL_PAGE}}', str(request.headers.get('Origin'))).replace('{{token}}', str(token_pass))
            SendMailMailJet(subject="Reset your password", body=content, email_to=[{"Email": data.get('email').lower(),"Name": data.get('fullname')}])
            save_logbook("Request for password change.", user.id)
            response = {"code": 200, "msg": "We have sent the email for password change."}
    except Exception as e:
        print(e)
        response = {"code": 500, "msg": "We couldn't find your username."}
    return JsonResponse(response)

@csrf_exempt
def change_password(request, token):
    if not _checkVarchar(token) and Profile.objects.filter(token_pass=token).exists():
        response = {'token': token}
        #succes page (no time)
        return render(request, 'app/core/templates/onboarding/change-password.html', response)
    else:
        #404 error page (no time)
        return redirect('/')


def reset_password(request):
    data = request.POST
    password = data.get('password')
    cpassword = data.get('cpassword')
    token = data.get('token')
    token = token.strip('/')
    try:
        if password != cpassword:
            response = {"code": 500, "msg": "Passwords are not the same, please verify them."}
        else:
            profile = Profile.objects.get(token_pass=token)
            if profile == "":
                response = {"code": 500, "msg": "We have not been able to verify the verification token."}
            else:
                user = User.objects.get(pk=profile.user_id)
                user.set_password(data.get('password'))
                profile.token_pass = uuid.uuid4()
                save_logbook("Made a password change.", user.id)
                html = render_template('new-password')
                content = html.replace('{{BASE_URL_PAGE}}', str(request.headers.get('Origin')))
                SendMailMailJet(subject="New password", body=content, email_to=[{"Email": user.username,"Name": user.first_name}])
                profile.save()
                user.save()
                response = {"code": 200, "msg": "Your password has been successfully changed."}
    except Exception as e:
        print(e)
        response = {"code": 500, "msg": "We couldn't find your username."}
    return JsonResponse(response)

@login_required
def logbook(request):
    logbook = Logbook.objects.filter(user_id=request.user.id)
    action = []
    action_unique = []
    for r in logbook:
        if r.action not in action_unique:
            action_unique.append(r.action)
            action.append({'id': r.action, 'action': r.action})
    response = {'action': action}
    return render(request, 'app/core/templates/user/logbook.html', response)

@login_required
@csrf_exempt
def get_logbook(request):
    logbook = Logbook.objects.filter(user_id=request.user.id)
    size = len(logbook)
    response = {"meta": {
        "page": 1,
        "pages": size / 10,
        "perpage": -1,
        "total": size,
        "sort": "asc",
        "field": "RecordID"}
    }
    data = []
    for r in logbook:
        data.append({'RecordID': r.id,
                     'Action': r.action,
                     'ShipDate': r.timestamp})
    response.update({'data': data})
    return JsonResponse(response)

@login_required
def test(request):
    values = {}
    return render(request, 'app/core/templates/home.html', values)