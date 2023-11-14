from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm


@login_required
def profile(request):
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)


        if u_form.is_valid() and p_form.is_valid():
            approval_status = u_form.cleaned_data['approval_status']
            profile_picture = p_form.cleaned_data['profile_picture']
            
            if approval_status == 'n':
                u_form.instance.approval_status = 'p'

            if not profile_picture:
                p_form.instance.profile_picture.delete()
                p_form.instance.profile_picture = 'profile_pics/default.jpg'

            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        profile = request.user.profile
        p_form = ProfileUpdateForm(instance=profile)
        p_form.fields['profile_picture'].widget.attrs['value'] = profile.get_profile_picture()
   
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/edit-profile.html', context)