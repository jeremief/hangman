#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""
import logging

import webapp2
from google.appengine.api import mail, app_identity
from api import HangmanApi

from models import User, Game


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with an email about games.
        Called every 24 hours using a cron job"""
        app_id = app_identity.get_application_id()
        games = Game.query(Game.game_over == False).fetch()
        users = []
        for game in games:
            user = User.query(game.user == User.key).get()
            if user not in users:
                users.append(user)


        for user in users:
            subject = 'This is a hangman reminder!'
            body = 'Hello {}, you have pending games on + \
            Hangman!'.format(user.name)
            # This will send test emails, the arguments to send_mail are:
            # from, to, subject, body
            mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                           user.email,
                           subject,
                           body)

app = webapp2.WSGIApplication([
    ('/crons/send_reminder', SendReminderEmail),
], debug=True)
