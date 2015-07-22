#!/usr/bin/python3
import os
import sys
from selenium import webdriver
import yaml

LOG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../logs/")

with open("config.yml", "r") as conf:
    config = yaml.load(conf)

def load_driver(**options):
    ops = **options
    browser = webdriver.PhantomJS(
        service_log_path=LOG_DIR
    )
    # by default cookies are enabled
    # and maintains a cookiejar

    return browser


def gen_script(config):
    login_url = config["url"]
    fields = config["form"]
    options = config["options"]



