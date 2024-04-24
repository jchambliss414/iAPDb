from django.shortcuts import render, get_object_or_404, redirect
from database import models


def landing_page(request):
    return render(request, 'landingpage.html')







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
