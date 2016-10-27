"""utils.py - File for collecting general utility functions."""

import logging
from google.appengine.ext import ndb
import endpoints
import math

from models import User, HistoryRecord, Game, Score


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


def validate_input(user_input, char_number=0):
    """ This function validates that user input is an alpha only string
    of the required length
    """
    user_input_valid = True
    function_message = ""
    user_input_list = list(user_input)
    for i in user_input_list:
        if i.isdigit() == True:
            function_message = "No numbers please..."
            user_input_valid = False
    if user_input.isalnum() == False:
        function_message += "No special characters please..."
        user_input_valid = False
    if char_number != 0:
        if len(user_input) != char_number:
            if char_number != 1:
                function_message += "Only %i characters please..." % character
            else:
                function_message += "Only one character please..."
            user_input_valid = False
    if user_input_valid == True:
        return [True]
    else:
        return [False, function_message]

