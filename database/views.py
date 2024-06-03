from django.shortcuts import render, redirect, get_object_or_404
from members import forms
from database import models
from django.utils.dateparse import parse_duration
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
        return render(request, 'database/campaign_database.html', {'campaigns': campaigns})

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
    context = {
        'addCampaign_form': forms.AddCampaignForm,
        'addActor_form': forms.AddActorForm,
        'addPC_form': forms.AddPCForm,
        'addParty_form': forms.AddPartyForm,
        'addProducer_form': forms.AddProducerForm,
        'addPublisher_form': forms.AddPublisherForm,
        'addSystem_form': forms.AddSystemForm,
    }

    if request.method == 'POST':
        if 'submitPC' in request.POST:
            submit_record(request, 'pc')
            # Render success message
            messages.success(request, "PC Successfully Added")
            return render(request, 'user_forms/add_records/add_new_records.html', context)
        if 'submitActor' in request.POST:
            submit_record(request, 'actor')
            # Render success message
            messages.success(request, "Actor Successfully Added")
            return render(request, 'user_forms/add_records/add_new_records.html', context)
        if 'submitParty' in request.POST:
            submit_record(request, 'party')
            # Render success message
            messages.success(request, "Party Successfully Added")
            return render(request, 'user_forms/add_records/add_new_records.html', context)
        if 'submitProducer' in request.POST:
            submit_record(request, 'producer')
            # Render success message
            messages.success(request, "Producer Successfully Added")
            return render(request, 'user_forms/add_records/add_new_records.html', context)
        if 'submitPublisher' in request.POST:
            submit_record(request, 'publisher')
            # Render success message
            messages.success(request, "Publisher Successfully Added")
            return render(request, 'user_forms/add_records/add_new_records.html', context)
        if 'submitCampaign' in request.POST:
            submit_record(request, 'campaign')
            # Render success message
            messages.success(request, "Campaign Successfully Added")
            return render(request, 'user_forms/add_records/add_new_records.html', context)
        if 'submitSystem' in request.POST:
            submit_record(request, 'system')
            # Render success message
            messages.success(request, "System Successfully Added")
            return render(request, 'user_forms/add_records/add_new_records.html', context)
    return render(request, 'user_forms/add_records/add_new_records.html', context)


@login_required(login_url="/members/login")
def add_new_model(request, entity):
    if entity == 'campaign':
        addCampaign_form = forms.AddCampaignForm(request.POST)
        if request.method == 'POST':
            if 'submitCampaign' in request.POST:
                # submit_record(request, 'campaign')
                addCampaign_form.save()
                if addCampaign_form.is_valid():
                    # Render success message
                    messages.success(request, "Campaign Successfully Added")
                return redirect('add_model', 'campaign')
        return render(request, 'user_forms/add_records/add_campaign.html', {'addCampaign_form': addCampaign_form})

    if entity == 'actor':
        addActor_form = forms.AddActorForm(request.POST)
        if request.method == 'POST':
            if 'submitActor' in request.POST:
                if addActor_form.is_valid():
                    submit_record(request, 'actor')
                    # Render success message
                    messages.success(request, "Actor Successfully Added")
                    return redirect('add_model', 'actor')
                else:
                    # Render fail message
                    messages.error(request, "Actor Failed to Add")
                    return redirect('add_model', 'actor')
        return render(request, 'user_forms/add_records/add_actor.html', {'addActor_form': addActor_form})

    if entity == 'pc':
        addPC_form = forms.AddPCForm(request.POST)
        if request.method == 'POST':
            if 'submitPC' in request.POST:
                submit_record(request, 'pc')
                # Render success message
                messages.success(request, "PC Successfully Added")
                return redirect('add_model', 'pc')
        return render(request, 'user_forms/add_records/add_pc.html', {'addPC_form': addPC_form})

    if entity == 'party':
        addParty_form = forms.AddPartyForm(request.POST)
        if request.method == 'POST':
            if 'submitParty' in request.POST:
                submit_record(request, 'party')
                # Render success message
                messages.success(request, "Party Successfully Added")
                return redirect('add_model', 'party')
        return render(request, 'user_forms/add_records/add_party.html', {'addParty_form': addParty_form})

    if entity == 'producer':
        addProducer_form = forms.AddProducerForm(request.POST)
        if request.method == 'POST':
            if 'submitProducer' in request.POST:
                submit_record(request, 'producer')
                # Render success message
                messages.success(request, "Producer Successfully Added")
                return redirect('add_model', 'producer')
        return render(request, 'user_forms/add_records/add_producer.html', {'addProducer_form': addProducer_form})

    if entity == 'publisher':
        addPublisher_form = forms.AddPublisherForm(request.POST)
        if request.method == 'POST':
            if 'submitPublisher' in request.POST:
                submit_record(request, 'publisher')
                # Render success message
                messages.success(request, "Publisher Successfully Added")
                return redirect('add_model', 'publisher')
        return render(request, 'user_forms/add_records/add_publisher.html', {'addPublisher_form': addPublisher_form})

    if entity == 'system':
        addSystem_form = forms.AddSystemForm(request.POST)
        if 'submitSystem' in request.POST:
            submit_record(request, 'system')
            # Render success message
            messages.success(request, "System Successfully Added")
            return redirect('add_model', 'system')
        return render(request, 'user_forms/add_records/add_system.html', {'addSystem_form': addSystem_form})


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


