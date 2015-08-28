"""
The idea is to capture the session tokens from a set such as given below, and match the token name.
If it matches, successfully mark it as a HTTP session and store it in the DB.
The reasoning behind marking the session + the response/request is to authenticate using the same message
at a later time.

This needs to be implemented as a proxy plugin.
"""

# CONSTANTS
DEFAULT_TOKENS = [ "asp.net_sessionid", "aspsessionid", "siteserver", "cfid",
                  "cftoken", "jsessionid", "phpsessid", "sessid", "sid", "viewstate", "zenid" ]

