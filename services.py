"""MuleSoft integration and data-shaping helpers for the LoanDesk demo."""
from __future__ import annotations

import json
import os
import re
from typing import Any

import requests
import streamlit as st

MULESOFT_HOST = "https://loan-application-api-ygnir9.3m1neu-1.ind-w1.in1.cloudhub.io"
DEFAULT_APPLY_URL = f"{MULESOFT_HOST}/api/v1/loans/apply"
DEFAULT_LIST_URL = f"{MULESOFT_HOST}/api/v1/loans"
REQUEST_TIMEOUT_SECONDS = 60
MAX_BODY_BYTES = 32 * 1024
REQUIRED_CUSTOMER_FIELDS = (
    "fullName",
    "dob",
    "pan",
    "aadhaar",
    "mobile",
    "applicationId",
    "requestedAmount",
    "tenureMonths",
)
ALLOWED_VERIFICATION_STEPS = {"PAN", "AADHAR", "CREDITCHECK", "SUBMIT"}


def _secret_or_env(secret_key: str, env_key: str, default: str) -> str:
    """Read Streamlit secrets first, then environment variables, then fallback."""
    try:
        value = st.secrets.get(secret_key)
        if value:
            return str(value).strip()
    except Exception:
        # A local secrets.toml file is optional.
        pass
    return os.environ.get(env_key, default).strip()


def mule_urls() -> tuple[str, str]:
    return (
        _secret_or_env("MULESOFT_APPLY_URL", "MULESOFT_APPLY_URL", DEFAULT_APPLY_URL),
        _secret_or_env("MULESOFT_LIST_URL", "MULESOFT_LIST_URL", DEFAULT_LIST_URL),
    )


def validate_customer_server(customer: Any) -> str | None:
    """Mirror the Node proxy's required-field and format validation."""
    for key in REQUIRED_CUSTOMER_FIELDS:
        value = customer.get(key) if isinstance(customer, dict) else None
        if not isinstance(value, str) or not value.strip():
            return f"{key} is required."
    if not re.fullmatch(r"\d{2}-\d{2}-\d{4}", customer["dob"]):
        return "Date of birth must use DD-MM-YYYY."
    if not re.fullmatch(r"[A-Z]{5}\d{4}[A-Z]", customer["pan"]):
        return "PAN must use the format ABCDE1234F."
    if not re.fullmatch(r"LR-\d{6}", customer["applicationId"]):
        return "Application ID must use LR- followed by six digits."
    if not re.fullmatch(r"\d{12}", customer["aadhaar"]):
        return "Aadhaar must contain 12 digits."
    if not re.fullmatch(r"\d{10}", customer["mobile"]):
        return "Mobile number must contain 10 digits."
    if not re.fullmatch(r"\d+", customer["requestedAmount"]):
        return "Requested amount must be a positive whole number."
    try:
        amount = int(customer["requestedAmount"])
    except (TypeError, ValueError):
        return "Requested amount must be a positive whole number."
    if amount <= 0:
        return "Requested amount must be a positive whole number."
    if not re.fullmatch(r"\d+", customer["tenureMonths"]):
        return "Tenure must be a positive whole number of months."
    try:
        tenure = int(customer["tenureMonths"])
    except (TypeError, ValueError):
        return "Tenure must be a positive whole number of months."
    if tenure <= 0:
        return "Tenure must be a positive whole number of months."
    return None


def _parse_response_body(response: requests.Response) -> Any:
    text_body = response.text
    if not text_body:
        return None
    try:
        return response.json()
    except (ValueError, requests.JSONDecodeError):
        return text_body


