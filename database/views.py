from django.shortcuts import render, redirect, get_object_or_404
from members import forms
from database import models
from django.utils.dateparse import parse_duration
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from database.models import Campaign


def database_home(request):
    campaigns = models.Campaign.objects.all()
    actors = models.Actor.objects.all()
    pcs = models.PC.objects.all()
    parties = models.Party.objects.all()
    producers = models.Producer.objects.all()
    systems = models.System.objects.all()
    publishers = models.Publisher.objects.all()

    featured_campaigns = models.Campaign.objects.filter(featured=True)

    context = {'campaigns': campaigns,
               'actors': actors,
               'pcs': pcs,
               'parties': parties,
               'producers': producers,
               'systems': systems,
               'publishers': publishers,
               'featured_campaigns': featured_campaigns}
    return render(request, 'database/main.html', context)


def database_pages(request, entity):
    if entity == 'campaigns':
        campaigns = models.Campaign.objects.all()
        progress_choices = {}
        for choice in Campaign.progress_choices:
            progress_choices[choice[0].lower().replace(' ', '_')] = choice[0]

        medium_choices = {}
        for choice in Campaign.medium_choices:
            medium_choices[choice[0].lower().replace(' ', '_')] = choice[0]

        type_choices = {}
        for choice in Campaign.type_choices:
            type_choices[choice[0].lower().replace(' ', '_')] = choice[0]

        if request.method == 'POST':
            if "submit_filter" in request.POST:
                if request.POST.get('sort_order') == 'asc':
                    sort_order = request.POST.get('sort_order')
                    campaigns = campaigns.order_by('title')
                elif request.POST.get('sort_order') == 'desc':
                    sort_order = request.POST.get('sort_order')
                    campaigns = campaigns.order_by('-title')
                else:
                    sort_order = request.POST.get('sort_order')
                    campaigns = campaigns.order_by('title')
                if request.POST.get('progress_filter'):
                    progress = request.POST.get('progress_filter')
                    campaigns = campaigns.filter(progress__icontains=progress)
                if request.POST.get('medium_filter'):
                    medium = request.POST.get('medium_filter')
                    campaigns = campaigns.filter(medium__icontains=medium)
                if request.POST.get('type_filter'):
                    t = request.POST.get('type_filter')
                    campaigns = campaigns.filter(type__icontains=t)
        context = {
            "campaigns": campaigns,
            # "progress": progress,
            "progress_choices": progress_choices,
            # "medium": medium,
            "medium_choices": medium_choices,
            # "type": t,
            "type_choices": type_choices,
            # "sort_order": sort_order,
        }
        return render(request, 'database/campaign_database.html', context)

    if entity == 'actors':
        actors = models.Actor.objects.all()
        return render(request, 'database/actor_database.html', {'actors': actors})

    if entity == 'pcs':
        pcs = models.PC.objects.all()
        return render(request, 'database/pc_database.html', {'pcs': pcs})

    if entity == 'parties':
        parties = models.Party.objects.all()
        return render(request, 'database/party_database.html', {'parties': parties})

    if entity == 'producers':
        producers = models.Producer.objects.all()
        return render(request, 'database/producer_database.html', {'producers': producers})

    if entity == 'publishers':
        publishers = models.Publisher.objects.all()
        return render(request, 'database/publisher_database.html', {'publishers': publishers})

    if entity == 'systems':
        systems = models.System.objects.all()
        featured_campaigns = models.Campaign.objects.filter(featured=True)
        return render(request, 'database/system_database.html', {'systems': systems,
                                                                 'featured_campaigns': featured_campaigns})


