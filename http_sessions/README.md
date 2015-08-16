## Improved session tracking framework plugin for OWTF

This was done during the OWASP Summer Code Sprint 2015

The main aim of this plugin is to mark the HTTP sessions for the target for vulnerability analysis and to cover a large attack surface.

* The basic ORM model for the plugin is provided in the `model.py` file.

* The actual API for managing the sessions is in the `session_manager.py`. This will be as a plugin to the OWTF mitm proxy


The actual spec for the proxy plugin architecture currently lives [here](https://github.com/owtf/reboot/issues/15).

