#!/usr/bin/python3
import shortuuid



class HTTPSession(object):
    """
    defines a user session

    """

    def __init__(self, name, active=False, valid=True, msgs_matched, \
                 token_vals, token_names):
        # token_vals is a dict
        # token_names is a list of session token names
        self.name = shortuuid.uuid()
        self.active = active
        self.valid = valid
        self.msgs_matched = msgs_matched
        self.token_vals = token_vals
        self.token_names = token_names


    def set_token_value(self, token_name, value=None):
        # check the value
        if not value:
            self.token_vals[token_name]
        # get the current value of the token
        val = self.token_vals[token_name]
        if val:
            self.token_vals[token_name] = value
        else:
            self.token_vals[token_name] = None

    def matches_token(self,token_name, value):
        # check if value is null
        if not value:
            return True if token_name in self.token_vals else False

        val = self.token_vals[token_name]
        if val and val == value:
            return True
        else:
            return False

    def get_token_value(self, token_name):
        return self.token_vals[token_name]

    def remove_token(self, token_name):
        return self.token_vals.pop(token_name, None)

    def count(self):
        return len([k for (k, v) in self.token_vals.iteritems()])

    def token_val_string(self):
        if not self.token_vals:
            return("")
        token_string = ""
        for key in self.token_vals:
            token_string += key+ " = "+ self.token_vals[key]
        return token_string

    def __str__(self):

        return "HTTPSession [name=%s, active=%s, tokenvalues=%s]" % ( self.name, \
                                                                      self.active,\
                                                                      self.token_val_string()
                                                                    )


class SessionManager(object):
    """
    simple API for managing multiple HTTPsessions
    for a target
    1 session manager obj for one target

    """
    def __init__(self, sessions=None, target):
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
                self.sessions.remove(httpsession)
            else:
                print("No such session")