def model_pages(request, entity, ent_id):
    if entity == "campaigns":
        campaign = get_object_or_404(models.Campaign, id=ent_id)
        episodes = models.Episode.objects.filter(in_campaign=campaign)
        context = {'campaign': campaign, 'episodes': episodes}

        if 'previousEnt' in request.POST:
            return redirect('model_page', entity, ent_id - 1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id + 1)
        if 'followCampaign' in request.POST:
            campaign.campaign_followers.add(request.user.profile)
        if 'unfollowCampaign' in request.POST:
            campaign.campaign_followers.remove(request.user.profile)
        if 'watchlistCampaign' in request.POST:
            campaign.watchlist_profiles.add(request.user.profile)
        if 'watchlistCampaignRemove' in request.POST:
            campaign.watchlist_profiles.remove(request.user.profile)
        return render(request, 'database/model_pages/campaign_page.html', context)
    if entity == "actors":
        actor = get_object_or_404(models.Actor, id=ent_id)
        context = {'actor': actor}

        if 'previousEnt' in request.POST:
            return redirect('model_page', entity, ent_id - 1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id + 1)
        if 'followActor' in request.POST:
            actor.followers.add(request.user.profile)
        if 'unfollowActor' in request.POST:
            actor.followers.remove(request.user.profile)

        return render(request, 'database/model_pages/actor_page.html', context)
    if entity == "pcs":
        pc = get_object_or_404(models.PC, id=ent_id)
        context = {'pc': pc}

        if 'previousEnt' in request.POST:
            return redirect('model_page', entity, ent_id - 1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id + 1)

        return render(request, 'database/model_pages/pc_page.html', context)
    if entity == "producers":
        producer = get_object_or_404(models.Producer, id=ent_id)
        context = {'producer': producer}

        if 'previousEnt' in request.POST:
            return redirect('model_page', entity, ent_id - 1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id + 1)
        if 'followProducer' in request.POST:
            producer.followers.add(request.user.profile)
        if 'unfollowProducer' in request.POST:
            producer.followers.remove(request.user.profile)

        return render(request, 'database/model_pages/producer_page.html', context)
    if entity == "publishers":
        publisher = get_object_or_404(models.Publisher, id=ent_id)
        context = {'publisher': publisher}

        if 'previousEnt' in request.POST:
            return redirect('model_page', entity, ent_id - 1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id + 1)

        return render(request, 'database/model_pages/publisher_page.html', context)
    if entity == "systems":
        system = get_object_or_404(models.System, id=ent_id)
        campaigns = models.Campaign.objects.filter(featured=True)
        featured_campaigns = []
        for campaign in campaigns:
            if system in campaign.system.all():
                featured_campaigns.append(campaign)
        context = {'system': system,
                   'featured_campaigns': featured_campaigns}

        if 'previousEnt' in request.POST:
            return redirect('model_page', entity, ent_id - 1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id + 1)

        return render(request, 'database/model_pages/system_page.html', context)
    if entity == "parties":
        party = get_object_or_404(models.Party, id=ent_id)
        context = {'party': party}

        if 'previousEnt' in request.POST:
            return redirect('model_page', entity, ent_id - 1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id + 1)

        return render(request, 'database/model_pages/party_page.html', context)


@login_required(login_url="/members/login")
def add_new_records(request):
    system_form = forms.AddSystemForm
    publisher_form = forms.AddPublisherForm
    producer_form = forms.AddProducerForm
    party_form = forms.AddPartyForm
    pc_form = forms.AddPCForm
    actor_form = forms.AddActorForm
    campaign_form = forms.AddCampaignForm

    context = {
        'addCampaign_form': campaign_form,
        'addActor_form': actor_form,
        'addPC_form': pc_form,
        'addParty_form': party_form,
        'addProducer_form': producer_form,
        'addPublisher_form': publisher_form,
        'addSystem_form': system_form,
    }

    if request.method == 'POST':
        if 'submitPC' in request.POST:
            if pc_form.is_valid():
                pc_form.save()
                # Render success message
                messages.success(request, "PC Successfully Added")
                return render(request, 'user_forms/add_records/add_new_records.html', context)
        if 'submitActor' in request.POST:
            if actor_form.is_valid():
                actor_form.save()
            # Render success message
            messages.success(request, "Actor Successfully Added")
            return render(request, 'user_forms/add_records/add_new_records.html', context)
        if 'submitParty' in request.POST:
            if party_form.is_valid():
                party_form.save()
            # Render success message
            messages.success(request, "Party Successfully Added")
            return render(request, 'user_forms/add_records/add_new_records.html', context)
        if 'submitProducer' in request.POST:
            if producer_form.is_valid():
                producer_form.save()
            # Render success message
            messages.success(request, "Producer Successfully Added")
            return render(request, 'user_forms/add_records/add_new_records.html', context)
        if 'submitPublisher' in request.POST:
            if publisher_form.is_valid():
                publisher_form.save()
            # Render success message
            messages.success(request, "Publisher Successfully Added")
            return render(request, 'user_forms/add_records/add_new_records.html', context)
        if 'submitCampaign' in request.POST:
            if campaign_form.is_valid():
                campaign_form.save()
            # Render success message
            messages.success(request, "Campaign Successfully Added")
            return render(request, 'user_forms/add_records/add_new_records.html', context)
        if 'submitSystem' in request.POST:
            if system_form.is_valid():
                system_form.save()
            # Render success message
            messages.success(request, "System Successfully Added")
            return render(request, 'user_forms/add_records/add_new_records.html', context)
    return render(request, 'user_forms/add_records/add_new_records.html', context)


