import json
import sys
import requests
import os
import getopt
import base64
import connect_utils
import urllib

AUDIT_APPLICATIONS_URL_SEGMENT="api/-default-/public/alfresco/versions/1/audit-applications/"
AUDIT_ENTRIES_URL_SEGMENT="/audit-entries"
config = { 
   "url": "http://127.0.0.1:8080/alfresco/",
    "username": "admin",
    "password": "admin",
    "debug":False
}

def get_audit_entries(conn,audit_application,from_id, to_id, include_values=True,skipCount=0,maxItems=100):
    where_clause="(id BETWEEN ('" + str(from_id) + "', '" + str(to_id) + "'))"
    params = {
        "skipCount": str(skipCount),
        "maxItems": str(maxItems),
        "where": urllib.quote(where_clause)
    }
    if include_values:
        params["include"] = "values"

    url = config["url"] + AUDIT_APPLICATIONS_URL_SEGMENT + audit_application + AUDIT_ENTRIES_URL_SEGMENT + "?" + connect_utils.build_params(params)

    return conn.smart_get(url)


include_values=True
skip=0
max_count=100
from_id=0
to_id=2000000000
audit_app = "RM"

optlist, args = getopt.gnu_getopt(sys.argv, "f:t:s:m:q",
                                  ["from=", "to=", "skip=", "max=","quiet"])
from_args = dict()
debug = False
for opt, val in optlist:
    if opt in ("-q", "--quiet"):
        include_values = False
    elif opt in ("-f", "--from"):
        from_id = val
    elif opt in ("-t", "--to"):
        to_id = val
    elif opt in ("-m", "--max"):
        max_count = val
    elif opt in ("-s", "--skip"):
        skip = val
    elif opt in ("-a", "--app"):
        audit_app = val


conn = connect_utils.SmartConnection(connect_utils.make_auth_header(config["username"],config["password"]), logging=config["debug"])


json.dump(get_audit_entries(conn,audit_app,from_id,to_id,skipCount=skip,maxItems=max_count,include_values=include_values), sys.stdout, indent=2)