from django.shortcuts import render, redirect, get_object_or_404
from database import models


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
