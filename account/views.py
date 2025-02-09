from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from package.models import UserPackage
from .models import Profile

from .forms import (
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm
)

@login_required()
def landing(request):
    return render(
        request,
        'account/onboarding.html',
    )


def register(request):
    referral_code = request.GET.get('invitedby', None)  # Get referral code from URL
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            # Create the user profile
            user_profile = Profile.objects.create(user=new_user)

            # Assign the referrer if a valid referral code is provided
            if referral_code:
                try:
                    referrer = get_user_model().objects.get(username=referral_code)
                    user_profile.invited_by = referrer  # Correct assignment
                    user_profile.save()
                except get_user_model().DoesNotExist:
                    pass  # Ignore if referrer does not exist

            return render(
                request,
                'account/register_done.html',
                {'new_user': new_user},
            )
    else:
        user_form = UserRegistrationForm()

    return render(
        request,
        'account/register.html',
        {
            'user_form': user_form,
            'referral_code': referral_code
        }
    )




@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        },
    )


@login_required()
def dashboard(request):
    user_profile = request.user.profile

    user_package = UserPackage.objects.filter(user=request.user).order_by('-purchased_at').first()
    context = {
        "user_profile": user_profile,
        "user_package": user_package
    }
    return render(
        request,
        'dashboard/index.html',
        context,
    )


@login_required()
def profile(request):

    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(
        request,
        'dashboard/pages/profile/profile.html',
        context
    )


def get_referrals_by_package(user, package_name=None):
    """Helper function to get referrals filtered by package type."""
    referrals = Profile.objects.filter(invited_by=user).select_related('user')

    referral_data = []
    for referral in referrals:
        user_package = UserPackage.objects.filter(user=referral.user).order_by('-purchased_at').first()

        if package_name:
            if not user_package or user_package.package.name.lower() != package_name.lower():
                continue  # Skip if the package does not match

        referral_data.append({
            "name": referral.user.get_full_name() or referral.user.username,
            "phone": referral.phone_number,
            "active_since": referral.user.date_joined.strftime('%Y-%m-%d'),
            "package_plan": user_package.package.name if user_package else "No Package",
            "account_status": referral.account_status,
        })

    return referral_data


@login_required
def all_referrals(request):
    context = {
        "user_profile": request.user.profile,
        "referral_data": get_referrals_by_package(request.user),
    }
    return render(request, 'dashboard/pages/history/afilliates.html', context)


@login_required
def basic_referrals(request):
    context = {
        "user_profile": request.user.profile,
        "referral_data": get_referrals_by_package(request.user, package_name="Basic"),
    }
    return render(request, 'dashboard/pages/history/basicafilliates.html', context)


@login_required
def premium_referrals(request):
    context = {
        "user_profile": request.user.profile,
        "referral_data": get_referrals_by_package(request.user, package_name="Elite"),
    }
    return render(request, 'dashboard/pages/history/premiumafilliates.html', context)


@login_required
def gold_referrals(request):
    context = {
        "user_profile": request.user.profile,
        "referral_data": get_referrals_by_package(request.user, package_name="Executive"),
    }
    return render(request, 'dashboard/pages/history/goldafilliates.html', context)

@login_required()
def dormant_referrals(request):
    user_profile = request.user.profile

    # Get dormant referrals invited by the user
    referrals = Profile.objects.filter(
        invited_by=request.user,
        account_status=Profile.AccountStatus.DORMANT
    ).select_related('user')

    # Get user packages for referrals
    referral_data = []
    for referral in referrals:
        user_package = UserPackage.objects.filter(user=referral.user).order_by('-purchased_at').first()

        referral_data.append({
            "name": referral.user.get_full_name() or referral.user.username,
            "phone": referral.phone_number,
            "active_since": referral.user.date_joined.strftime('%Y-%m-%d'),
            "package_plan": user_package.package.name if user_package else "No Package",
            "account_status": referral.account_status,
        })

    context = {
        "user_profile": user_profile,
        "referral_data": referral_data,
    }

    return render(request, 'dashboard/pages/history/dormantafilliates.html', context)