from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from .forms import UserRegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from .tokens import email_account_activation
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse


def index(request):
    return render(request, "reset/index.html")


def signup(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Activate your account"
            message = render_to_string("reset/activate.html", {
                "user": form.cleaned_data['username'],
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": email_account_activation.make_token(user),

            })
            to_mail = form.cleaned_data.get("email")
            mail = EmailMessage(
                mail_subject, message, to=[to_mail]
            )
            mail.send()

            messages.success(request, "Account created.")
            return redirect("/")
        else:
            messages.error(request, "Account failed try again")

    return render(request, "reset/signup.html", {"form":form})


# Create your views here.

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_account_activation.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "reset/activation_successful.html")

        # messages.success(request, "Your account has been successfully activated")
        # return redirect(reverse("login"))
    else:
        return render(request, "reset/activation_unsuccessful.html")
        # messages.error(request, "Activation link is invalid or expired")
        # return redirect("index")

#
# class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         return redirect("reset:home")