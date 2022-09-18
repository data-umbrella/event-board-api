from django.conf import settings


def passwordless_email_processor():
   return {
     'magic_link_domain': settings.MAGIC_LINK_DOMAIN,
   }
