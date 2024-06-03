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
    notifications = models.CRUD_Update_Notification.objects.filter(receiver=profile)
    unread_notifications = notifications.filter(read_status=False)

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
               'notifications': notifications,
               'unread_notifications': unread_notifications,
               }

    return render(request, 'members/user_home.html', context)


@login_required(login_url="/members/login")
def inbox(request, user_id):
    user = get_object_or_404(models.Profile, id=user_id)
    notifications = models.CRUD_Update_Notification.objects.filter(receiver=user)
    unread_notifications = notifications.filter(read_status=False).order_by('-datetime')
    read_notifications = notifications.filter(read_status=True).order_by('-datetime')

    context = {'user': user, 'notifications': notifications, 'unread_notifications': unread_notifications,
               'read_notifications': read_notifications}
    return render(request, 'members/notifications/inbox.html', context)


def CRUD_m2m_key_handler(content_type, instance, cfs):
    changes = {}
    key_list = []
    if content_type == 'Campaign':
        for key in cfs:
            if key == 'gm':
                actor_list = []
                for actor_id in cfs[key]:
                    actor = get_object_or_404(models.Actor, id=actor_id)
                    actor_list.append(actor.name)
                changes.update({"gm": actor_list})
                key_list.append("GMs")
                actor_list_formatted = []
                for actor in actor_list:
                    actor_list_formatted.append(f"{actor}<br>")
            elif key == 'system':
                system_list = []
                for system_id in cfs[key]:
                    system = get_object_or_404(models.System, id=system_id)
                    system_list.append(system)
                changes.update({"system": system_list})
                key_list.append("Systems")
            elif key == 'produced_by':
                producer_list = []
                for producer_id in cfs[key]:
                    producer = get_object_or_404(models.Producer, id=producer_id)
                    producer_list.append(producer)
                changes.update({"producer": producer_list})
                key_list.append("Producers")
            elif key == 'party':
                party_list = []
                for party_id in cfs[key]:
                    party = get_object_or_404(models.Party, id=party_id)
                    party_list.append(party)
                changes.update({"party": party_list})
                key_list.append("Parties")
            elif key == 'guest_pcs':
                guest_list = []
                for guest_id in cfs[key]:
                    guest = get_object_or_404(models.PC, id=guest_id)
                    guest_list.append(guest)
                changes.update({"guest": guest_list})
                key_list.append("Guest PCs")


def CRUD_event_notification(event_type, c_t, crud_event):
    # Create
    if event_type == 1:
        pass
    # Update
    elif event_type == 2:
        pass
        # for key in dict.keys():
        #     print(f"{key.title()} changed from \"{crud_event[key][0]}\" to \"{crud_event[key][1]}\"")
    # M2M Add
    elif event_type == 6:
        content_type = str(c_t).replace('Database | ', '')
        instance = get_object_or_404(getattr(models, content_type), id=crud_event.object_id)
        instance_str = str(instance)
        fields_w_additions = getattr(crud_event, 'changed_fields')

        if content_type is "Campaign" or "Actor" or "Producer":
            if "follower" in fields_w_additions:
                pass
            else:
                for user in instance.followers.all():
                    models.CRUD_Update_Notification.objects.create(
                        receiver=user,
                        subject=instance_str + "'s page has been updated",
                        id=getattr(crud_event, 'id'),
                        event_type=getattr(crud_event, 'event_type'),
                        instance_name_str=getattr(crud_event, 'object_repr'),
                        instance_basic_fields_str=getattr(crud_event, 'object_json_repr'),
                        field_with_addition=getattr(crud_event, 'changed_fields'),
                        content_type_id=getattr(crud_event, 'content_type_id'),
                        updated_instance_id=getattr(crud_event, 'object_id'),
                        user_id=getattr(crud_event, 'user_id'),
                        datetime=getattr(crud_event, 'datetime'),
                    )
                if "gm" in fields_w_additions:
                    changed_ids = str(fields_w_additions)
                    changed_field_type = "gm"
                    changed_field_model = models.Actor
                    new_punctuations = string.punctuation.replace(",", '')
                    for punctuation in new_punctuations:
                        changed_ids = changed_ids.replace(punctuation, '').replace(changed_field_type, '').replace(" ",
                                                                                                                   "")
                    changed_id_list = changed_ids.split(",")
                    changed_instances = []
                    for instance_id in changed_id_list:
                        actor = get_object_or_404(changed_field_model, id=instance_id)
                        changed_instances.append(actor)
                    print(changed_instances)
                    for actor in changed_instances:
                        for user in actor.followers.all():
                            models.CRUD_Update_Notification.objects.create(
                                receiver=user,
                                subject=str(actor.name) + "'s page has been updated",
                                event_type=601,
                                instance_name_str=str(actor),
                                instance_basic_fields_str="database.actor",
                                field_with_addition="campaign " + str(getattr(crud_event, 'object_id')),
                                content_type_id=getattr(crud_event, 'object_id'),
                                updated_instance_id=actor.id,
                                user_id=getattr(crud_event, 'user_id'),
                                datetime=getattr(crud_event, 'datetime'),
                            )


    # M2M Remove
    elif event_type == 8:
        pass


