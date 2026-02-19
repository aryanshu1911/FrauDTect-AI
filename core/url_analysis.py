import requests
import socket
import time
from urllib.parse import urlparse
from datetime import datetime
import whois
import os
from dotenv import load_dotenv

load_dotenv()

VT_API_KEY = os.getenv("VT_API_Key")
URLSCAN_API_KEY = os.getenv("URLSCAN_API_Key")


# ===============================
# URL NORMALIZATION
# ===============================
def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url.strip()


# ===============================
# DOMAIN EXTRACTION
# ===============================
def extract_domain(url: str) -> str:
    parsed = urlparse(url)
    return (parsed.netloc or parsed.path).lower().strip()


# ===============================
# DNS RESOLUTION
# ===============================
def resolve_domain(domain: str):
    try:
        socket.gethostbyname(domain)
        return True, "Domain resolves correctly"
    except Exception as e:
        return False, f"DNS resolution failed: {str(e)[:80]}"


# ===============================
# WHOIS AGE (VERY ROBUST)
# ===============================
def get_domain_age(domain: str):
    try:
        w = whois.whois(domain)

        creation_date = w.creation_date
        expiration_date = w.expiration_date
        registrar = w.registrar

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        if not creation_date:
            return None, {
                "error": "WHOIS did not return creation date"
            }

        if isinstance(creation_date, datetime):
            age_days = (datetime.utcnow() - creation_date).days

            return age_days, {
                "age_days": age_days,
                "creation_date": str(creation_date.date()),
                "expiration_date": str(expiration_date.date()) if expiration_date else "Unknown",
                "registrar": registrar if registrar else "Unknown"
            }

        return None, {"error": "Unsupported WHOIS format"}

    except Exception as e:
        return None, {"error": f"WHOIS lookup failed: {str(e)[:120]}"}


# ===============================
# VIRUSTOTAL
# ===============================
def check_virustotal(url: str):
    if not VT_API_KEY:
        return {"error": "VT API key missing"}

    try:
        headers = {"x-apikey": VT_API_KEY}

        resp = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url},
            timeout=20,
        )

        if resp.status_code != 200:
            return {"error": f"VT submit failed: {resp.status_code}"}

        analysis_id = resp.json()["data"]["id"]

        time.sleep(3)

        report = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers,
            timeout=20,
        )

        if report.status_code != 200:
            return {"error": f"VT fetch failed: {report.status_code}"}

        stats = report.json()["data"]["attributes"]["stats"]

        return {
            "stats": stats,
            "link": f"https://www.virustotal.com/gui/url/{analysis_id}/detection",
        }

    except Exception as e:
        return {"error": f"VT error: {e}"}


# ===============================
# URLSCAN (HARDENED)
# ===============================
def check_urlscan(url: str):
    if not URLSCAN_API_KEY:
        return {"error": "URLScan API key missing"}

    try:
        url = normalize_url(url)

        headers = {
            "API-Key": URLSCAN_API_KEY,
            "Content-Type": "application/json",
        }

        payload = {
            "url": url,
            "visibility": "public",
        }

        resp = requests.post(
            "https://urlscan.io/api/v1/scan/",
            headers=headers,
            json=payload,
            timeout=30,
        )

        if resp.status_code not in (200, 201):
            return {
                "error": f"URLScan failed: {resp.status_code}",
                "hint": "Possible causes: key not activated, rate limit, or duplicate scan",
                "raw": resp.text[:200],
            }

        data = resp.json()

        return {
            "result": data.get("result"),
            "scan_id": data.get("uuid"),
        }

    except Exception as e:
        return {"error": f"URLScan error: {e}"}


# ===============================
# 🧠 EXPLANATION ENGINE
# ===============================
def build_explanation(reasons, score, age_days):
    explanation = []

    if reasons:
        explanation.append("Risk factors detected:")
        explanation.extend([f"• {r}" for r in reasons])
    else:
        explanation.append("No major red flags detected.")

    if isinstance(age_days, int):
        if age_days < 30:
            explanation.append(
                "⚠️ Newly registered domains are frequently used in phishing attacks."
            )

    explanation.append(f"Final risk score: {score}/100")

    return "\n".join(explanation)


# ===============================
# MAIN ANALYZER
# ===============================
def analyze_url(url: str, deep_scan: bool = False):
    url = normalize_url(url)
    domain = extract_domain(url)

    risk_score = 0
    reasons = []
    osint_data = {}

    # ---------------- DNS ----------------
    resolves, dns_msg = resolve_domain(domain)
    if not resolves:
        risk_score += 40
        reasons.append("Domain failed DNS resolution")

    # ---------------- TLD ----------------
    suspicious_tlds = [".vip", ".xyz", ".top", ".club", ".online"]
    if any(domain.endswith(tld) for tld in suspicious_tlds):
        risk_score += 25
        reasons.append("Suspicious TLD commonly abused in scams")

    # ---------------- LENGTH ----------------
    if len(domain) > 30:
        risk_score += 10
        reasons.append("Unusually long domain")

    # ---------------- WHOIS ----------------
    age_days, whois_data = get_domain_age(domain)

    if isinstance(age_days, int):
        if age_days < 30:
            risk_score += 35
            reasons.append(f"Very new domain ({age_days} days old)")
        elif age_days < 90:
            risk_score += 15
            reasons.append(f"Recently registered domain ({age_days} days old)")
    else:
        if isinstance(whois_data, dict) and whois_data.get("error"):
            reasons.append(whois_data["error"])

    # ---------------- DEEP SCAN ----------------
    if deep_scan:
        vt_data = check_virustotal(url)
        urlscan_data = check_urlscan(url)

        osint_data["virustotal"] = vt_data
        osint_data["urlscan"] = urlscan_data

        try:
            malicious = vt_data.get("stats", {}).get("malicious", 0)
            if malicious > 0:
                risk_score += min(50, malicious * 5)
                reasons.append("Flagged by VirusTotal engines")
        except Exception:
            pass

    # ---------------- SCORE ----------------
    risk_score = int(min(100, max(0, risk_score)))

    if risk_score >= 70:
        verdict = "🔴 MALICIOUS"
    elif risk_score >= 40:
        verdict = "🟠 SUSPICIOUS"
    else:
        verdict = "🟢 LEGITIMATE"

    explanation = build_explanation(reasons, risk_score, age_days)

    return {
        "url": url,
        "domain": domain,
        "risk_score": risk_score,
        "verdict": verdict,
        "reasons": reasons,
        "explanation": explanation,
        "domain_age_days": age_days,
        "whois_data": whois_data,
        "dns_status": dns_msg,
        "osint": osint_data,
    }
