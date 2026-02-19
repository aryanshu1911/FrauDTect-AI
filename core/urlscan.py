import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()

urlscan_key = os.getenv("URLSCAN_API_Key")

def scan_url_with_urlscan(url):
    headers = {
        "API-Key": urlscan_key,
        "Content-Type": "application/json"
    }

    payload = {
        "url": url,
        "visibility": "public"
    }

    try:
        # Step 1: Submit URL
        response = requests.post("https://urlscan.io/api/v1/scan/", headers=headers, json=payload)

        if response.status_code != 200:
            return {"error": f"Scan submission failed: {response.status_code} {response.text}"}

        data = response.json()
        uuid = data.get("uuid")

        if not uuid:
            return {"error": "Scan submission succeeded but UUID not returned."}

        # Step 2: Poll for result
        result_data = None
        for attempt in range(6):  # Try for ~30 seconds
            time.sleep(5)
            result = requests.get(f"https://urlscan.io/api/v1/result/{uuid}/", headers=headers)

            if result.status_code == 200:
                result_data = result.json()
                break
            elif result.status_code == 404:
                continue  # Scan not ready yet
            else:
                return {"error": f"Unexpected error: {result.status_code} {result.text}"}

        if not result_data:
            return {"error": "Scan is taking too long or failed."}

        # Step 3: Extract relevant info
        return {
            "Message": "✅ Scan Successful",
            "Scanned URL": result_data["page"]["url"],
            "Domain": result_data["page"].get("domain", "N/A"),
            "IP": result_data["page"].get("ip", "N/A"),
            "Country": result_data["page"].get("country", "N/A"),
            "Verdict Score": result_data.get("verdicts", {}).get("overall", {}).get("score", "N/A"),
            "Screenshot URL": result_data.get("screenshot", "N/A"),
            "Full Report URL": result_data["task"].get("reportURL", f"https://urlscan.io/result/{uuid}/")
        }

    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}
