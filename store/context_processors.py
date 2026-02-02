from django.conf import settings

def setting_vars(request):
    return {
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
        'RECAPTCHA_PRIVATE_KEY': settings.RECAPTCHA_PRIVATE_KEY,
        'RECAPTCHA_SCORE_THRESHOLD': settings.RECAPTCHA_SCORE_THRESHOLD,
    }