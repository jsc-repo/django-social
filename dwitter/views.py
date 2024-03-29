from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .models import Profile, Dweet
from .forms import DweetForm

# Create your views here.

def index(request):
    dweets = Dweet.objects.all()
    context = {
        "dweets": dweets
    }
    return render(request, 'dwitter/index.html', context)

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
    profile_user_dweets = profile.user.dweets.all()
    
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
    
    
    # liked = False
    
    context = { "profile": profile}

    return render(request, "dwitter/profile.html", context)


def dweet_detail(request, pk, **kwargs):
    get_dweet = get_object_or_404(Dweet,id=pk)
    liked = False

    if get_dweet.likes.filter(id=request.user.id).exists():
        liked = True


    context = {
        "dweet": get_dweet,
        "liked": liked
    }

    return render(request, "dwitter/dwitter_detailView.html", context)



def dweet_like(request, pk):
    data = request.POST
    dweet_id = data.get("dweet_id")
    profile_id = data.get("profile")
    dweet = get_object_or_404(Dweet, id=dweet_id)

    if dweet.likes.filter(id=request.user.id).exists():
        dweet.likes.remove(request.user)
    else:
        dweet.likes.add(request.user)
    
    return redirect('dwitter:dweet_detail', username=dweet.user.username, pk=dweet_id)

    # path("<str:username>/dweet/<int:pk>", dweet_detail, name="dweet_detail"),


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



   

