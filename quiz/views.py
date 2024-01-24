from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import Profile
from .models import Quiz,Category

# Create your views here.
@login_required(login_url='login')
def all_quiz_view(request):
    user_object=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_object)

    quizzes=Quiz.objects.order_by('-created_at')
    categories=Category.objects.all()

    context={"user_profile":user_profile,"quizzes":quizzes,"categories":categories}
    return render(request, 'all_quiz.html', context)


@login_required(login_url='login')
def search_view(request,category):
    user_object=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_object)

    if category!="":
        quizzes=Quiz.objects.filter(category__name=category)
    else:
        quizzes=Quiz.objects.order_by('-created_at')
        
    categories=Category.objects.all()

    context={}
    context={"user_profile":user_profile,"quizzes":quizzes,"categories":categories}
    return render(request,'all_quiz.html',context)