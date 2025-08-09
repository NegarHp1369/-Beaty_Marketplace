
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, SellerProfileForm, CustomerProfileForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

class CustomerUserRegister(View):
    template_name = 'accounts/customer_register.html'
    def get(self, request):
        user_form = UserRegisterForm()
        profile_form = CustomerProfileForm()
        return render(request, self.template_name,
                      {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserRegisterForm(request.POST)
        profile_form = CustomerProfileForm(request.POST)
        if user_form.is_valid and profile_form.is_valid:
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('accounts:customer_dashboard')
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})


class SellerRegisterView(View):
    template_name = 'accounts/seller_register.html'
    def get(self, request):
        user_form = UserRegisterForm()
        profile_form = SellerProfileForm()
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserRegisterForm(request.POST)
        profile_form = SellerProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_staff = True
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('accounts:seller_dashboard')
        return render(request, self.template_name,
                      {'user_form': user_form, 'profile_form': profile_form})



class UserLoginView(View):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data =request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_staff:
                messages.success(request, f" you login successfully {user.username}")
                return redirect('accounts:seller_dashboard')
            else:
                messages.success(request, f'you login successfully :{user.username}')
                return redirect('accounts:customer_dashboard')
        messages.error(request, 'your username or your password is wrong')
        return render(request, self.template_name, {'form': form})



class UserLogoutView(View):
    def get(self, request):
        logout(request)

        return redirect('accounts:login')

class SellerDashboardView(View):
    def get(self, request):
        return render(request, 'accounts/seller_dashboard.html')

class CustomerDashboardView(View):
    def get(self, request):
        return render(request, 'accounts/customer_dashboard.html')