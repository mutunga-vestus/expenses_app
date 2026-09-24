from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading


class EmailThread(threading.Thread):
    def __init__(self, email): 
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=True)    


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html') 
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)< 6:
                    messages.error(request,'Password too short')
                    return render(request, 'authentication/register.html',context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate',kwargs ={
                    'uidb64':uidb64,"token":token_generator.make_token(user)
                })

                activate_url = 'http://'+domain+link

                email_subject = 'Activate your account'
                email_body = 'Hi '+ user.username + \
                    'Please use this link to verify your account\n'+ activate_url

                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolony.com',
                    [email],
                )
                EmailThread(email).start()

                messages.success(request,'Account Created, please check your email to activate account')
                return render(request, 'authentication/register.html',  )
        return render(request, 'authentication/register.html')
    
class UsernamevalidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not username.isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric characters'}, status=400)
        
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error':'username already exixts, please choose another one'}, status=400)
            
        return JsonResponse({'username': True})    
    

class EmailvalidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':' the email is invalid'}, status=400)
        
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_error':'email already exixts, please choose another one'}, status=400)
            
        return JsonResponse({'email': True})  


class VerificationView(View):
    def get(self, request, uidb64,token):

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id) 
            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')
            if user.is_active:
                return redirect('login')
            user.is_active= True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex: 
            pass   
        return redirect('login')
            

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')    

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request, 'Welcome, '+
                                     user.username+' you are now logged in' )
                    return redirect('expenses')
                messages.error(
                    request, 'Account not active. Please check your email to activate') 
                return render(request, 'authentication/login.html')  
            messages.error(
                    request, 'Invalid Credentials. Try again') 
            return render(request, 'authentication/login.html')   
        messages.error(
                    request, 'Fill all fields') 
        return render(request, 'authentication/login.html')  

class LogoutView(View):
    def post(self, request):
        auth.logout(request)        
        messages.success(request,'you are logged out')
        return redirect('login')

class ResetPassword(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')

    def post(self, request):
        user_email = request.POST.get('email')
        context = {'values': request.POST}

        if not validate_email(user_email):
            messages.error(request, 'Please supply a valid email')
            return render(request, 'authentication/reset-password.html', context)

        user_qs = User.objects.filter(email=user_email)

        if user_qs.exists():
            user = user_qs.first()
            current_site = get_current_site(request)
            token_generator = PasswordResetTokenGenerator()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            link = reverse('reset-user-password', kwargs={
                'uidb64': uid,
                'token': token
            })

            reset_url = 'http://' + current_site.domain + link

            email_message = EmailMessage(
                'Password Reset Instructions',
                'Hi,\n\nClick the link below to reset your password:\n' + reset_url,
                'noreply@semicolon.com',
                [user_email],
            )
            EmailThread(email_message).start()

        messages.success(
            request,
            'Please check your email for password reset link.'
        )
        return render(request, 'authentication/reset-password.html')

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        return render(request, 'authentication/set-new-password.html', {
            'uidb64': uidb64,
            'token': token
        })

    def post(self, request, uidb64, token):
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        context = {'uidb64': uidb64, 'token': token}

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'authentication/set-new-password.html', context)

        if len(password) < 6:
            messages.error(request, 'Password too short')
            return render(request, 'authentication/set-new-password.html', context)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'Invalid reset link')
            return render(request, 'authentication/set-new-password.html', context)

        token_generator = PasswordResetTokenGenerator()

        if not token_generator.check_token(user, token):
            messages.error(request, 'Reset link is invalid or expired')
            return render(request, 'authentication/set-new-password.html', context)

        user.set_password(password)
        user.save()

        messages.success(request, 'Password reset successful. You can now log in.')
        return redirect('login')
    
   
