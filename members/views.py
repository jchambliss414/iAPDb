from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from database import models
from members.forms import RegisterUserForm
import string


@login_required(login_url="/members/login")
def members_list(request):
    return render(request, 'members_list.html')


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=[password])
            messages.success(request, "Registration Successful. Welcome!")
            return redirect('login')
    else:
        form = RegisterUserForm()
    return render(request, 'members/authenticate/register.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request, "Login Error")
            return redirect('login')
            pass

    else:
        return render(request, 'members/authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "Successfully Logout Out")
    return redirect('/')


@login_required(login_url="/members/login")
def user_homepage(request, user_id):
    profile = get_object_or_404(models.Profile, user=user_id)
    user = profile.user

    watchlist = profile.campaigns_to_watch.all()
    watchinglist = profile.campaigns_watching.all()
    have_watchedlist = profile.campaigns_watched.all()

    following_campaigns = profile.campaigns_following.all()
    following_actors = profile.actors_following.all()
    following_producers = profile.producers_following.all()

    if request.method == 'POST':
        if 'WatchlistToWatching' in request.POST:
            campaign_id = request.POST.get('WatchlistToWatching')
            campaign = get_object_or_404(models.Campaign, id=campaign_id)
            profile.campaigns_to_watch.remove(campaign)
            profile.campaigns_watching.add(campaign)
            if campaign not in profile.campaigns_following.all():
                profile.campaigns_following.add(campaign)
        if 'RemoveWatchlist' in request.POST:
            campaign_id = request.POST.get('RemoveWatchlist')
            campaign = get_object_or_404(models.Campaign, id=campaign_id)
            profile.campaigns_to_watch.remove(campaign)
        if 'WatchingToWatched' in request.POST:
            campaign_id = request.POST.get('WatchingToWatched')
            campaign = get_object_or_404(models.Campaign, id=campaign_id)
            profile.campaigns_watching.remove(campaign)
            profile.campaigns_watched.add(campaign)
        if 'RemoveWatching' in request.POST:
            campaign_id = request.POST.get('RemoveWatching')
            campaign = get_object_or_404(models.Campaign, id=campaign_id)
            profile.campaigns_watching.remove(campaign)
        if 'RemoveWatched' in request.POST:
            campaign_id = request.POST.get('RemoveWatched')
            campaign = get_object_or_404(models.Campaign, id=campaign_id)
            profile.campaigns_watched.remove(campaign)

        if 'UnfollowCampaign' in request.POST:
            campaign_id = request.POST.get('UnfollowCampaign')
            campaign = get_object_or_404(models.Campaign, id=campaign_id)
            profile.campaigns_following.remove(campaign)
        if 'UnfollowActor' in request.POST:
            actor_id = request.POST.get('UnfollowActor')
            actor = get_object_or_404(models.Actor, id=actor_id)
            profile.actors_following.remove(actor)
        if 'UnfollowProducer' in request.POST:
            producer_id = request.POST.get('UnfollowProducer')
            producer = get_object_or_404(models.Producer, id=producer_id)
            profile.producers_following.remove(producer)

    context = {'user': user,
               'profile': profile,
               'following_campaigns': following_campaigns,
               'following_producers': following_producers,
               'following_actors': following_actors,
               'have_watchedlist': have_watchedlist,
               'watchinglist': watchinglist,
               'watchlist': watchlist,
               }

    return render(request, 'members/user_home.html', context)