def submit_record(request, entity):
    if entity == 'campaign':
        # Get the IDs of the objects you're looking to add
        party_ids = request.POST.getlist('party')
        gm_ids = request.POST.getlist('gm')
        guest_pc_ids = request.POST.getlist('guest_pcs')
        producer_ids = request.POST.getlist('produced_by')

        # Create a query set of Party objects from the list of IDs
        party_objects = models.Party.objects.filter(id__in=party_ids)
        gm_objects = models.Actor.objects.filter(id__in=gm_ids)
        guest_pc_objects = models.PC.objects.filter(id__in=guest_pc_ids)
        producer_objects = models.Producer.objects.filter(id__in=producer_ids)

        # Create and save the Campaign object
        campaign = models.Campaign.objects.create(
            title=request.POST['title'],
            medium=request.POST['medium'],
            link=request.POST['link'],
            image_url=request.POST['image_url'],
            blurb=request.POST['blurb'],
        )

        # Set the many-to-many fields with the related objects
        campaign.party.set(party_objects)
        campaign.gm.set(gm_objects)
        campaign.guest_pcs.set(guest_pc_objects)
        campaign.produced_by.set(producer_objects)

    if entity == 'actor':
        # Get the IDs of the m2m objects you're looking to add
        pc_ids = request.POST.getlist('characters')
        gm_campaign_ids = request.POST.getlist('gm_campaigns')

        # Create a query set of Party objects from the list of IDs
        pc_objects = models.PC.objects.filter(id__in=pc_ids)
        gm_campaign_objects = models.Campaign.objects.filter(id__in=gm_campaign_ids)

        # Create and save the Actor object
        actor = models.Actor.objects.create(
            name=request.POST['name'],
            link=request.POST['link'],
            image_url=request.POST['image_url'],
            blurb=request.POST['blurb'],
        )
        # Set the many-to-many fields with the related objects
        actor.characters.set(pc_objects)
        actor.gm_campaigns.set(gm_campaign_objects)

    if entity == 'pc':
        played_by_ids = request.POST.getlist('played_by')
        # Create a query set of Actor objects from the list of IDs
        played_by_actors = models.Actor.objects.filter(id__in=played_by_ids)
        # Create and save the PC object
        pc = models.PC.objects.create(
            name=request.POST['name'],
            fandom_page=request.POST['fandom_page'],
            image_url=request.POST['image_url'],
            blurb=request.POST['blurb'],
        )
        # Set the 'played_by' field with the related Actor objects
        pc.played_by.set(played_by_actors)
        # Notify Followers of the Actor
        # for actor in played_by_actors:
        #     for user in actor.followers.all():
        #         models.Notification.objects.create(
        #             receiver=user,
        #             subject="New PC played by " + actor.name + " added to database",
        #             message="A new player character played by " + actor.name + " was just added to our database."
        #         )

    if entity == 'party':
        member_ids = request.POST.getlist('members')

        # Create a query set of Actor objects from the list of IDs
        member_pcs = models.PC.objects.filter(id__in=member_ids)

        # Create and save the PC object
        party = models.Party.objects.create(
            name=request.POST['name'],
            fandom_page=request.POST['fandom_page'],
            image_url=request.POST['image_url'],
            blurb=request.POST['blurb'],
        )

        # Set the 'played_by' field with the related Actor objects
        party.members.set(member_pcs)
    if entity == 'producer':
        campaign_ids = request.POST.getlist('campaigns')

        # Create a query set of Actor objects from the list of IDs
        campaigns = models.Producer.objects.filter(id__in=campaign_ids)

        # Create and save the PC object
        producer = models.Producer.objects.create(
            name=request.POST['name'],
            medium=request.POST['medium'],
            link=request.POST['link'],
            image_url=request.POST['image_url'],
            blurb=request.POST['blurb'],
        )

        # Set the 'played_by' field with the related Actor objects
        producer.campaigns.set(campaign_ids)
    if entity == 'publisher':
        system_ids = request.POST.getlist('systems')

        # Create a query set of Actor objects from the list of IDs
        systems = models.System.objects.filter(id__in=system_ids)

        # Create and save the PC object
        publisher = models.Publisher.objects.create(
            name=request.POST['name'],
            link=request.POST['link'],
            image_url=request.POST['image_url'],
            blurb=request.POST['blurb'],
        )

        # Set the 'played_by' field with the related Actor objects
        publisher.systems.set(systems)
    if entity == 'system':
        publisher_ids = request.POST.getlist('publisher')

        # Create a query set of Actor objects from the list of IDs
        publisher = models.Producer.objects.filter(id__in=publisher_ids)

        # Create and save the PC object
        system = models.System.objects.create(
            name=request.POST['name'],
            link=request.POST['link'],
            image_url=request.POST['image_url'],
            blurb=request.POST['blurb'],
        )

        # Set the 'played_by' field with the related Actor objects
        system.published_by.set(publisher)
