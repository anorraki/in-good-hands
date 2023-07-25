from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View

from giveaway_app.forms import RegisterForm, LoginForm, EditProfileForm, EditPasswordForm
from giveaway_app.models import Donation, Institution, Category


# Create your views here.
class LandingPageView(View):
    def get(self, request):
        donations = Donation.objects.all()
        foundations = Institution.objects.filter(type=0)
        ngos = Institution.objects.filter(type=1)
        local_collections = Institution.objects.filter(type=2)
        all_bags = 0
        organizations_donated = []
        for donation in donations:
            all_bags += donation.quantity
            if donation.institution not in organizations_donated:
                organizations_donated.append(donation.institution)
        context = {
            "all_bags": all_bags,
            "organizations_donated_amount": len(organizations_donated),
            "foundations": foundations,
            "ngos": ngos,
            "local_collections": local_collections,
        }
        return render(request, 'index.html', context)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            registered_user = User.objects.filter(email=email)
            if user is None:
                context = {
                    'form': form,
                    'message': 'Błędne dane logowania!',
                }
                return render(request, 'login.html', context)
            elif not registered_user:
                return redirect(reverse('register'))
            else:
                login(request, user)
                url = request.GET.get('next', 'landing_page')
                return redirect(url)
        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('landing_page'))


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        context = {
            'form': form,
        }
        return render(request, 'register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            User.objects.create_user(username=email, email=email,
                                     first_name=first_name, last_name=last_name,
                                     password=password)
            return redirect(reverse('landing_page'))
        return render(request, "register.html", context={"form": form})


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        context = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, 'form.html', context)

    def post(self, request):
        quantity = request.POST.get("bags")
        categories_id = request.POST.getlist("categories")
        categories = Category.objects.filter(pk__in=categories_id)
        institution_id = request.POST.get("organization")
        institution = Institution.objects.get(pk=institution_id)
        address = request.POST.get("address")
        city = request.POST.get("city")
        zip_code = request.POST.get("postcode")
        phone_number = request.POST.get("phone")
        pick_up_date = request.POST.get("date")
        pick_up_time = request.POST.get("time")
        comment = request.POST.get("more_info")
        donation = Donation(quantity=quantity, address=address, phone_number=phone_number,
                            city=city, zip_code=zip_code, pick_up_date=pick_up_date,
                            pick_up_time=pick_up_time, pick_up_comment=comment, user=request.user,
                            institution_id=institution.id)
        donation.save()
        donation.categories.set(categories)
        return redirect("form_confirmation")


class DonationConfirmationView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "form-confirmation.html")


class DonationSetTakenView(LoginRequiredMixin, View):
    def get(self, request, donation_id):
        donation = get_object_or_404(Donation, pk=donation_id)
        donation.is_taken = not donation.is_taken
        donation.save()
        return redirect('/profile/#donations')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_donations = Donation.objects.filter(user_id=request.user.id).order_by('is_taken', '-pick_up_date')
        context = {
            "user": request.user,
            "donations": user_donations,
        }
        return render(request, 'profile.html', context)


class EditUserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(initial={"first_name": request.user.first_name,
                                        "last_name": request.user.last_name,
                                        "email": request.user.email})
        return render(request, 'edit-profile.html', context={"form": form})

    def post(self, request):
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.email, password=form.cleaned_data["password"])
            if user is not None:
                user.username = form.cleaned_data["email"]
                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.email = form.cleaned_data["email"]
                user.save()
                return redirect(reverse('profile'))
            else:
                form = EditProfileForm(initial={"first_name": form.cleaned_data["first_name"],
                                                "last_name": form.cleaned_data["last_name"],
                                                "email": form.cleaned_data["email"]})
                message = "Podano błędne hasło!"
                context = {
                    "form": form,
                    "message": message
                }
                return render(request, "edit-profile.html", context)
        return render(request, 'edit-profile.html', context={"form": form})


class EditUserPasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditPasswordForm()
        return render(request, 'edit-password.html', context={"form": form})

    def post(self, request):
        form = EditPasswordForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.email, password=form.cleaned_data["old_password"])
            if user is not None:
                user.set_password(form.cleaned_data["new_password1"])
                user.save()
                login(request, user)
                return redirect(reverse('profile'))
            else:
                message = "Błędne hasło!"
                context = {
                    "form": form,
                    "message": message,
                }
                return render(request, "edit-password.html", context)
        return render(request, 'edit-password.html', context={"form": form})