#!/usr/bin/python3
import uuid
import base64


# get a UUID - URL safe, Base64
def get_uuid():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return r_uuid.replace('=', '')


class HTTPSession(object):
    """Defines a user session"""

    def __init__(self, name, active=False, valid=True, msgs_matched=None, token_vals=None, token_names=None):
        # token_vals is a dict
        # token_names is a list of session token names
        self.name = get_uuid()
        self.active = active
        self.valid = valid
        self.msgs_matched = msgs_matched
        self.token_vals = token_vals
        self.token_names = token_names


    def set_token_value(self, token_name, value=None):
        # check the value
        if not value:
            self.token_vals.pop(token_name, None)
        # get the current value of the token
        self.token_vals[token_name] = value or None

    def matches_token(self,token_name, value):
        # check if value is null
        if not value:
            return True if token_name in self.token_vals else False

        token = self.token_vals[token_name]
        if token and token == value:
            return True
        else:
            return False

    def get_token_value(self, token_name):
        return self.token_vals[token_name]

    def remove_token(self, token_name):
        return self.token_vals.pop(token_name, None)

    def count(self):
        # counts the net no of tokens - including nested ones
        return len([k for (k, v) in self.token_vals.items()])

    def token_val_string(self):
        if not self.token_vals:
            return ''
        return ''.join('%s = %s' % (key, value) for key, value in self.token_vals.items())

    def __str__(self):
        return "HTTPSession [name=%s, active=%s, tokenvalues=%s]" % ( self.name, self.active, self.token_val_string())


class SessionManager(object):
    """
    Simple API for managing multiple HTTPsessions
    for a target
    Usage:
        One session manager object for one target
        >> SessionManager([], google.com)
    """
    def __init__(self, sessions=None, target=None):
        self.target = target
        # sessions is a list of httpsessions objects
        self.sessions = sessions
        self.active_session = None

    def set_default(self, id):
        self.active_session = [session for session in self.sessions if session["name"] == id][0]

    def add_session(self, httpsession):
        # check if existing session exists
        for session in self.sessions:
            if not session["name"] == httpsession.id:
                self.sessions.append(httpsession)
            else:
                print("Error: Duplicate session")

    def remove_session(self, id):
        for session in self.sessions:
            if session["name"] == id:
                self.sessions.remove(session)
            else:
                print("No such session")

