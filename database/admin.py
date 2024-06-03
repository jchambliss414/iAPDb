from django.contrib import admin
from database import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


# -------------------- Inlines --------------------
class ActorAccountsInline(admin.TabularInline):
    model = models.ActorAccounts
    extra = 1
    verbose_name = 'Actor Account'


class ActorCharactersInline(admin.TabularInline):
    model = models.ActorCharacters
    extra = 1
    verbose_name = 'Actor Character'


class CampaignEpisodeInline(admin.TabularInline):
    model = models.Episode
    fields = ('title', 'ep_count')
    readonly_fields = ('title', 'ep_count')
    can_delete = False
    extra = 0
    verbose_name = 'Campaign Episode'


class CampaignPartyInline(admin.TabularInline):
    model = models.CampaignParty
    extra = 1
    verbose_name = 'Campaign Party'
    verbose_name_plural = 'Campaign Parties'


class CampaignGuestsInline(admin.TabularInline):
    model = models.CampaignGuests
    extra = 1
    verbose_name = 'Campaign Guest'


class CampaignSystemInline(admin.TabularInline):
    model = models.CampaignSystem
    extra = 1
    verbose_name = 'Campaign System'


class CampaignGMsInline(admin.TabularInline):
    model = models.CampaignGMs
    extra = 1
    verbose_name = 'Campaign GM'


class ProducerCampaignsInline(admin.TabularInline):
    model = models.ProducerCampaigns
    extra = 1
    verbose_name = 'Producer Campaign'


class ProducerOwnersInline(admin.TabularInline):
    model = models.ProducerOwners
    extra = 1
    verbose_name = 'Producer Owner'


class PartyMembersInline(admin.TabularInline):
    model = models.PartyMembers
    extra = 1
    verbose_name = 'Party Member'


class PublisherSystemsInline(admin.TabularInline):
    model = models.PublisherSystems
    extra = 1
    verbose_name = 'Publisher System'


class WatchlistInline(admin.TabularInline):
    model = models.Watchlist
    extra = 1
    verbose_name = 'Watchlist Campaign'


class WatchinglistInline(admin.TabularInline):
    model = models.WatchingList
    extra = 1
    verbose_name = 'Watching Campaign'


class WatchedlistInline(admin.TabularInline):
    model = models.HaveWatchedList
    extra = 1
    verbose_name = 'Have Watched Campaign'


class FollowingActorsInline(admin.TabularInline):
    model = models.ActorFollowers
    extra = 1
    verbose_name = 'Following Actor'


class FollowingCampaignsInline(admin.TabularInline):
    model = models.CampaignFollowers
    extra = 1
    verbose_name = 'Following Campaign'


class FollowingProducersInline(admin.TabularInline):
    model = models.ProducerFollowers
    extra = 1
    verbose_name = 'Following Producer'


# -------------------- Admin Pages --------------------

class UserAdmin(admin.ModelAdmin):
    exclude = []


class ActorAdmin(admin.ModelAdmin):
    inlines = [ActorCharactersInline, CampaignGMsInline, ActorAccountsInline]
    list_display = ['id', 'name']


class CampaignAdmin(admin.ModelAdmin):
    inlines = [CampaignPartyInline, CampaignGuestsInline, CampaignSystemInline, CampaignGMsInline,
               ProducerCampaignsInline, CampaignEpisodeInline]
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
    inlines = [WatchlistInline, WatchinglistInline, WatchedlistInline, FollowingActorsInline,
               FollowingCampaignsInline, FollowingProducersInline]
    exclude = []


class NotificationAdmin(admin.ModelAdmin):
    exclude = ()


class CRUDNotificationAdmin(admin.ModelAdmin):
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
admin.site.register(models.Party, PartyAdmin)
admin.site.register(models.PC, PCAdmin)
admin.site.register(models.Publisher, PublisherAdmin)
admin.site.register(models.Producer, ProducerAdmin)
admin.site.register(models.System, SystemAdmin)


