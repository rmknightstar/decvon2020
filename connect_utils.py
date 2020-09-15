import requests
import time
import sys
import json
import base64


def value_chaining(first_val, second_val):
    return first_val if first_val != None else second_val


def plog(msg, to_stderr=True):
    pstream = sys.stderr if to_stderr else sys.stdout
    pstream.write(time.strftime('%Y-%m-%d %X') + ": " + unicode(msg) + "\n")
    pstream.flush()


# TODO add log levels
def dplog(msg, enabled, to_stderr=True):
    if enabled:
        plog(msg, to_stderr=to_stderr)


def make_auth_header(username, password):
    return {"Authorization": "Basic " + base64.b64encode(username + ":" + password)}


def build_params(params):
    retval = ""
    first_one = True
    if params != None:
        for pname in params:
            param = params[pname]
            if not first_one:
                retval += "&"
            else:
                first_one = False
            retval += pname + "=" + param
    return retval


class SmartConnection:
    def __init__(self, auth_headers, debug=False, logging=False):
        self.auth_headers = auth_headers
        self.last_status = None
        self.debug = debug
        self.logging = logging

    def smart_post(self, url, json_data):
        if self.debug:
            dplog("Submiting " + url, self.logging)
            jout = {}

        else:
            dplog("Submiting " + url, self.logging)
            dplog("Submiting " + json.dumps(json_data, 2), self.logging)
            headers = {"Content-Type": "application/json; charset=utf-8", "Accept": 'application/json' }
            headers.update(self.auth_headers)
            resp = requests.post(url, headers=headers, verify=False, json=json_data)
            self.last_status = resp.status_code
            try:
                jout = resp.json()
            except:
                plog(resp)
                jout = {}

            dplog(url, self.logging)
            dplog(resp, self.logging)

        return jout

    def raw_put(self, url, data, contentType="application/octet-stream; charset=utf-8"):
        if self.debug:
            dplog("Submiting " + url, self.logging)
            jout = {}

        else:
            dplog("Submiting " + url, self.logging)
            headers = {"Content-Type": contentType, "Accept": 'application/json' }
            headers.update(self.auth_headers)
            resp = requests.put(url, headers=headers, verify=False, data=data.encode("utf-8"))
            self.last_status = resp.status_code
            try:
                jout = resp.json()
            except:
                jout = {}

            dplog(url, self.logging)
            dplog(resp, self.logging)

        return jout

    def smart_get(self, url):
        resp = requests.get(url, headers=self.auth_headers)
        self.last_status = resp.status_code
        return resp.json()

    def raw_get(self, url):
        # self.last_status = resp.status_code
        return requests.get(url, headers=self.auth_headers)
