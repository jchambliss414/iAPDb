from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django_ckeditor_5.fields import CKEditor5Field

# ---------------------------------------- create profile on user signup ----------------------------------------
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_user_profile, sender=User)


# ----------------------------------------  watchlist models ----------------------------------------
class Watchlist(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile.user}'s Watchlist:"


class WatchingList(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile.user}'s Watchinglist:"


class HaveWatchedList(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile.user}'s HaveWatchedList:"


# ---------------------------------------- follower models ----------------------------------------
class ActorFollowers(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    actor = models.ForeignKey('Actor', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile}"


class CampaignFollowers(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile}"


class ProducerFollowers(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    Producer = models.ForeignKey('Producer', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile}"


# ---------------------------------------- bridge models ----------------------------------------
class ActorAccounts(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    actor = models.ForeignKey('Actor', on_delete=models.CASCADE)

    def __str__(self):
        return "Actor Pages:"


class ActorCharacters(models.Model):
    pc = models.ForeignKey('PC', on_delete=models.CASCADE)
    actor = models.ForeignKey('Actor', on_delete=models.CASCADE)

    def __str__(self):
        return "PCs:"


class CampaignParty(models.Model):
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)
    party = models.ForeignKey('Party', on_delete=models.CASCADE)

    def __str__(self):
        return "Party:"


class CampaignGuests(models.Model):
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)
    pc = models.ForeignKey('PC', on_delete=models.CASCADE)

    def __str__(self):
        return "Guest PCs:"


class CampaignSystem(models.Model):
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)
    system = models.ForeignKey('system', on_delete=models.CASCADE)

    def __str__(self):
        return "Systems:"


class CampaignGMs(models.Model):
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)
    actor = models.ForeignKey('actor', on_delete=models.CASCADE)

    def __str__(self):
        return "GMs:"


class EpisodesWatched(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    episode = models.ForeignKey('Episode', on_delete=models.CASCADE)

    def __str__(self):
        return "Episodes Watched"


class ProducerCampaigns(models.Model):
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)
    Producer = models.ForeignKey('Producer', on_delete=models.CASCADE)

    def __str__(self):
        return "Producer campaigns"


class ProducerOwners(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    Producer = models.ForeignKey('Producer', on_delete=models.CASCADE)

    def __str__(self):
        return "Producer Accounts:"


class PartyMembers(models.Model):
    pc = models.ForeignKey('PC', on_delete=models.CASCADE)
    party = models.ForeignKey('party', on_delete=models.CASCADE)

    def __str__(self):
        return "Members:"


class PublisherSystems(models.Model):
    system = models.ForeignKey('System', on_delete=models.CASCADE)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)

    def __str__(self):
        return "Publisher Systems"


# ---------------------------------------- Models ----------------------------------------
class Actor(models.Model):
    name = models.CharField(max_length=2083, blank=True, null=True)
    blurb = models.TextField(max_length=5000, blank=True, null=True)
    characters = models.ManyToManyField('PC', through=ActorCharacters, blank=True)
    gm_campaigns = models.ManyToManyField('Campaign', through=CampaignGMs, blank=True)
    followers = models.ManyToManyField('Profile', through=ActorFollowers, blank=True)
    account_owners = models.ManyToManyField('Profile', through='ActorAccounts', blank=True, related_name='actor_owner')
    link = models.CharField(max_length=2083, blank=True, null=True)
    image_url = models.CharField(max_length=2083, blank=True, null=False,
                                 default="static/images/default_profile_pic.png")

    class Meta:
        verbose_name = 'Actor'

    def __str__(self):
        return self.name or ''


