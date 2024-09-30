from django.shortcuts import render, redirect
from .forms import UserUpdateForm, ProfileUpdateForm  # Assuming these forms are correctly defined
from django.contrib.auth.decorators import login_required
from .models  import UserProfile

@login_required
def profile(request):
    return render(request, 'user/profile.html', {'user': request.user})

@login_required
def profile_update(request):

    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)
    
    user_profile = request.user.userprofile

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/profile_update.html', context)