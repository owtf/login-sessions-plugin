##owtf auto-login and script runner

This is the home of the auto-login and login-script runner plugins for OWTF.
OWTF framework needs to authenticate the user to cover a larger vunerable attack surface. To do this, there are 2 approaches:

- `Auto-login` :
  The auto-login script uses CLI arguments to authenticate the user with form parameters and offers additional check to see if the user is successfully logged in or not.

  ```
  usage: script_runner.py [-h] [--script SCRIPT] [--target TARGET]
                        [--parameters PARAMETERS] [--check CHECK]

  optional arguments:
    -h, --help          show this help message and exit
    --script SCRIPT, -s SCRIPT
                        the script name
    --target TARGET, -t TARGET
                        the target for auto-login
    --parameters PARAMETERS, -p PARAMETERS
                        The username/password for the login form
    --check CHECK, -c CHECK
                        Python regex/string to check for successful login
    ```

- `login-script` :
This method provides for more flexibility to the user to define custom/complex authentication sequences using a PhantomJS browser instance

## Usage

To use the `auto-login` functionality, pass target, parameters in a URL encoded form, and a check for the successful login. This can be either a regex or a simple string.

For the script-based method,
* Create a login script to authenticate the user to the target using the PhantomJS `browser` instance in the `scripts/` directory.
* Define your config in `conf.json` file. A sample has been provided, `conf.json.sample`.
* Pass the script name to the plugin on the commandline.

