from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from account.models import Profile
from quiz.models import UserRank
from django.contrib.auth.decorators import login_required

def home(request):

    leaderboard_user=UserRank.objects.order_by('rank')[:4]
    
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile}
        
    else:
        context={"leaderboard_user":leaderboard_user}
        
    return render(request, 'welcome.html', context)

@login_required(login_url="login")
def leaderboard_view(request):

    leaderboard_user=UserRank.objects.order_by('rank')

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    context={"leaderboard_user":leaderboard_user,"user_profile":user_profile}
    return render(request,"leaderboard.html",context)
