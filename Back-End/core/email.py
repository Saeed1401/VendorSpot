from djoser.email import ActivationEmail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from djoser.conf import settings as djoser_setting




class MyActivationEmail(ActivationEmail):
    """
    difference between this custom class with the default one is that,
    in the default djoser implementation of email templates, it provide 
    a link to a front-end page so the user by clicking in that link 
    would be mapped to a front-end page which the front-end then sends a
    post request to server to activate the user but in this custom class
    we changed the functionality to a direct link in email so the user would
    be activated directly.
    """

    template_name = "core/activation.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context['user']
        context['activation_url'] = self.activation_url(user)
        return context

    
    def activation_url(self, user):
        uid = utils.encode_uid(user.pk)
        token = default_token_generator.make_token(user)
        activate_url = reverse('core:custom_activation', args=[uid, token])
        direct_url = f'{djoser_setting.PROTOCOL}://{djoser_setting.DOMAIN}{activate_url}'
        return direct_url