class Campaign(models.Model):
    Ongoing = 'Ongoing'
    Complete = 'Complete'
    On_Hiatus = 'On Hiatus'
    Podcast = 'Podcast'
    Video = 'Video'
    Live_Stream = 'Live Stream'
    One_Shot = 'One-Shot'
    Series = 'Series'

    progress_choices = [
        (Ongoing, 'Ongoing'), (Complete, 'Complete'), (On_Hiatus, 'On Hiatus')
    ]
    medium_choices = [
        (Podcast, 'Podcast'), (Video, 'Video'), (Live_Stream, 'Live Stream')
    ]
    type_choices = [
        (One_Shot, 'One-Shot'), (Series, 'Series')
    ]

    title = models.CharField(max_length=2083, blank=True, null=True)
    party = models.ManyToManyField('Party', through='CampaignParty', blank=True)
    guest_pcs = models.ManyToManyField('PC', through=CampaignGuests, blank=True)
    gm = models.ManyToManyField('Actor', through='CampaignGMs', blank=True, related_name='campaign_gms')
    system = models.ManyToManyField('System', through='CampaignSystem', blank=True, related_name='campaign_systems')
    produced_by = models.ManyToManyField('Producer', through=ProducerCampaigns, blank=True,
                                         related_name='campaign_companies')
    progress = models.CharField(max_length=100, choices=progress_choices, blank=True, null=True)
    medium = MultiSelectField(choices=medium_choices, blank=True, null=True, max_length=100)
    type = models.CharField(max_length=100, choices=type_choices, blank=True, null=True)
    watchlist_profiles = models.ManyToManyField('Profile', through=Watchlist, blank=True,
                                                related_name='towatch_campaign')
    watchinglist_profiles = models.ManyToManyField('Profile', through=WatchingList, blank=True,
                                                   related_name='watching_campaign')
    watchedlist_profiles = models.ManyToManyField('Profile', through=HaveWatchedList, blank=True,
                                                  related_name='watched_campaign')
    blurb = models.TextField(max_length=5000, blank=True, null=True)
    link = models.CharField(max_length=2083, blank=True, null=True)
    followers = models.ManyToManyField('Profile', through=CampaignFollowers, blank=True)
    featured = models.BooleanField(null=True, blank=True)
    image_url = models.CharField(max_length=2083, blank=True, null=False, default="static/images/default-rect-img.png")

    class Meta:
        verbose_name = 'Campaign'

    def __str__(self):
        return self.title or ''


class Episode(models.Model):
    Podcast = 'Podcast'
    Video = 'Video'
    Live_Stream = 'Live Stream'

    medium_choices = [
        (Podcast, 'Podcast'), (Video, 'Video'), (Live_Stream, 'Live Stream')
    ]

    title = models.CharField(max_length=2083, blank=True, null=True)
    medium = MultiSelectField(choices=medium_choices, blank=True, null=True, max_length=100)
    blurb = models.TextField(max_length=5000, blank=True, null=True)
    link = models.CharField(max_length=2083, blank=True, null=True)
    runtime = models.DurationField(blank=True, verbose_name="Runtime (hh:mm)")
    in_campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, verbose_name='Campaign', blank=True, null=True)
    ep_count = models.IntegerField(blank=False, null=False, default="01")
    airdate = models.DateField(blank=True, null=True)
    image_url = models.CharField(max_length=2083, blank=True, null=False, default="static/images/default-rect-img.png")

    class Meta:
        verbose_name = 'Episode'

    def __str__(self):
        return self.title or '(Untitled)'


class Notification(models.Model):
    n_type_list = [
        ('CRUD_event', 'CRUD_event')
    ]

    notification_type = MultiSelectField(choices=n_type_list, blank=True, null=True, max_length=100)
    receiver = models.ForeignKey('Profile', blank=True, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=False, null=False, default='[Subject]')
    message = models.TextField(max_length=5000, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)

    updated_obj_type = models.CharField(max_length=50, blank=True, null=True)
    updated_obj_id = models.IntegerField(blank=True, null=True)
    added_instance_type = models.CharField(max_length=50, blank=True, null=True)
    added_instance_id = models.IntegerField(blank=True, null=True)



    class Meta:
        verbose_name = 'Notification'

    def __str__(self):
        return self.subject or '(Untitled)'


class Party(models.Model):
    name = models.CharField(max_length=2083, blank=True, null=True)
    blurb = models.TextField(max_length=5000, blank=True, null=True)
    members = models.ManyToManyField('PC', through=PartyMembers, blank=True)
    campaigns = models.ManyToManyField(Campaign, through=CampaignParty, blank=True, related_name='party_campaigns')
    fandom_page = models.CharField(max_length=2083, blank=True, null=True)
    image_url = models.CharField(max_length=2083, blank=True, null=False,
                                 default="static/images/default-rect-img.png")

    class Meta:
        verbose_name = 'Party'

    def __str__(self):
        return self.name or ''


