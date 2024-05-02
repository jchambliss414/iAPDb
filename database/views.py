from django.shortcuts import render, redirect, get_object_or_404
from members import forms
from database import models
from django.utils.dateparse import parse_duration


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


def campaign_database(request):
    campaigns = models.Campaign.objects.all()

    return render(request, 'database/campaign_database.html', {'campaigns': campaigns})


def actor_database(request):
    actors = models.Actor.objects.all()

    return render(request, 'database/actor_database.html', {'actors': actors})


def pc_database(request):
    pcs = models.PC.objects.all()

    return render(request, 'database/pc_database.html', {'pcs': pcs})


def party_database(request):
    parties = models.Party.objects.all()

    return render(request, 'database/party_database.html', {'parties': parties})


def producer_database(request):
    producers = models.Producer.objects.all()

    return render(request, 'database/producer_database.html', {'producers': producers})


def system_database(request):
    systems = models.System.objects.all()
    featured_campaigns = models.Campaign.objects.filter(featured=True)

    return render(request, 'database/system_database.html', {'systems': systems,
                                                             'featured_campaigns': featured_campaigns})


def publisher_database(request):
    publishers = models.Publisher.objects.all()

    return render(request, 'database/publisher_database.html', {'publishers': publishers    })


def model_pages(request, entity, ent_id):
    if entity == "campaigns":
        campaign = get_object_or_404(models.Campaign, id=ent_id)
        context = {'campaign': campaign}

        if 'previousEnt' in request.POST:
            return redirect('model_page', entity, ent_id-1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id+1)

        return render(request, 'database/model_pages/campaign_page.html', context)
    if entity == "actors":
        actor = get_object_or_404(models.Actor, id=ent_id)
        context = {'actor': actor}

        if 'previousEnt' in request.POST:
            return redirect('model_page', entity, ent_id-1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id+1)

        return render(request, 'database/model_pages/actor_page.html', context)
    if entity == "pcs":
        pc = get_object_or_404(models.PC, id=ent_id)
        context = {'pc': pc}

        if 'previousEnt' in request.POST:
            return redirect('model_page', entity, ent_id-1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id+1)

        return render(request, 'database/model_pages/pc_page.html', context)
    if entity == "producers":
        producer = get_object_or_404(models.Producer, id=ent_id)
        context = {'producer': producer}

        if 'previousEnt' in request.POST:
            return redirect('model_page', entity, ent_id-1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id+1)

        return render(request, 'database/model_pages/producer_page.html', context)
    if entity == "publishers":
        publisher = get_object_or_404(models.Publisher, id=ent_id)
        context = {'publisher': publisher}

        if 'previousEnt' in request.POST:
            return redirect('model_page', entity, ent_id-1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id+1)

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
            return redirect('model_page', entity, ent_id-1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id+1)

        return render(request, 'database/model_pages/system_page.html', context)
    if entity == "parties":
        party = get_object_or_404(models.Party, id=ent_id)
        context = {'party': party}

        if 'previousEnt' in request.POST:
            return redirect('model_page', entity, ent_id-1)
        if 'nextEnt' in request.POST:
            return redirect('model_page', entity, ent_id+1)

        return render(request, 'database/model_pages/party_page.html', context)


def add_new_actor(request):
    addActor_form = forms.AddActorForm(request.POST)

    if request.method == 'POST':
        if 'submitActor' in request.POST:
            models.Actor.objects.create(
                name=request.POST['name'],
                link=request.POST['link'],
                image_url=request.POST['image_url'],
                blurb=request.POST['blurb'],
            )
            return redirect('database_home')
    return render(request, 'user_forms/add_records/add_actor.html', {'addActor_form': addActor_form})


# @login_required(login_url='/login')
def add_new_campaign(request):
    addCampaign_form = forms.AddCampaignForm(request.POST)

    if request.method == 'POST':
        if 'submitCampaign' in request.POST:
            # Get the IDs of the objects you're looking to add
            party_ids = request.POST.getlist('party')
            gm_ids = request.POST.getlist('gm')
            guest_pc_ids = request.POST.getlist('guests')

            # Create a query set of Party objects from the list of IDs
            party_objects = models.Party.objects.filter(id__in=party_ids)
            gm_objects = models.Actor.objects.filter(id__in=gm_ids)
            guest_pc_objects = models.PC.objects.filter(id__in=guest_pc_ids)

            # Create and save the Campaign object
            campaign = models.Campaign.objects.create(
                title=request.POST['title'],
                medium=request.POST['medium'],
                website=request.POST['website'],
                image_url=request.POST['image_url'],
                blurb=request.POST['blurb'],
            )

            # Set the many-to-many fields with the related objects
            campaign.party.set(party_objects)
            campaign.gm.set(gm_objects)
            campaign.guests.set(guest_pc_objects)

            # Redirect to the desired view
            return redirect('add_campaign')
    return render(request, 'user_forms/add_records/add_campaign.html', {'addCampaign_form': addCampaign_form})


