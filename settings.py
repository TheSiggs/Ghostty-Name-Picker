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
