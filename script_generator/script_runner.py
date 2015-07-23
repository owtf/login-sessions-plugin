#!/usr/bin/python3
import os
import sys
import base64
import uuid
import json
import re
from selenium import webdriver


ROOT_DIR = os.path.dirname(sys.argv[0])
LOG_DIR = os.path.abspath(os.path.join(ROOT_DIR, '..', '/logs/'))
SCRIPT_DIR = os.path.abspath(os.path.join(ROOT_DIR, '..', '/scripts/'))

# get the conf options for PhantomJS
with open("conf.json", "r") as config:
    conf = json.load(config)

#print(conf)

# get a UUID - URL safe, Base64
def get_uuid():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return r_uuid.replace('=', '')


# get name of the script and store it in SCRIPT var
script_name = sys.argv[1]


STATUSES  = {
    "success": 'Login was successful.',
    "failure": 'The script was executed successfully, but the login check failed.',
    "error": 'A runtime error was encountered while executing the login script.',
    "missing_browser": 'A browser is required for this operation but is not available.',
    "missing_check": 'No session check was provided, either via interface options or the script.'
}


class LoginScript(object):

    def __init__(self, script_name=None):
        
        if script:
            self.script = script_name
        else:
            print("No script specified! Exiting....")
            sys.exit(-1)
        self.check_pattern = conf["check_pattern"]
        self.browser = self.prep()
        self.id = get_uuid()

    def prep(self):
        return webdriver.PhantomJS(
            service_args=[
                '--ignore-ssl-errors=true',
                '--proxy='+conf["proxy"],
                '--proxy-type=http',
                '--disk-cache=true',
                '--debug='+conf["debug"]
            ],
            service_log_path=LOG_DIR
        )

    def run(self):
        with open(os.path.join(SCRIPT_DIR, script_name), "r") as file:
            script = file.read()

        browser = self.browser

        # run the login script using the above browser instance
        exec(script, globals())

        source = browser.page_source

        # check for login sequence
        match = re.search(self.check_pattern, source)
        if match:
            print(STATUSES["success"])
        else:
            print(STATUSES["failure"])

