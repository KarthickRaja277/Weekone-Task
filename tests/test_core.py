import hashlib
import hmac

from scripts.task1_core import Employee, Manager, calculate_bonus
from src.security import verify_signature


def test_bonus_extras_and_cap():
    assert calculate_bonus(1000, 0.1, 20, 30, cap=120) == 120


def test_employee_annual_salary():
    assert Employee("A", 100).annual_salary == 1200


def test_manager_details():
    assert Manager("Divya", 75000, 5).get_details() == (
        "Divya - 75000 - Team Size: 5"
    )


def test_hmac_valid():
    payload = b"sample"
    secret = "secret"
    signature = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    assert verify_signature(payload, signature, secret)


def test_hmac_tampered_and_wrong_secret():
    payload = b"sample"
    secret = "secret"
    signature = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    assert not verify_signature(payload + b"x", signature, secret)
    assert not verify_signature(payload, signature, "wrong")