def apply_application(customer: dict[str, str], verification_step: str | None = None) -> dict[str, Any]:
    """POST to MuleSoft and return the same envelope produced by the Node proxy."""
    apply_url, _ = mule_urls()
    validation_error = validate_customer_server(customer)
    if validation_error:
        return {
            "ok": False,
            "status": 400,
            "statusText": "Bad Request",
            "upstreamMethod": "POST",
            "upstreamUrl": apply_url,
            "verificationStep": verification_step,
            "error": validation_error,
            "data": None,
        }

    step = verification_step.upper() if verification_step else None
    if step and step not in ALLOWED_VERIFICATION_STEPS:
        return {
            "ok": False,
            "status": 400,
            "statusText": "Bad Request",
            "upstreamMethod": "POST",
            "upstreamUrl": apply_url,
            "verificationStep": step,
            "error": "Invalid verification step.",
            "data": None,
        }

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if step:
        headers["verificationStep"] = step
    request_json = json.dumps({"customer": customer}, ensure_ascii=False, separators=(",", ":"))
    if len(request_json.encode("utf-8")) > MAX_BODY_BYTES:
        return {
            "ok": False,
            "status": 413,
            "statusText": "Payload Too Large",
            "upstreamMethod": "POST",
            "upstreamUrl": apply_url,
            "verificationStep": step,
            "error": "Request body is too large.",
            "data": None,
        }
    try:
        response = requests.post(
            apply_url,
            data=request_json.encode("utf-8"),
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        body = _parse_response_body(response)
        return {
            "ok": response.ok,
            "status": response.status_code,
            "statusText": response.reason or "",
            "upstreamMethod": "POST",
            "upstreamUrl": apply_url,
            "verificationStep": step,
            "data": body,
        }
    except requests.Timeout as exc:
        return {
            "ok": False,
            "status": 502,
            "statusText": "Bad Gateway",
            "upstreamMethod": "POST",
            "upstreamUrl": apply_url,
            "verificationStep": step,
            "error": "The MuleSoft endpoint did not respond within 60 seconds.",
            "detail": str(exc) or "Request timed out",
        }
    except requests.RequestException as exc:
        return {
            "ok": False,
            "status": 502,
            "statusText": "Bad Gateway",
            "upstreamMethod": "POST",
            "upstreamUrl": apply_url,
            "verificationStep": step,
            "error": "Could not reach the MuleSoft submission endpoint. Check that the Mule app is running and the POST URL is correct.",
            "detail": str(exc) or "Unknown network error",
        }


def list_applications() -> dict[str, Any]:
    """GET the MuleSoft register endpoint and return the Node proxy envelope."""
    _, list_url = mule_urls()
    try:
        response = requests.get(
            list_url,
            headers={"Accept": "application/json"},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        return {
            "ok": response.ok,
            "status": response.status_code,
            "statusText": response.reason or "",
            "upstreamMethod": "GET",
            "upstreamUrl": list_url,
            "data": _parse_response_body(response),
        }
    except requests.Timeout as exc:
        return {
            "ok": False,
            "status": 502,
            "statusText": "Bad Gateway",
            "upstreamMethod": "GET",
            "upstreamUrl": list_url,
            "error": "The MuleSoft loan records endpoint did not respond within 60 seconds.",
            "detail": str(exc) or "Request timed out",
        }
    except requests.RequestException as exc:
        return {
            "ok": False,
            "status": 502,
            "statusText": "Bad Gateway",
            "upstreamMethod": "GET",
            "upstreamUrl": list_url,
            "error": (
                f"Could not reach the MuleSoft loan records endpoint at {list_url}. "
                "Check that your Mule app is running and the GET URL is correct."
            ),
            "detail": str(exc) or "Unknown network error",
        }


def collect_response_text(value: Any, seen: set[int] | None = None) -> str:
    """Recursively concatenate string values, like the source JavaScript helper."""
    if isinstance(value, str):
        return value
    if value is None or isinstance(value, (int, float, bool)):
        return ""
    if seen is None:
        seen = set()
    object_id = id(value)
    if object_id in seen:
        return ""
    seen.add(object_id)
    if isinstance(value, list):
        return " ".join(filter(None, (collect_response_text(item, seen) for item in value)))
    if isinstance(value, dict):
        return " ".join(filter(None, (collect_response_text(item, seen) for item in value.values())))
    return ""


def identify_verification_failure(value: Any) -> dict[str, Any] | None:
    response_text = re.sub(r"\s+", " ", collect_response_text(value)).strip()
    if re.search(r"\bpan\s+number\s+is\s+invalid\b", response_text, re.IGNORECASE):
        return {
            "stepIndex": 0,
            "code": "PAN",
            "title": "PAN verification failed",
            "label": "PAN verification failed",
            "message": (
                "PAN verification failed. The PAN number is invalid. "
                "Please check the PAN details and try again."
            ),
        }
    if re.search(r"\b(?:aadhaar|aadhar)\s+number\s+is\s+invalid\b", response_text, re.IGNORECASE):
        return {
            "stepIndex": 1,
            "code": "AADHAR",
            "title": "Aadhaar verification failed",
            "label": "Aadhaar verification failed",
            "message": (
                "Aadhaar verification failed. The Aadhaar number is invalid. "
                "Please check the 12-digit number and try again."
            ),
        }
    return None


def parse_record_value(value: Any) -> dict[str, Any] | None:
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else None
        except (json.JSONDecodeError, TypeError):
            return None
    return value if isinstance(value, dict) else None


def extract_applications(api_response: Any) -> list[dict[str, Any]]:
    """Accept arrays, a single record, JSON-string values, and keyed object maps."""
    payload = api_response.get("data", api_response) if isinstance(api_response, dict) else api_response

    for _ in range(4):
        if not isinstance(payload, dict):
            break
        if "applicationId" in payload or "fullName" in payload:
            break
        if isinstance(payload.get("data"), (dict, list)):
            payload = payload["data"]
            continue
        if isinstance(payload.get("records"), (dict, list)):
            payload = payload["records"]
            continue
        break

    if isinstance(payload, list):
        result: list[dict[str, Any]] = []
        for value in payload:
            record = parse_record_value(value)
            if record:
                record = dict(record)
                record["applicationId"] = record.get("applicationId") or record.get("id") or "—"
                result.append(record)
        return result

    if not isinstance(payload, dict):
        return []
    if "applicationId" in payload or "fullName" in payload:
        record = dict(payload)
        record["applicationId"] = record.get("applicationId") or record.get("id") or "—"
        return [record]

    excluded = {"ok", "status", "statusText", "message", "upstreamMethod", "upstreamUrl"}
    result = []
    for key, value in payload.items():
        if key in excluded:
            continue
        record = parse_record_value(value)
        if record:
            record = dict(record)
            record["applicationId"] = record.get("applicationId") or key
            result.append(record)
    return result


def indian_number(value: Any) -> str:
    """Format a whole-number value with Indian digit grouping."""
    try:
        number = int(float(str(value).replace(",", "").strip()))
    except (TypeError, ValueError, OverflowError):
        return "—"
    sign = "-" if number < 0 else ""
    digits = str(abs(number))
    if len(digits) <= 3:
        return sign + digits
    last_three = digits[-3:]
    leading = digits[:-3]
    groups: list[str] = []
    while len(leading) > 2:
        groups.insert(0, leading[-2:])
        leading = leading[:-2]
    if leading:
        groups.insert(0, leading)
    return sign + ",".join(groups + [last_three])


def format_currency(value: Any) -> str:
    try:
        number = float(str(value).replace(",", "").strip())
        if not (number == number and abs(number) != float("inf")):
            return "—"
    except (TypeError, ValueError):
        return "—"
    return f"₹{indian_number(number)}"


def mask_pan(value: Any) -> str:
    pan = str(value or "").strip()
    if not pan:
        return "—"
    if len(pan) < 5:
        return "••••••••••"
    return f"{pan[:2]}•••••{pan[-2:]}"


def mask_aadhaar(value: Any) -> str:
    aadhaar = re.sub(r"\D", "", str(value or ""))
    return f"•••• •••• {aadhaar[-4:]}" if len(aadhaar) >= 4 else "—"


def mask_mobile(value: Any) -> str:
    mobile = re.sub(r"\D", "", str(value or ""))
    return f"{mobile[:2]}••••••{mobile[-2:]}" if len(mobile) >= 4 else "—"
