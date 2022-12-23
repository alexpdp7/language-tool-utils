import json
import urllib.parse
import urllib.request


def check(data, language, endpoint="http://localhost:8010", level="picky", disabled_rules=["WHITESPACE_RULE"]):
    with urllib.request.urlopen(f"{endpoint}/v2/check", urllib.parse.urlencode({
        "data" :json.dumps(data),
        "language": language,
        "level": level,
        "disabledRules": ",".join(disabled_rules),
    }).encode("ascii")) as r:
        return json.loads(r.read().decode("utf-8"))
