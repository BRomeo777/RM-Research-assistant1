from slowapi import Limiter
from slowapi.util import get_remote_address

# Uses the user's IP address to track and limit request velocity
limiter = Limiter(key_func=get_remote_address)