class PC(models.Model):
    name = models.CharField(max_length=2083, blank=True, null=True)
    blurb = models.TextField(max_length=5000, blank=True, null=True)
    played_by = models.ManyToManyField(Actor, through=ActorCharacters, blank=True)
    fandom_page = models.CharField(max_length=2083, blank=True, null=True)
    member_of = models.ManyToManyField('Party', through=PartyMembers, blank=True)
    guest_of = models.ManyToManyField('Campaign', through=CampaignGuests, blank=True)
    image_url = models.CharField(max_length=2083, blank=True, null=False,
                                 default="static/images/default_profile_pic.png")

    class Meta:
        verbose_name = 'PC'

    def __str__(self):
        return self.name or ''


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=2083, blank=True, null=True,
                                 default='static/images/default_profile_pic.png')
    campaigns_to_watch = models.ManyToManyField('Campaign', through=Watchlist, blank=True, related_name='To_Watch')
    campaigns_watching = models.ManyToManyField('Campaign', through=WatchingList, blank=True, related_name='Watching')
    campaigns_watched = models.ManyToManyField('Campaign', through=HaveWatchedList, blank=True,
                                               related_name='Have_Watched')
    campaigns_following = models.ManyToManyField('Campaign', through=CampaignFollowers, blank=True,
                                                 related_name='campaign_followers')
    actors_following = models.ManyToManyField('Actor', through=ActorFollowers, blank=True,
                                              related_name='actors_following')
    producers_following = models.ManyToManyField('Producer', through=ProducerFollowers, blank=True,
                                                 related_name='producers_following')
    producer_accounts = models.ManyToManyField('Producer', through=ProducerOwners, blank=True)
    actor_accounts = models.ManyToManyField('Actor', through='ActorAccounts', blank=True)
    episodes_watched = models.ManyToManyField('Episode', through='EpisodesWatched', blank=True)
    USERNAME_FIELD = ()

    class Meta:
        verbose_name = 'Profile'

    def __str__(self):
        return self.user.username


class Producer(models.Model):
    Podcast = 'Podcast'
    Video = 'Video'
    Live_Stream = 'Live Stream'

    medium_choices = [
        (Podcast, 'Podcast'), (Video, 'Video'), (Live_Stream, 'Live Stream')
    ]

    name = models.CharField(max_length=2083, blank=True, null=True)
    medium = MultiSelectField(choices=medium_choices, blank=True, null=True, max_length=100)
    blurb = models.TextField(max_length=5000, blank=True, null=True)
    link = models.CharField(max_length=2083, blank=True, null=True)
    campaigns = models.ManyToManyField('Campaign', through=ProducerCampaigns, blank=True,
                                       related_name='Producer_campaigns')
    account_owners = models.ManyToManyField('Profile', through='ProducerOwners', blank=True,
                                            related_name='Producer_owners')
    followers = models.ManyToManyField('Profile', through=ProducerFollowers, blank=True,
                                       related_name='Producer_followers')
    image_url = models.CharField(max_length=2083, blank=True, null=False,
                                 default="static/images/default-rect-img.png")

    class Meta:
        verbose_name = 'Producer'

    def __str__(self):
        return self.name or ''


class Publisher(models.Model):
    name = models.CharField(max_length=2083, blank=True, null=True)
    blurb = models.TextField(max_length=5000, blank=True, null=True)
    systems = models.ManyToManyField('System', through=PublisherSystems, blank=True,
                                     related_name='publisher_systems')
    link = models.CharField(max_length=2083, blank=True, null=True)
    image_url = models.CharField(max_length=2083, blank=True, null=False,
                                 default="static/images/default-rect-img.png")

    class Meta:
        verbose_name = 'Publisher'

    def __str__(self):
        return self.name or ''


class System(models.Model):
    name = models.CharField(max_length=2083, blank=True, null=True)
    blurb = models.TextField(max_length=5000, blank=True, null=True)
    campaigns = models.ManyToManyField('Campaign', through='CampaignSystem', blank=True,
                                       related_name='system_campaigns')
    published_by = models.ManyToManyField(Publisher, through=PublisherSystems, blank=True,
                                          related_name='system_publishers')
    link = models.CharField(max_length=2083, blank=True, null=True)
    image_url = models.CharField(max_length=2083, blank=True, null=False,
                                 default="static/images/default-rect-img.png")

    class Meta:
        verbose_name = 'System'

    def __str__(self):
        return self.name or ''
