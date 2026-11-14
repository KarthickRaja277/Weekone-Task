import hashlib
import hmac
import os

from dotenv import load_dotenv

from src.api_client import fetch_users
from src.security import verify_signature


def main() -> None:
    load_dotenv()
    users = fetch_users()
    for user in users[:5]:
        print(f"{user.get('id')} - {user.get('name')} - {user.get('email')}")

    first = users[0] if users else {}
    address = first.get("address") or {}
    geo = address.get("geo") or {}
    company = first.get("company") or {}
    city = address.get("city", "Not Available")
    latitude = geo.get("lat", "Not Available")
    zip_code = address.get("zipcode", "Not Available")
    company_name = company.get("name", "Not Available")
    print(
        f"City: {city} | Latitude: {latitude} | Zip: {zip_code} "
        f"| Company: {company_name}"
    )

    secret = os.getenv("WEBHOOK_SECRET", "")
    payload = b'{"event":"employee.created","id":1}'
    valid_signature = hmac.new(
        secret.encode("utf-8"), payload, hashlib.sha256
    ).hexdigest()
    print(
        "Valid: "
        f"{verify_signature(payload, valid_signature, secret)} | "
        f"Tampered: "
        f"{verify_signature(payload + b'!', valid_signature, secret)} | "
        f"Wrong secret: "
        f"{verify_signature(payload, valid_signature, secret + '-wrong')}"
    )


if __name__ == "__main__":
    load_dotenv()
    main()
