from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST,
#                                    request.FILES,
#                                    instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('user:profile')

#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {
#         'u_form': u_form,
#         'p_form': p_form
#     }

#     return render(request, 'users/profile.html', context)

# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)


#         if u_form.is_valid() and p_form.is_valid():
#             approval_status = u_form.cleaned_data['approval_status']
#             profile_picture = p_form.cleaned_data['profile_picture']
            
            
#             u_form.save()
#             p_form.save()
#             messages.success(request, 'Your profile has been updated!')
#             return redirect('users:profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         profile = request.user.profile
#         p_form = ProfileUpdateForm(instance=profile)
#         p_form.fields['profile_picture'].widget.attrs['value'] = profile.get_profile_picture()
   
#     context = {
#         'u_form': u_form,
#         'p_form': p_form
#     }

#     return render(request, 'users/edit-profile.html', context)

@login_required
def profile(request):
    try:
        # Attempt to retrieve the user's profile
        profile = request.user.profile
    except Profile.DoesNotExist:
        # If the profile does not exist, redirect to the edit profile page
        return redirect('user:edit_profile')

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user:profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'user/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            profile_picture = p_form.cleaned_data['image']

            if not profile_picture:
                p_form.instance.profile_picture.delete()
                p_form.instance.profile_picture = 'profile_pics/default.jpg'

            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('user:profile')
        
        else:
            messages.error(request, 'There was an error updating your profile. Please check the form.')

    else:
        u_form = UserUpdateForm(instance=request.user)
        profile = request.user.profile
        p_form = ProfileUpdateForm(instance=profile)
   
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'user/edit_profile.html', context)