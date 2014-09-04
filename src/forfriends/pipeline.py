import datetime

from requests import request, HTTPError

from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from profiles.models import Address, Job, Info, UserPicture, Gamification



'''def save_profile_picture(strategy, user, response, details, is_new=False,*args,**kwargs):

    if is_new and strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            profile = user.get_profile()
            profile.profile_photo.save('{0}_social.jpg'.format(user.username),
                                   ContentFile(response.content))
            profile.save()
'''

# User details pipeline
    def user_details(strategy, details, response, user=None, *args, **kwargs):
        """Update user details using data from provider."""
        if user:
            if kwargs['is_new']:
                attrs = {'user': user}
               #if facebook
                if strategy.backend.__class__.__name__ == 'FacebookOAuth2':
                    fb_data = {
                        'city': response['location']['name'],
                        'gender': response['gender'],
                        'birthday': datetime.fromtimestamp(mktime(strptime(response['birthday'], '%m/%d/%Y')))
                    }
                    attrs = dict(attrs.items() + fb_data.items())
                Info.objects.create(
                    **attrs
                )
    
