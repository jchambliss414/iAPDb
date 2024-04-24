from django.shortcuts import render


def members_list(request):
    return render(request, 'members_list.html')
