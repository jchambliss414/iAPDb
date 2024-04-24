from django.contrib import admin
from database import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


# -------------------- Inlines --------------------
class ActorAccountsInline(admin.TabularInline):
    model = models.ActorAccounts
    extra = 1


class ActorCharactersInline(admin.TabularInline):
    model = models.ActorCharacters
    extra = 1


class CampaignPartyInline(admin.TabularInline):
    model = models.CampaignParty
    extra = 1


class CampaignGuestsInline(admin.TabularInline):
    model = models.CampaignGuests
    extra = 1


class CampaignSystemInline(admin.TabularInline):
    model = models.CampaignSystem
    extra = 1


class CampaignGMsInline(admin.TabularInline):
    model = models.CampaignGMs
    extra = 1


class ProducerCampaignsInline(admin.TabularInline):
    model = models.ProducerCampaigns
    extra = 1


class ProducerOwnersInline(admin.TabularInline):
    model = models.ProducerOwners
    extra = 1


class ProfileProducerInline(admin.TabularInline):
    model = models.ProducerOwners
    extra = 1


class PartyMembersInline(admin.TabularInline):
    model = models.PartyMembers
    extra = 1


class PublisherSystemsInline(admin.TabularInline):
    model = models.PublisherSystems
    extra = 1


# -------------------- Admin Pages --------------------

class UserAdmin(admin.ModelAdmin):
    exclude = []


class ActorAdmin(admin.ModelAdmin):
    inlines = [ActorCharactersInline, CampaignGMsInline, ActorAccountsInline]
    list_display = ['id', 'name']


class CampaignAdmin(admin.ModelAdmin):
    inlines = [CampaignPartyInline, CampaignGuestsInline, CampaignSystemInline, CampaignGMsInline, ProducerCampaignsInline,
               ]
    list_display = ['id', 'title']


class EpisodeAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['id', 'title']


class PartyAdmin(admin.ModelAdmin):
    inlines = [PartyMembersInline, CampaignPartyInline]
    list_display = ['id', 'name']


class PCAdmin(admin.ModelAdmin):
    inlines = [PartyMembersInline, ActorCharactersInline, CampaignGuestsInline]
    list_display = ['id', 'name']


class ProducerAdmin(admin.ModelAdmin):
    inlines = [ProducerCampaignsInline]
    list_display = ['id', 'name']


class PublisherAdmin(admin.ModelAdmin):
    inlines = [PublisherSystemsInline]
    list_display = ['id', 'name']


class ProfileAdmin(admin.ModelAdmin):
    exclude = []
    inlines = [ProfileProducerInline]


class NotificationAdmin(admin.ModelAdmin):
    exclude = ()


class SystemAdmin(admin.ModelAdmin):
    inlines = [CampaignSystemInline, PublisherSystemsInline]


admin.site.unregister(User)

User = get_user_model()
admin.site.register(User, UserAdmin)
admin.site.register(
    models.Profile, ProfileAdmin
)
admin.site.register(models.Actor, ActorAdmin)
admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.Episode, EpisodeAdmin)
admin.site.register(models.Notification, NotificationAdmin)
admin.site.register(models.Party, PartyAdmin)
admin.site.register(models.PC, PCAdmin)
admin.site.register(models.Publisher, PublisherAdmin)
admin.site.register(models.Producer, ProducerAdmin)
admin.site.register(models.System, SystemAdmin)


