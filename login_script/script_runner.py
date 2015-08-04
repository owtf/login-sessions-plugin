#!/usr/bin/python3
import os
import sys
import base64
import uuid
import json
import re
import logging
import argparse
from urllib.request import urlopen, Request
from selenium import webdriver


#DIR SETUP
ROOT_DIR = os.path.abspath(sys.argv[0])
LOG_DIR = os.path.abspath(os.path.join(ROOT_DIR, '..', '/logs/'))
SCRIPT_DIR = os.path.abspath(os.path.join(ROOT_DIR, '..', '/scripts/'))

# basic logging setup
logger = logging.getLogger("script generator")
logger.setLevel(logging.ERROR)

#filehandler
#filelog = logging.FileHandler(log_path)
#filelog.setLevel(logging.DEBUG)

# console logging
console = logging.StreamHandler()
console.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#filelog.setFormatter(formatter)
console.setFormatter(formatter)

# add the handlers to the logger
#logger.addHandler(filelog)
logger.addHandler(console)


# get the conf options for PhantomJS
with open("conf.json", "r") as config:
    conf = json.load(config)


# get a UUID - URL safe, Base64
def get_uuid():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return r_uuid.replace('=', '')


# get name of the script and store it in SCRIPT var
script_name = sys.argv[1]


AUTO_LOGIN_STATUSES  = {
    "ok": 'Form submitted successfully.',
    "form_not_found": 'Could not find a form suiting the provided parameters.',
    "form_not_visible": """The form was located but its DOM element is not
                              'visible and thus cannot be submitted.""",
    "check_failed": 'Form submitted but the response did not match the verifier.'
}

LOGIN_SCRIPT_STATUSES  = {
    "success": 'Login was successful.',
    "failure": 'The script was executed successfully, but the login check failed.',
    "error": 'A runtime error was encountered while executing the login script.',
    "missing_browser": 'A browser is required for this operation but is not available.',
    "missing_check": 'No session check was provided, either via interface options or the script.'
}


# args parsing here
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target","-t",
        dest="target",
        default=None,
        help="the target for auto-login")
    parser.add_argument(
        "parameters", "-p",
        dest="parameters",
        default=None,
        help="The username/password for the login form")
    parser.add_argument(
        "check", "-c",
        dest="check",
        default=None,
        help="Python regex/string to check for successful login")

    return parser.parse_args()


class LoginScript(object):

    def __init__(self, script_name=None):
        # check if cli args are present or not
        if sys.argv[1:]:
            # present
            self.cli_options = parse_args()
            self.check_pattern = cli_options["check"]
        else:
            if script:
                self.script = script_name
                self.check_pattern = conf["check_pattern"]
            else:
                logger.error("No script specified! Exiting....")
                sys.exit(-1)
        self.browser = self.prep()
        self.id = get_uuid()

    def prep(self):
        try:
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
        except WebDriverException:
            logger.critical("Cannot load the browser instance")

    def auto_login_cmd():
        # the support is still rudimentry
        target = self.cli_options["target"]
        # this is the url-encoded data
        # too much variety for us to handle different input tag names :/
        parameters = self.cli_options["parameters"]

        handler = urllib.HTTPHandler()
        # create an openerdirector instance
        opener = urllib.build_opener(handler)
        # build a request
        request = urllib.Request(target, data=parameters)
        # add appr content headers
        request.add_header("Content-Type",'application/x-www-form-urlencoded')
        request.get_method = 'POST'

        try:
            conn = opener.open(request)
        except urllib.HTTPError as e:
            conn = e

        if conn.code == 200:
            page_src = conn.read()
        else:
            sys.exit("Auto_login failed!")

        if page_src:
            # check for login successful pattern
            match = re.search(self.check_pattern, page_src)
            if match:
                print("Login successful")
            else:
                print("login unsuccessful!")

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
            print(LOGIN_SCRIPT_STATUSES["success"])
            logger.success(LOGIN_SCRIPT_STATUSES["success"])
        else:
            print(LOGIN_SCRIPT_STATUSES["failure"])
            logger.warn(LOGIN_SCRIPT_STATUSES["failure"])

    def teardown(self):
        """
        cleanup process after the login script is played

        """
        # first close the driver
        self.browser.quit()

