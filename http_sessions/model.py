#!/usr/bin/python3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Boolean


# CONSTANTS
DEFAULT_TOKENS = [ "asp.net_sessionid", "aspsessionid", "siteserver", "cfid",
			"cftoken", "jsessionid", "phpsessid", "sessid", "sid", "viewstate", "zenid" ]

Base = declarative_base()


class HTTPSessions(Base):
    __tablename__ == "http_sessions"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Boolean)
    valid = Column(Boolean)
    token_vals = Column(String)
    token_names = Column(String)

    def __str__(self):
        return name

