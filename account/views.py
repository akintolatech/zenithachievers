from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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


# def register(request):
#     # get referral code instead from the form
#     referral_code = request.GET.get('invitedby', None)  # Get referral code from URL
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             # Set the chosen password in hash
#             new_user.set_password(user_form.cleaned_data['password'])
#             # Save the User object
#             new_user.save()
#             # Create the user profile
#             Profile.objects.create(user=new_user)
#
#             # Assign the referrer if a valid referral code is provided
#             if referral_code:
#                 try:
#                     referrer = get_user_model().objects.get(username=referral_code)
#                     profile.invited_by = referrer
#                     profile.save()
#                 except get_user_model().DoesNotExist:
#                     pass  # Ignore if referrer does not exist
#
#             return render(
#                 request,
#                 'account/register_done.html',
#                 {'new_user': new_user},
#             )
#     else:
#         user_form = UserRegistrationForm()
#     return render(
#         request,
#         'account/register.html',
#         {'user_form': user_form}
#     )



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

    context = {
        "user_profile": user_profile
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