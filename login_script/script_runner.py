#!/usr/bin/python3
"""
:synopsis: Defines the script runner which accepts either CLI args or a script name.
The script does the authentication for the user.
.. moduleauthor:: Viyat Bhalodia
"""
import os
import sys
import base64
import binascii
import json
import re
import logging
import argparse
from urllib.request import urlopen, Request
from selenium import webdriver


#DIR SETUP
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
LOG_DIR = os.path.abspath(os.path.join(ROOT_DIR, 'logs'))
SCRIPT_DIR = os.path.abspath(os.path.join(ROOT_DIR, 'scripts'))

# basic logging setup
logger = logging.getLogger("script generator")
logger.setLevel(logging.ERROR)


# console logging
console = logging.StreamHandler()
console.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(console)


# get the conf options for PhantomJS
with open("conf.json", "r") as config:
    conf = json.load(config)

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
        "--script","-s",
        dest="script",
        default=None,
        help="the script name")
    parser.add_argument(
        "--target","-t",
        dest="target",
        default=None,
        help="the target for auto-login")
    parser.add_argument(
        "--parameters", "-p",
        dest="parameters",
        default=None,
        help="The username/password for the login form")
    parser.add_argument(
        "--check", "-c",
        dest="check",
        default=None,
        help="Python regex/string to check for successful login")

    return parser.parse_args()


class LoginScript(object):
    """
    .. note::
        This defines the main Login script runner. This will be imported into OWTF for further integration

    """
    def __init__(self):
        """Initialize :class:`LoginScript`.

        :param str script_name: Name of the authentication script.

        """
        # : :class: `type` -- Checks if CLI args are present or not
        self.cli_options = parse_args()
        if self.cli_options.script:
            #: :class: `str` -- Script name
            self.script = self.cli_options.script
            #: :class: `str` -- Login sequence check
            self.check_pattern = conf["check_pattern"]
        else:
            self.check_pattern = self.cli_options.check
        #: :class: `type` -- The PhantomJS browser instance
        self.browser = self.prep()
        #: :class: `type` -- A very simple random token generator
        self.id = binascii.hexlify(os.urandom(1000))

    @staticmethod
    def prep():
        """Uses the config parameters to initialise a PhantomJS instance.
        :return: A Selenium PhantomJS browser instance
        :rtype: object
        :raises: :class:`WebDriverException`.
        """
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

    def auto_login_cmd(self):
        """Tries to authenticate the user via the parameters provided."""
        # the support is still rudimentry
        target = self.cli_options.target
        # this is the url-encoded data
        # too much variety for us to handle different input tag names :/
        parameters = self.cli_options.parameters

        handler = urllib.HTTPHandler()
        # create an openerdirector instance
        opener = urllib.build_opener(handler)
        # build a request
        request = urllib.Request(target, data=parameters)
        # add appropriate content headers
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
        """Runs the actual authentication script"""
        with open(os.path.join(SCRIPT_DIR, self.script), "r") as file:
            script = file.read()
        #: :class: `type` -- The browser instance
        browser = self.browser

        # Magic: run the login script using the above browser instance
        exec(script, globals())

        source = browser.page_source

        # check for login sequence
        match = re.search(self.check_pattern, source)
        if match:
            logger.success(LOGIN_SCRIPT_STATUSES["success"])
        else:
            logger.warn(LOGIN_SCRIPT_STATUSES["failure"])

    def teardown(self):
        """Cleanup process after the login script is played """
        # close the driver
        self.browser.quit()


if __name__ == "__main__":
    login_obj = LoginScript()
    if login_obj.script:
        login_obj.run()
    else:
        login_obj.auto_login_cmd()
    login_obj.teardown()
    print("Login sequence successful")

