from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Dweet
from .forms import DweetForm

# Create your views here.

@login_required
def dashboard(request):
    # You fill DweetForm with the data that 
    # came in through the POST request
    form = DweetForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            # you need to save the DweetForm(request.POST) 
            # bc if not, it is just raw HTML
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")
          
    #followers = request.user.profile.follows.exclude(user=request.user)

    # Filter or give me every Dweet model WHERE the Dweet.user.profile 
    # is IN every person the logged in User follows.
    followed_dweets = Dweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()
        ).order_by('-created_at')

    context = {
        "dweets": followed_dweets,
        "form": form
    }
    return render(request, "dwitter/dashboard.html", context)


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    context = {"profiles": profiles}
    return render(request, "dwitter/profile_list.html", context)

def profile(request, pk):
    # incase the user does not have a profile, create one
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        # request.POST is raw html
        data = request.POST 
        action = data.get("follow")
        if action=="follow":
            current_user_profile.follows.add(profile)
        elif action=="unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    
    context = { "profile": profile}

    return render(request, "dwitter/profile.html", context)


def register(request):
    if request.method == "POST":
        new_user_form = UserCreationForm(request.POST)
        if new_user_form.is_valid():
            new_user_form.save()
            messages.success(request, 'Account created successfully!')
            return redirect("dwitter:login")

    else:
        new_user_form = UserCreationForm()
    
    context = {'register_form': new_user_form}
    

    return render(request, "account/register.html", context)



   

