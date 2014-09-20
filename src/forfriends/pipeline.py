import datetime

from requests import request, HTTPError
from social.pipeline.user import get_username as social_get_username


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
'''def user_details(strategy, details, response, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if user:
        if kwargs['is_new']:
            attrs = {'user': user}
           #if facebook
            if strategy.backend.__class__.__name__ == 'FacebookOAuth2':
                fb_data = {
                    
                    'gender': response['gender'],
                    
                }
                attrs = dict(attrs.items() + fb_data.items())
            Info.objects.create(
                **attrs
            )
'''

def associate_user_by_email(**kwargs):
    try:
        email = kwargs['details']['email']
        kwargs['user'] = User.objects.get(email=email)
    except:
        pass
    return kwargs


def get_username(strategy, details, user=None, *args, **kwargs):
    username_old = social_get_username(strategy, details, user=user, *args, **kwargs)
    username = username_old[0]
    username_new = username.translate(None, " ?.!/;:")
    return username_new



    
