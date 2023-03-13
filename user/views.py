from django.shortcuts import render, redirect

# Create your views here.

# from django.contrib.auth import login as django_login, logout as django_logout, authenticate as django_authenticate
from django.contrib.auth import login as django_login, logout as django_logout, authenticate as django_authenticate
from django.contrib import messages

from .forms import LoginForm, RegistrationForm

# def login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         ...
#     else:
#         # Return an 'invalid login' error message.
#         ...


from django.views.generic import View

def login_page(request):
    '''rendering home view'''
    login_form = LoginForm
    register_form = RegistrationForm
    context = {
        'login_form':login_form,
        'register_form':register_form
    }
    return render(request, "user/login.html", context=context)


# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(data = request.POST)
#         if form.is_valid():
#             email = request.POST['email']
#             password = request.POST['password']
#             user = django_authenticate(email=email, password=password)
#             if user is not None:
#                 if user.is_active:
#                     django_login(request,user)
#                     return redirect('home:home') #user is redirected to dashboard
#     else:
#         # form = LoginForm()
#         return redirect('user:login')

#     return render(request,'user/login.html', context={'login_form': form })

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(data = request.POST)
#         if form.is_valid():
#             user = form.save()
#             u = django_authenticate(email =user.email, password=user.password )
#             django_login(request,u)
#             return redirect('home:home')
#     else:
#         return redirect('user:login')

#     return render(request,'user/login.html', context={'registration_form': form })

def logout(request):
    django_logout(request)
    return redirect('user:login_page')

def login(request):
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(email, password)
            user = django_authenticate(username=email, password=password)
            print(user)
            if user is not None:
                if user.is_active:
                    django_login(request,user)
                    return redirect('home:home') #user is redirected to dashboard
            else:
                # form = LoginForm()
                return redirect('user:login_page')
    else:
        # form = LoginForm()
        return redirect('user:login_page')
    
def register(request):
    form = RegistrationForm(request.POST)
    message = ''
    if request.method == 'POST':
        print(request)
        # form = RegisterForm(request.POST)
        if form.is_valid():
            # print(request)
            user = form.save()
            django_login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        # form = LoginForm()
        return redirect('user:login_page')
# class LoginPageView(View):
#     form_classes = {
#       'login_form' : LoginForm,
#       'register_form' : RegisterForm,
#    }
#     template_name = 'user/login.html'
    
#     def get(self, request):
#         message = ''
#         return render(request, self.template_name, context={'message': message})
        
#     def post(self, request):
#         print(request.POST)
#         username = request.POST.get('username')
#         password = request.POST.get('pass')
#         print(username, password)
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home:home')
#         else:
#             message = 'Login failed!'
#             return render(request, self.template_name, context={'message': message})
    # form_class = LoginForm
    
    # def get(self, request):
    #     form = self.form_class()
    #     message = ''
    #     return render(request, self.template_name, context={'form': form, 'message': message})
        
    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         user = authenticate(
    #             username=form.cleaned_data['username'],
    #             password=form.cleaned_data['password'],
    #         )
    #         if user is not None:
    #             login(request, user)
    #             return redirect('home')
    #     message = 'Login failed!'
    #     return render(request, self.template_name, context={'form': form, 'message': message})