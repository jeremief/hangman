"""utils.py - File for collecting general utility functions."""

import logging
from google.appengine.ext import ndb
import endpoints

def get_by_urlsafe(urlsafe, model):
    """Returns an ndb.Model entity that the urlsafe key points to. Checks
        that the type of entity returned is of the correct kind. Raises an
        error if the key String is malformed or the entity is of the incorrect
        kind
    Args:
        urlsafe: A urlsafe key string
        model: The expected entity kind
    Returns:
        The entity that the urlsafe Key string points to or None if no entity
        exists.
    Raises:
        ValueError:""" 
    try:
        key = ndb.Key(urlsafe=urlsafe)
        print "Key allocated to key"
    except TypeError:
        raise endpoints.BadRequestException('Invalid Key')
        print "Type error"
    except Exception, e:
        if e.__class__.__name__ == 'ProtocolBufferDecodeError':
            raise endpoints.BadRequestException('Invalid Key')
        else:
            raise
        print "Exception"

    entity = key.get()
    print "key allocated to entity"
    if not entity:
        print "No entity to return"
        return None
    if not isinstance(entity, model):
        print "Value error - Incorrect kind"
        raise ValueError('Incorrect Kind')
    return entity
