#
#   config - provide various configuration settings
#

import configparser
import os
import sys
import json

config = configparser.ConfigParser()
config_dir = os.path.expanduser('~/.phishbuckets/')
full_path = config_dir + 'config'

try:
    config.read(full_path)
    key_itself = json.loads(config.get("Global", "GOPHISH_KEY"))
    GOPHISH_KEY = {'api_key': key_itself}
except:
    sys.exit(
        "\n[Error]: 'GOPHISH_KEY' not found.\n"
        "\n   The script expects the API key to be stored"
        "\n   in the file: ~/.phishbuckets/config "
        "\n"
    )

try:
    config.read(full_path)
    EMAIL_FROM = json.loads(config.get("Global", "FROM"))
except:
    sys.exit(
        "\n[Error]: 'FROM' not found.\n"
        "\n   The script expects the 'FROM' value to be stored "
        "\n   in the file: ~/.phishbuckets/config "
        "\n"
    )

try:
    config.read(full_path)
    PHISH_MASTER = json.loads(config.get("Global", "PHISH_MASTER"))
except:
    sys.exit(
        "\n[Error]: 'PHISH_MASTER' not found.\n"
        "\n   The script expects the email address of the 'phish_master' to be"
        "\n   in the file: ~/.phishbuckets/config "
        "\n"
    )

try:
    config.read(full_path)
    URL = json.loads(config.get("Global", "GOPHISH_SERVER_URL"))
except:
    sys.exit(
        "\n[Error]: 'GOPHISH_SERVER_URL' not found.\n"
        "\n   The script expects the gophish server url to be stored "
        "\n   in the file: ~/.phishbuckets/config "
        "\n"
    )
