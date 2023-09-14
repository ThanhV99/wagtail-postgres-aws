from .base import *

DEBUG = False

ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get('ALLOWED_HOSTS', '').split(','),
    )
)

try:
    from .local import *
except ImportError:
    pass
