#!/usr/bin/python3
from cookies import Cookie
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Table, Column, Integer, String, Boolean,\
            Float, DateTime, ForeignKey, Text
import json


# CONSTANTS
DEFAULT_TOKENS = [ "asp.net_sessionid", "aspsessionid", "siteserver", "cfid", \
			"cftoken", "jsessionid", "phpsessid", "sessid", "sid", "viewstate", "zenid" ]


Base = declarative_base()

class CookiesDB(Base):
    """
    mapping for storing cookies

    """
    __tablename__ = 'cookies'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    name = Column(String)
    expires = Column(Integer)
    value = Column(String)
    max_age = Column(Integer)
    domain = Column(String)
    path = Column(String)
    secure = Column(Boolean)
    httponly = Column(Boolean)
    other = Column(String)

    def __str__(self):
        return("Set-Cookie: %s; name=%s; expires=%s, path=%s, domain=%s, secure=%s; httpOnly=%s"
               % (value, name, str(expires), path, domain, secure, httponly)
        )


class OCookie(object):
    """
    This cookie jar implementation recieves cookies in a dict format
    and stores in an object
    + dump as json

    """

    def __init__(self, cookie):
        self.engine = create_engine('sqlite:///cookies.db', echo=True)
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.scoped_factory = scoped_session(self.session_factory)
        self.session = self.scoped_factory()

        # check if it is a string
        if type(cookie).__name__ == "string":
            self.cookiestring = self.parse(cookie)
        else:
            self.cookiestring = cookie

    def parse(self, cookie):
        return Cookie.from_dict(cookie, ignore_bad_attributes=True)

    def fetch(self, domain, is_session=False):
        return ""

    def store(self, domain, is_session):
        # check for session cookies
       return ""

    def jsonify(elf):

       return ""

    def dump(self):

    def clear(self):


    def clear_all_session_cookies(self):

    def load(self)
        """
        load cookies from a json file

        """



