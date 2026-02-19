import requests
import base64
import time
import os
from dotenv import load_dotenv

load_dotenv()

virustotal_key = os.getenv("VirusTotal_API_Key")

def scan_url_virustotal(url):
    headers = {
        "x-apikey": virustotal_key
    }

    try:
        # Step 1: Submit the URL for scanning
        submit_response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url}
        )

        if submit_response.status_code != 200:
            return {"error": f"Submission failed: {submit_response.status_code} {submit_response.text}"}

        # Step 2: Encode the URL to base64 (URL-safe, no padding)
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

        # Step 3: Wait for scan results to be processed
        time.sleep(6)

        # Step 4: Fetch the analysis report
        report_response = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers=headers
        )

        if report_response.status_code != 200:
            return {"error": f"Analysis failed: {report_response.status_code} {report_response.text}"}

        result = report_response.json()
        attributes = result["data"]["attributes"]
        stats = attributes["last_analysis_stats"]

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        harmless = stats.get("harmless", 0)
        undetected = stats.get("undetected", 0)
        timeout = stats.get("timeout", 0)
        total = sum(stats.values())

        # Optional: get individual engine results
        engines = attributes.get("last_analysis_results", {})

        return {
            "Submitted URL": url,
            "Malicious Detections": malicious,
            "Suspicious Detections": suspicious,
            "Harmless": harmless,
            "Undetected": undetected,
            "Timeout": timeout,
            "Total Engines Checked": total,
            "Verdict": "⚠️ Suspicious or Malicious" if malicious or suspicious else "✅ Clean",
            "Detailed Report URL": f"https://www.virustotal.com/gui/url/{url_id}/detection"
        }

    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}
