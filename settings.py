import os
from dotenv import load_dotenv

# FIXME: Yes I know unsafe-eval and unsafe-inline is bad bad...
# I spent enough hours trying to get the nonce to work to give up and move on...
# It's probably something stupid...
CSP_POLICY = {
    "default-src": "'self'",
    "script-src": ["'self'", "'unsafe-eval'", "'unsafe-inline'", "ajax.googleapis.com", "*.googleanalytics.com", "*.google-analytics.com"],
    "style-src": ["'self'", "'unsafe-inline'", "ajax.googleapis.com", "fonts.googleapis.com", "*.gstatic.com"],
    "img-src": ["'self'", "*.google-analytics.com"],
    "connect-src": ["'self'", "*.google-analytics.com"],
    "font-src": ["'self'", "*.gstatic.com"],
    "object-src": "'none'",
    "base-uri": "'none'",
    "frame-ancestors": "'none'",
}

# FIXME: Update once CSP_POLICY is actually compliant
CSP_POLICY_NONCE_IN = []


load_dotenv()

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