# @login_required(login_url='/login')
def add_new_publisher(request):
    addPublisher_form = forms.AddPublisherForm(request.POST)

    if request.method == 'POST':
        if 'submitPublisher' in request.POST:
            system_ids = request.POST.getlist('systems')

            # Create a query set of Actor objects from the list of IDs
            systems = models.System.objects.filter(id__in=system_ids)

            # Create and save the PC object
            publisher = models.Publisher.objects.create(
                name=request.POST['name'],
                website=request.POST['website'],
                image_url=request.POST['image_url'],
                blurb=request.POST['blurb'],
            )

            # Set the 'played_by' field with the related Actor objects
            publisher.systems.set(systems)

            # Redirect to the desired view
            return redirect('add_publisher')
    return render(request, 'user_forms/add_records/add_publisher.html', {'addPublisher_form': addPublisher_form})


# @login_required(login_url='/login')
def add_new_producer(request):
    addProducer_form = forms.AddProducerForm(request.POST)

    if request.method == 'POST':
        if 'submitProducer' in request.POST:
            campaign_ids = request.POST.getlist('campaigns')

            # Create a query set of Actor objects from the list of IDs
            campaigns = models.Producer.objects.filter(id__in=campaign_ids)

            # Create and save the PC object
            producer = models.Producer.objects.create(
                name=request.POST['name'],
                medium=request.POST['medium'],
                website=request.POST['website'],
                image_url=request.POST['image_url'],
                blurb=request.POST['blurb'],
            )

            # Set the 'played_by' field with the related Actor objects
            producer.campaigns.set(campaigns)
            return redirect('add_producer')
    return render(request, 'user_forms/add_records/add_producer.html', {'addProducer_form': addProducer_form})


# @login_required(login_url='/login')
def add_new_party(request):
    addParty_form = forms.AddPartyForm(request.POST)

    if request.method == 'POST':
        if 'submitParty' in request.POST:
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

            # Redirect to the desired view
            return redirect('add_party')
    return render(request, 'user_forms/add_records/add_party.html', {'addParty_form': addParty_form})


# @login_required(login_url='/login')
def add_new_pc(request):
    addPC_form = forms.AddPCForm(request.POST)

    if request.method == 'POST':
        if 'submitPC' in request.POST:
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

            # Redirect to the desired view
            return redirect('add_pc')
    return render(request, 'user_forms/add_records/add_pc.html', {'addPC_form': addPC_form})


# @login_required(login_url='/login')
def add_new_system(request):
    addSystem_form = forms.AddSystemForm(request.POST)

    if 'submitSystem' in request.POST:
        publisher_ids = request.POST.getlist('publisher')

        # Create a query set of Actor objects from the list of IDs
        publisher = models.Producer.objects.filter(id__in=publisher_ids)

        # Create and save the PC object
        system = models.System.objects.create(
            name=request.POST['name'],
            website=request.POST['website'],
            image_url=request.POST['image_url'],
            blurb=request.POST['blurb'],
        )

        # Set the 'played_by' field with the related Actor objects
        system.published_by.set(publisher)

        return redirect('add_system')
    return render(request, 'user_forms/add_records/add_system.html', {'addSystem_form': addSystem_form})


# @login_required(login_url='/login')
def add_new_episode(request, campaign_id):
    form = forms.AddEpisodeForm(request.POST)
    campaign = get_object_or_404(models.Campaign, id=campaign_id)

    if request.method == 'POST':
        if 'submitEpisode' in request.POST:
            models.Episode.objects.create(
                title=request.POST['title'],
                link=request.POST['link'],
                image_url=request.POST['image_url'],
                blurb=request.POST['blurb'],
                airdate=request.POST['airdate'],
                medium=request.POST['medium'],
                in_campaign=campaign,
                runtime=parse_duration(request.POST['runtime']),
                ep_count=request.POST['ep_count']
            )
            return redirect('campaign_id', campaign_id)
    return render(request, 'user_forms/add_records/add_episode.html', {'form': form})