def read_crud_update(request, notification_id):
    crud_event = get_object_or_404(models.CRUD_Update_Notification, id=notification_id)
    if not crud_event.read_status:
        crud_event.read_status = True
        crud_event.save()
    if "database.campaign" in crud_event.instance_basic_fields_str:
        instance_type = "Campaign"
        instance_type_model = "campaigns"
    if "database.actor" in crud_event.instance_basic_fields_str:
        instance_type = "Actor"
        instance_type_model = "actors"
    if "database.pc" in crud_event.instance_basic_fields_str:
        instance_type = "PC"
        instance_type_model = "pcs"
    if "database.producer" in crud_event.instance_basic_fields_str:
        instance_type = "Producer"
        instance_type_model = "producers"
    if "database.party" in crud_event.instance_basic_fields_str:
        instance_type = "Party"
        instance_type_model = "parties"
    if "database.publisher" in crud_event.instance_basic_fields_str:
        instance_type = "Publisher"
        instance_type_model = "publishers"
    if "database.system" in crud_event.instance_basic_fields_str:
        instance_type = "System"
        instance_type_model = "systems"
    if 'campaign' in crud_event.field_with_addition:
        changed_field_name = "Campaign(s)"
        changed_field_model = models.Campaign
        changed_field_type = "campaign"
        changed_field_type_model = "campaigns"
    elif 'party' in crud_event.field_with_addition:
        changed_field_name = "Party/Parties"
        changed_field_model = models.Party
        changed_field_type = "party"
        changed_field_type_model = "parties"
    elif 'guest_pcs' in crud_event.field_with_addition:
        changed_field_name = "Guest PC(s)"
        changed_field_model = models.PC
        changed_field_type = "guest_pcs"
        changed_field_type_model = "pcs"
    elif 'gm' in crud_event.field_with_addition:
        changed_field_name = "GM(s)"
        changed_field_model = models.Actor
        changed_field_type = "gm"
        changed_field_type_model = "actors"
    elif 'system' in crud_event.field_with_addition:
        changed_field_name = "System(s)"
        changed_field_model = models.System
        changed_field_type = "system"
        changed_field_type_model = "systems"
    elif 'produced_by' in crud_event.field_with_addition:
        changed_field_name = "Producer(s)"
        changed_field_model = models.Producer
        changed_field_type = "produced_by"
        changed_field_type_model = "producers"
    changed_ids = str(crud_event.field_with_addition)
    new_punctuations = string.punctuation.replace(",", '')
    for punctuation in new_punctuations:
        changed_ids = changed_ids.replace(punctuation, '')
    changed_ids = changed_ids.replace(changed_field_type, '').replace(" ", "")
    changed_id_list = changed_ids.split(",")
    changed_instances = []
    for instance_id in changed_id_list:
        instance = get_object_or_404(changed_field_model, id=instance_id)
        changed_instances.append(instance)

    context = {
        'crud_event': crud_event,
        'instance_type': instance_type,
        'instance_type_model': instance_type_model,
        'changed_field_type': changed_field_type,
        'changed_field_name': changed_field_name,
        'changed_id_list': changed_id_list,
        'changed_instances': changed_instances,
        'changed_field_type_model': changed_field_type_model,
    }
    return render(request, "members/notifications/CRUDEvent.html", context)
