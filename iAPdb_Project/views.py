from django.shortcuts import render, get_object_or_404, redirect
from database import models


def landing_page(request):
    return render(request, 'landingpage.html')


def search_results(request):
    if request.method == 'POST':
        entity_searched = request.POST.get('entity_type')
        searched = request.POST.get('searched')

        if entity_searched == 'actors':
            results = models.Actor.objects.filter(name__icontains=searched)
            actors = models.Actor.objects.filter(name__icontains=searched)
            return render(request, 'database/search_results.html', {"searched": searched, "results": results,
                                                                          "actors": actors,
                                                                          "entity_searched": entity_searched})
        elif entity_searched == 'producers':
            results = models.Producer.objects.filter(name__icontains=searched)
            producers = models.Producer.objects.filter(name__icontains=searched)
            return render(request, 'database/search_results.html', {"searched": searched, "results": results,
                                                                          "producers": producers,
                                                                          "entity_searched": entity_searched})
        elif entity_searched == 'campaigns':
            results = models.Campaign.objects.filter(title__icontains=searched)
            campaigns = models.Campaign.objects.filter(title__icontains=searched)
            return render(request, 'database/search_results.html', {"searched": searched, "results": results,
                                                                          "campaigns": campaigns,
                                                                          "entity_searched": entity_searched})
        elif entity_searched == 'parties':
            results = models.Party.objects.filter(name__icontains=searched)
            parties = models.Party.objects.filter(name__icontains=searched)
            return render(request, 'database/search_results.html', {"searched": searched, "results": results,
                                                                          "parties": parties,
                                                                          "entity_searched": entity_searched})
        elif entity_searched == 'pcs':
            results = models.PC.objects.filter(name__icontains=searched)
            pcs = models.PC.objects.filter(name__icontains=searched)
            return render(request, 'database/search_results.html', {"searched": searched, "results": results,
                                                                          "pcs": pcs,
                                                                          "entity_searched": entity_searched})
        elif entity_searched == 'systems':
            results = models.System.objects.filter(name__icontains=searched)
            systems = models.System.objects.filter(name__icontains=searched)
            return render(request, 'database/search_results.html', {"searched": searched, "results": results,
                                                                          "systems": systems,
                                                                          "entity_searched": entity_searched})
        elif entity_searched == 'publishers':
            results = models.Publisher.objects.filter(name__icontains=searched)
            publishers = models.Publisher.objects.filter(name__icontains=searched)
            return render(request, 'database/search_results.html', {"searched": searched, "results": results,
                                                                          "publishers": publishers,
                                                                          "entity_searched": entity_searched})
        elif entity_searched == 'all':
            results = []
            actors = models.Actor.objects.filter(name__icontains=searched)
            producers = models.Producer.objects.filter(name__icontains=searched)
            campaigns = models.Campaign.objects.filter(title__icontains=searched)
            parties = models.Party.objects.filter(name__icontains=searched)
            pcs = models.PC.objects.filter(name__icontains=searched)
            systems = models.System.objects.filter(name__icontains=searched)
            publishers = models.Publisher.objects.filter(name__icontains=searched)
            for model in actors:
                if model:
                    results.append(model)
                else:
                    pass
            for model in producers:
                if model:
                    results.append(model)
                else:
                    pass
            for model in campaigns:
                if model:
                    results.append(model)
            for model in parties:
                if model:
                    results.append(model)
                else:
                    pass
            for model in pcs:
                if model:
                    results.append(model)
                else:
                    pass
            for model in systems:
                if model:
                    results.append(model)
                else:
                    pass
            for model in publishers:
                if model:
                    results.append(model)
                else:
                    pass
            result_count = 0
            for item in results:
                result_count += 1

            return render(request, 'database/search_results.html', {"searched": searched, "results": results,
                                                                          "entity_searched": entity_searched,
                                                                          "actors": actors, "producers": producers,
                                                                          "campaigns": campaigns, "pcs": pcs,
                                                                          "parties": parties, "systems": systems,
                                                                          "publishers": publishers,
                                                                          "result_count": result_count})
    else:
        return render(request, 'database/search_results.html', {})
    return render(request, 'database/search_results.html', {})


def elements_test_page(request):
    campaign = get_object_or_404(models.Campaign, id=1)
    actor = get_object_or_404(models.Actor, id=5)
    pc = get_object_or_404(models.PC, id=16)
    producer = get_object_or_404(models.Producer, id=1)
    party = get_object_or_404(models.Party, id=1)
    system = get_object_or_404(models.System, id=1)
    publisher = get_object_or_404(models.Publisher, id=1)

    return render(request, 'test_pages/elementsPage.html', {'campaign': campaign,
                                                            'actor': actor,
                                                            'pc': pc,
                                                            'producer': producer,
                                                            'party': party,
                                                            'system': system,
                                                            'publisher': publisher})


def campaign_model_test(request):
    return render(request, 'test_pages/model_pages/campaign_model.html')


def actor_model_test(request):
    return render(request, 'test_pages/model_pages/actor_model.html')


def pc_model_test(request):
    return render(request, 'test_pages/model_pages/pc_model.html')


def party_model_test(request):
    return render(request, 'test_pages/model_pages/party_model.html')


def producer_model_test(request):
    return render(request, 'test_pages/model_pages/producer_model.html')


def system_model_test(request):
    return render(request, 'test_pages/model_pages/system_model.html')


def publisher_model_test(request):
    return render(request, 'test_pages/model_pages/publisher_model.html')
