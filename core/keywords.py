keyword_weights = {

    # -------------------------------
    # 💰 Financial & Investment Lures
    # -------------------------------
    "investment": 3,
    "lottery": 6,
    "prize": 5,
    "claim": 5,
    "free gift": 5,
    "forex": 4,
    "bitcoin": 6,
    "crypto": 6,
    "profit": 4,
    "returns": 4,
    "roi": 4,
    "double your money": 7,
    "passive income": 5,
    "risk free": 5,
    "guarantee": 5,
    "earn": 3,
    "bonus": 3,
    "airdrop": 5,
    "presale": 5,
    "prelaunch": 5,
    "staking": 4,
    "mint now": 5,

    # -------------------------------
    # 💳 Banking / Payment Fraud
    # -------------------------------
    "bank account": 6,
    "upi": 5,
    "upi id": 5,
    "transfer money": 6,
    "send money": 6,
    "wire transfer": 5,
    "payment": 5,
    "deposit": 3,
    "withdraw": 3,
    "amount": 4,

    # -------------------------------
    # ⚠ Urgency & Manipulation
    # -------------------------------
    "urgent": 4,
    "hurry": 3,
    "limited time": 4,
    "limited offer": 4,
    "act fast": 5,
    "last chance": 5,
    "immediately": 4,
    "exclusive offer": 4,
    "don’t miss": 4,
    "ending soon": 4,

    # -------------------------------
    # 🔐 Phishing / Account Takeover
    # -------------------------------
    "verify": 5,
    "verify your account": 6,
    "account": 3,
    "security alert": 6,
    "unauthorized": 5,
    "unauthorized access": 6,
    "password": 6,
    "password reset": 6,
    "otp": 6,
    "login": 4,
    "reset": 4,
    "suspend": 5,
    "account suspended": 5,
    "account compromised": 6,
    "credentials": 5,

    # -------------------------------
    # 🧾 Identity Fraud
    # -------------------------------
    "government id": 6,
    "pan card": 5,
    "aadhaar": 5,
    "passport": 5,
    "social security": 6,
    "bank details": 6,
    "kyc": 4,
    "compliance team": 4,

    # -------------------------------
    # 📎 Link / Contact Manipulation
    # -------------------------------
    "click link": 6,
    "click here": 6,
    "open attachment": 6,
    "call now": 4,
    "join telegram": 3,
    "whatsapp support": 3,
    "chat with agent": 3,

    # -------------------------------
    # 🪙 Crypto / Web3 Exploits
    # -------------------------------
    "metamask": 6,
    "wallet drain": 7,
    "private key": 7,
    "seed phrase": 7,
    "contract": 3,
    "nft drop": 5,

    # -------------------------------
    # 🧑‍💼 Impersonation & Fake Authority
    # -------------------------------
    "official": 3,
    "government grant": 6,
    "elon musk": 6,
    "ai robot": 5,
    "trading bot": 6,

    # -------------------------------
    # 🚨 General Scam Indicators
    # -------------------------------
    "scam": 6,
    "fake": 5,
    "fraud": 6,
    "hack": 6,
    "compromised": 5,
    "phishing": 6,
    "malicious": 5,
    "clone site": 6
}

# ==========================================================
# URL KEYWORD WEIGHTS
# ==========================================================

url_keyword_weights = {

    # Authentication traps
    "login": 10,
    "verify": 9,
    "reset": 9,
    "unlock": 9,
    "account": 8,
    "wallet": 10,
    "auth": 8,
    "2fa": 8,

    # Crypto traps
    "crypto": 9,
    "binance": 10,
    "metamask": 10,
    "investment": 9,
    "airdrop": 8,
    "giveaway": 10,
    "profit": 7,

    # Support impersonation
    "support": 7,
    "recovery": 7,
    "security": 7,
    "update": 6,

    # Suspicious TLDs
    ".vip": 10,
    ".xyz": 9,
    ".top": 9,
    ".live": 8,
    ".club": 7,
    ".cam": 9,
    ".cfd": 9,
    ".app": 5
}

# ==========================================================
# SCAM CATEGORIES
# ==========================================================

scam_categories = {

    "Financial Scam": [
        "investment", "lottery", "profit", "returns",
        "roi", "double your money", "passive income"
    ],

    "Crypto Scam": [
        "crypto", "bitcoin", "wallet drain",
        "seed phrase", "private key", "metamask",
        "airdrop", "nft drop"
    ],

    "Banking / Payment Fraud": [
        "bank account", "upi", "transfer money",
        "wire transfer", "payment"
    ],

    "Phishing / Account Takeover": [
        "verify", "login", "password",
        "otp", "account suspended",
        "security alert"
    ],

    "Urgency Manipulation": [
        "urgent", "act fast", "limited time",
        "last chance", "immediately"
    ]
}