@login_required(login_url="/members/login")
def add_new_model(request, entity):
    if entity == 'campaign':
        campaign_form = forms.AddCampaignForm(request.POST)
        if request.method == 'POST':
            if 'submitCampaign' in request.POST:
                if campaign_form.is_valid():
                    campaign_form.save()
                # Render success message
                messages.success(request, "Campaign Successfully Added")
                return redirect('add_model', 'campaign')
        return render(request, 'user_forms/add_records/add_campaign.html', {'addCampaign_form': campaign_form})

    if entity == 'actor':
        actor_form = forms.AddActorForm(request.POST)
        if request.method == 'POST':
            if 'submitActor' in request.POST:
                if actor_form.is_valid():
                    actor_form.save()
                # Render success message
                messages.success(request, "Actor Successfully Added")
        return render(request, 'user_forms/add_records/add_actor.html', {'addActor_form': actor_form})

    if entity == 'pc':
        pc_form = forms.AddPCForm(request.POST)
        if request.method == 'POST':
            if 'submitPC' in request.POST:
                if pc_form.is_valid():
                    pc_form.save()
                # Render success message
                messages.success(request, "PC Successfully Added")
        return render(request, 'user_forms/add_records/add_pc.html', {'addPC_form': pc_form})

    if entity == 'party':
        party_form = forms.AddPartyForm(request.POST)
        if request.method == 'POST':
            if 'submitParty' in request.POST:
                if party_form.is_valid():
                    party_form.save()
                # Render success message
                messages.success(request, "Party Successfully Added")
                return redirect('add_model', 'party')
        return render(request, 'user_forms/add_records/add_party.html', {'addParty_form': party_form})

    if entity == 'producer':
        producer_form = forms.AddProducerForm(request.POST)
        if request.method == 'POST':
            if 'submitProducer' in request.POST:
                if producer_form.is_valid():
                    producer_form.save()
                # Render success message
                messages.success(request, "Producer Successfully Added")
                return redirect('add_model', 'producer')
        return render(request, 'user_forms/add_records/add_producer.html', {'addProducer_form': producer_form})

    if entity == 'publisher':
        publisher_form = forms.AddPublisherForm(request.POST)
        if request.method == 'POST':
            if 'submitPublisher' in request.POST:
                if publisher_form.is_valid():
                    publisher_form.save()
                # Render success message
                messages.success(request, "Publisher Successfully Added")
                return redirect('add_model', 'publisher')
        return render(request, 'user_forms/add_records/add_publisher.html', {'addPublisher_form': publisher_form})

    if entity == 'system':
        system_form = forms.AddSystemForm(request.POST)
        if 'submitSystem' in request.POST:
            if system_form.is_valid():
                system_form.save()
            # Render success message
            messages.success(request, "System Successfully Added")
            return redirect('add_model', 'system')
        return render(request, 'user_forms/add_records/add_system.html', {'addSystem_form': system_form})


