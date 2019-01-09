
import datetime
import os
import requests
import re
import json

import util

def main():
    JST = datetime.timezone(datetime.timedelta(hours=+9), "JST")
    # TODO: Implement skipping Japanese holiday.
    if os.environ.get("SKIP_JP_HOLIDAY", False) and not util.is_weekday(datetime.datetime.now(JST)):
        print("Today is holiday. Skipped.")
        return False

    mail = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]
    mackerel_api_key = os.environ["MACKEREL_API_KEY"]
    service_url = os.environ["MACKEREL_SERVICE_URL"]

    try:
        browser = util.login(mail, password)
        shisan = util.fetch_folio_shisan(browser)
    except:
        return False

    requests.post(service_url, data=json.dumps([
        {
            "name": "Folio.soushisan",
            "time": datetime.datetime.now().timestamp(),
            "value": int(re.sub(r"\D", "", shisan["all_shisan"])),
        },
    ]), headers={
        "X-Api-Key": mackerel_api_key,
        "Content-Type": "application/json"
    })

    return True

if __name__ == "__main__":
    main()
    exit(0)

