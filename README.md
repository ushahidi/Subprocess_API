# Subprocess API

## Description

* Standalone Python script that runs a basic HTTP server based on Python's [BaseHTTPServer](http://docs.python.org/library/basehttpserver.html).
* Provides a REST+JSON API into the Python [Subprocess](http://docs.python.org/library/subprocess.html) module.
* Uses only the Python standard library and no additional third party packages.
* Tested with Python 2.7 but might work on other Python 2.x versions.
* Released under the [GNU GPL](http://www.gnu.org/copyleft/gpl.html).
* Supported by the [SwiftRiver](http://groups.google.com/group/swiftriver) team.

## Running

    wget https://raw.github.com/ushahidi/Subprocess_API/master/subprocess_api.py
    python subprocess_api.py

This will run the HTTP server localhost port 8000 by default. If you would like to customise this, change the `HOST` and `PORT` settings at the top of the script.

## Security

This script was written to be used inside a fully trusted environment (including the client, the server and the network). Running this in an untrusted environment is not recommended.

## Request

The request needs to be an HTTP POST with the request body being a JSON object with the following attributes:

* `args` Required string or array
* `stdin` Optional string
* `shell` Optional boolean

For more details on the use of the above, please consult the [`subprocess.call` documentation on python.org](http://docs.python.org/library/subprocess.html#subprocess.call).

## Response

A successful response will have an HTTP code of 200 and an error response will have an HTTP code of 500. In either case, the `Content-Type` will be set to `application/json` and the response body will be a JSON object.

### Success

The returned JSON object will have the following attributes on a successful call:

* `returncode` The return code of the executed command as an integer.
* `stdout` The contents of the stdout stream as a string.
* `stderr` The contents of the stderr stream as a string.

### Error

The returned JSON object will have the following attributes on an unsuccessful call:

* `error` The full Python stack trace of the error.

## Example

    $ curl -d '{"args":["ls","/"]}' localhost:8000
    {"returncode": 0, "stderr": "", "stdout": "bin\nboot\ncdrom\ndev\netc\nhome\ninitrd.img\nlib\nlib32\nlib64\nlost+found\nmedia\nmnt\nopt\nproc\nroot\nrun\nsbin\nselinux\nsrv\nsys\ntmp\nusr\nvar\nvmlinuz\n"}