@login_required(login_url="/members/login")
def edit_model(request, entity, ent_id):
    if entity == 'campaign':
        campaign = get_object_or_404(models.Campaign, id=ent_id)
        form = forms.CampaignEditForm(request.POST or None, instance=campaign)
        if request.method == 'POST':
            if 'editCampaign' in request.POST:
                if form.is_valid():
                    form.save()
                    # Notify Followers
                    # for user in campaign.followers.all():
                    #     models.Notification.objects.create(
                    #         receiver=user,
                    #         subject=campaign.title + "'s page has been updated",
                    #         message="A new update has been made to " + campaign.title + "'s page. See below for details"
                    #     )
                    # Render success message
                    messages.success(request, "Campaign Successfully Updated")
                    return redirect("model_page", entity='campaigns', ent_id=ent_id)
                else:
                    # Render failure message
                    messages.error(request, "Failed to Update Campaign")
                    return redirect("model_page", entity='campaigns', ent_id=ent_id)
        context = {
            'campaign': campaign,
            'form': form
        }
        return render(request, 'user_forms/edit_records/edit_campaign.html', context)

    if entity == 'actor':
        actor = get_object_or_404(models.Actor, id=ent_id)
        form = forms.ActorEditForm(request.POST or None, instance=actor)

        if request.method == 'POST':
            if 'editActor' in request.POST:
                if form.is_valid():
                    form.save()
                    # Notify Followers
                    for user in actor.followers.all():
                        models.Notification.objects.create(
                            receiver=user,
                            subject=actor.name + "'s page has been updated",
                            message="A new update has been made to " + actor.name + "'s page. See below for details"
                        )
                    # Render success message
                    messages.success(request, "Actor Successfully Updated")
                    return redirect("model_page", entity='actors', ent_id=ent_id)
                else:
                    # Render failure message
                    messages.error(request, "Failed to Update Campaign")
                    return redirect("model_page", entity='actors', ent_id=ent_id)

        context = {
            'actor': actor,
            'form': form
        }
        return render(request, 'user_forms/edit_records/edit_actor.html', context)

    if entity == 'pc':
        pc = get_object_or_404(models.PC, id=ent_id)
        form = forms.PCEditForm(request.POST or None, instance=pc)
        if request.method == 'POST':
            if 'editPC' in request.POST:
                if form.is_valid():
                    form.save()
                    # Render success message
                    messages.success(request, "PC Successfully Updated")
                    return redirect("model_page", entity='pcs', ent_id=ent_id)
                else:
                    # Render failure message
                    messages.error(request, "Failed to Update PC")
                    return redirect("model_page", entity='pcs', ent_id=ent_id)
        context = {
            'pc': pc,
            'form': form
        }
        return render(request, 'user_forms/edit_records/edit_pc.html', context)

    if entity == 'party':
        party = get_object_or_404(models.Party, id=ent_id)
        form = forms.PartyEditForm(request.POST or None, instance=party)
        if request.method == 'POST':
            if 'editParty' in request.POST:
                if form.is_valid():
                    form.save()
                    # Render success message
                    messages.success(request, "Party Successfully Updated")
                    return redirect("model_page", entity='parties', ent_id=ent_id)
                else:
                    # Render failure message
                    messages.error(request, "Failed to Update Party")
                    return redirect("model_page", entity='parties', ent_id=ent_id)
        context = {
            'party': party,
            'form': form
        }
        return render(request, 'user_forms/edit_records/edit_party.html', context)

    if entity == 'producer':
        producer = get_object_or_404(models.Producer, id=ent_id)
        form = forms.ProducerEditForm(request.POST or None, instance=producer)
        if request.method == 'POST':
            if 'editProducer' in request.POST:
                if form.is_valid():
                    form.save()
                    # Notify Followers
                    # for user in producer.followers.all():
                    #     models.Notification.objects.create(
                    #         receiver=user,
                    #         subject=producer.name + "'s page has been updated",
                    #         message="A new update has been made to " + producer.name + "'s page. See below for details"
                    #     )
                    # Render success message
                    messages.success(request, "Producer Successfully Updated")
                    return redirect("model_page", entity='producers', ent_id=ent_id)
                else:
                    # Render failure message
                    messages.error(request, "Failed to Update Producer")
                    return redirect("model_page", entity='producers', ent_id=ent_id)
        context = {
            'producer': producer,
            'form': form
        }
        return render(request, 'user_forms/edit_records/edit_producer.html', context)

    if entity == 'publisher':
        publisher = get_object_or_404(models.Publisher, id=ent_id)
        form = forms.PublisherEditForm(request.POST or None, instance=publisher)
        if request.method == 'POST':
            if 'editPublisher' in request.POST:
                if form.is_valid():
                    form.save()
                    # Render success message
                    messages.success(request, "Publisher Successfully Updated")
                    return redirect("model_page", entity='publishers', ent_id=ent_id)
                else:
                    # Render failure message
                    messages.error(request, "Failed to Update Publisher")
                    return redirect("model_page", entity='publishers', ent_id=ent_id)
        context = {
            'publisher': publisher,
            'form': form
        }
        return render(request, 'user_forms/edit_records/edit_publisher.html', context)

    if entity == 'system':
        system = get_object_or_404(models.System, id=ent_id)
        form = forms.SystemEditForm(request.POST or None, instance=system)
        if request.method == 'POST':
            if 'editSystem' in request.POST:
                if form.is_valid():
                    form.save()
                    # Render success message
                    messages.success(request, "System Successfully Updated")
                    return redirect("model_page", entity='systems', ent_id=ent_id)
                else:
                    # Render failure message
                    messages.error(request, "Failed to Update System")
                    return redirect("model_page", entity='systems', ent_id=ent_id)
        context = {
            'system': system,
            'form': form
        }
        return render(request, 'user_forms/edit_records/edit_system.html', context)


@login_required(login_url="/members/login")
def add_new_episode(request, campaign_id):
    form = forms.AddEpisodeForm(request.POST)
    campaign = get_object_or_404(models.Campaign, id=campaign_id)

    if request.method == 'POST':
        if 'submitEpisode' in request.POST:
            episode = form.save(commit=False)
            episode.in_campaign = campaign
            episode.save()
            return redirect('model_page', entity='campaigns', ent_id=campaign_id)
    return render(request, 'user_forms/add_records/add_episode.html', {'form': form})
