import environ

env = environ.Env(
    ENV_PATH=(str, None),
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, ''),
    EMAIL_HOST=(str, ''),
    EMAIL_PORT=(int, 587),
    EMAIL_HOST_USER=(str, ''),
    EMAIL_HOST_PASSWORD=(str, ''),
    EMAIL_USE_TLS=(bool, False),
    EMAIL_CONTACT_FORM_RECEIVER=(str, ''),
    MOLLIE_CLIENT_API=(str, ''),
    SHIPPING_TO_BELGIUM=(float, 5.95),
    TAX=(float, 0)
)
if env('ENV_PATH'):
    environ.Env.read_env(env('ENV_PATH'))
