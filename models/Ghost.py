from google.cloud import ndb


class Ghost(ndb.Model):
    """Datastore Model for storing ghost names."""
    email = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    ghost_name = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    description = ndb.StringProperty()
