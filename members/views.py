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

    unread_notifications = models.Notification.objects.filter(receiver=profile).filter(read_status=False).order_by('-timestamp')

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
               'unread_notifications': unread_notifications,
               }

    return render(request, 'members/user_home.html', context)


@login_required(login_url="/members/login")
def inbox(request, user_id):
    user = get_object_or_404(models.Profile, id=user_id)
    notifications = models.Notification.objects.filter(receiver=user)
    unread_notifications = notifications.filter(read_status=False).order_by('-timestamp')
    read_notifications = notifications.filter(read_status=True).order_by('-timestamp')
    context = {
        "user": user,
        "notifications": notifications,
        "unread_notifications": unread_notifications,
        "read_notifications": read_notifications,
    }
    return render(request, "members/notifications/inbox.html", context)


@login_required(login_url="/members/login")
def read_notification(request, notification_id):
    notification = get_object_or_404(models.Notification, id=notification_id)
    if notification.read_status is False:
        notification.read_status = True
        notification.save()

    if "CRUD_event" in notification.notification_type:
        parent_obj_type = notification.updated_obj_type
        parent_obj_id = notification.updated_obj_id
        added_obj_type = notification.added_instance_type
        added_obj_id = notification.added_instance_id
        parent_obj = get_object_or_404(getattr(models, parent_obj_type), id=parent_obj_id)
        added_obj = get_object_or_404(getattr(models, added_obj_type), id=added_obj_id)

        if parent_obj_type == 'Party':
            parent_o_t_for_link = 'parties'
        else:
            parent_o_t_for_link = str(parent_obj_type.lower()) + 's'
        if added_obj_type == 'Party':
            added_o_t_for_link = 'parties'
        else:
            added_o_t_for_link = str(added_obj_type.lower()) + 's'

        context = {
            "notification": notification,
            "parent_obj": parent_obj,
            "parent_obj_type": parent_obj_type,
            "parent_o_t_for_link": parent_o_t_for_link,
            "added_obj": added_obj,
            "added_obj_type": added_obj_type,
            "added_o_t_for_link": added_o_t_for_link,
        }
        return render(request, "members/notifications/crud_notification.html", context)
    else:
        pass


def crud_notification(crud_event, c_t):
    if crud_event.event_type == 6:
        if "followers" in crud_event.changed_fields:
            pass
        else:
            parent_instance_id = crud_event.object_id
            parent_c_t = str(c_t).replace("Database | ", "")
            parent_instance = get_object_or_404(getattr(models, parent_c_t), id=parent_instance_id)
            changed_field = changed_field_splitter(crud_event.changed_fields)["field_name"]

            # make a list of ids for the models being added to the parent obj
            instance_ids = []
            for i in changed_field_splitter(crud_event.changed_fields)["instance_ids"]:
                instance_ids.append(i)

            # collect the instances of the models being added
            added_instances = []
            for i_id in instance_ids:
                instance = get_object_or_404(changed_field_splitter(crud_event.changed_fields)["changed_model_type"], id=i_id)
                added_instances.append(instance)

            # for each instance, notify its followers if it has any
            # first check to see if the added model is a "guest pc", notify the actor's followers instead
            if "guest" in changed_field:
                actors = []
                for pc in added_instances:
                    for a in pc.played_by.all():
                        actors.append(a)
                for actor in actors:
                    print(actor)
                for actor in actors:
                    if actor.followers.all():
                        for follower in actor.followers.all():
                            models.Notification.objects.create(
                                notification_type='CRUD_event',
                                receiver=follower,
                                subject=str(actor.name) + " listed as a Guest on '" + str(parent_instance.title) + "'",
                                updated_obj_type=parent_c_t,
                                updated_obj_id=parent_instance_id,
                                added_instance_type='PC',
                                added_instance_id=instance.id
                            )
            else:
                for instance in added_instances:
                    if instance.followers.all():
                        for follower in instance.followers.all():
                            if "gm" in changed_field:
                                models.Notification.objects.create(
                                    notification_type='CRUD_event',
                                    receiver=follower,
                                    subject=str(instance) + " added as GM to new Campaign",
                                    updated_obj_type=parent_c_t,
                                    updated_obj_id=parent_instance_id,
                                    added_instance_type=changed_field_splitter(crud_event.changed_fields)["c_f_model_name"],
                                    added_instance_id=instance.id
                                )
                            else:
                                models.Notification.objects.create(
                                    notification_type='CRUD_event',
                                    receiver=follower,
                                    subject="There's been an update to " +
                                            str(changed_field_splitter(crud_event.changed_fields)["c_f_model_name"]) +
                                            " '" + str(instance) + "'",
                                    updated_obj_type=parent_c_t,
                                    updated_obj_id=parent_instance_id,
                                    added_instance_type=changed_field_splitter(crud_event.changed_fields)["c_f_model_name"],
                                    added_instance_id=instance.id
                                )

    if crud_event.event_type == 1:
        type = ContentType.objects.get_for_model(models.Episode)
        if c_t == type:
            print("CRUD EVENT EPISODE CREATE DETECTED")
            episode = get_object_or_404(models.Episode, id=crud_event.object_id)
            campaign = episode.in_campaign
            print(episode, campaign)
            if campaign.followers.all():
                print("followers for" + str(campaign) + "detected")
                for follower in campaign.followers.all():
                    models.Notification.objects.create(
                        notification_type='CRUD_event',
                        receiver=follower,
                        subject=str(campaign.title) + " just added a new episode",
                        updated_obj_type='Campaign',
                        updated_obj_id=campaign.id,
                        added_instance_type='Episode',
                        added_instance_id=episode.id
                    )
                    print("notification created")
        else:
            pass


def changed_field_splitter(changed_fields):
    new_punctuation = string.punctuation.replace("_", '')
    c_f = changed_fields
    for p in new_punctuation:
        c_f = c_f.replace(p, '')
    for d in string.digits:
        c_f = c_f.replace(d, '')

    if "produced_by" in changed_fields:
        c_f = 'produced_by'
        c_f_model_type = models.Producer
        c_f_model_name = 'Producer'
    if "gm" in changed_fields:
        c_f = 'gm'
        c_f_model_type = models.Actor
        c_f_model_name = 'Actor'
    if "guest_pcs" in changed_fields:
        c_f = 'guest_pcs'
        c_f_model_type = models.PC
        c_f_model_name = 'PC'
    if "characters" in changed_fields:
        c_f = 'characters'
        c_f_model_type = models.PC
        c_f_model_name = 'PC'
    if "gm_campaigns" in changed_fields:
        c_f = 'gm_campaigns'
        c_f_model_type = models.Campaign
        c_f_model_name = 'Campaign'
    if "campaigns" in changed_fields:
        c_f = 'campaigns'
        c_f_model_type = models.Campaign
        c_f_model_name = 'Campaign'

    c_f_ids = changed_fields.replace(c_f, '')
    c_f_ids = c_f_ids.replace('"', '').replace(":", '').replace('{', '').replace('[', '').replace('}', '').replace(']', '')
    c_f_ids = c_f_ids.split(",")


    return {
        "field_name": c_f,
        "changed_model_type": c_f_model_type,
        "instance_ids": c_f_ids,
        "c_f_model_name": c_f_model_name,
    }
