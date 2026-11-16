"""Separate Loan Operations Portal interface and manual application register."""
from __future__ import annotations

import html
import streamlit as st

from services import (
    extract_applications,
    format_currency,
    list_applications,
    mask_aadhaar,
    mask_mobile,
    mask_pan,
)


def initialize_operations_state() -> None:
    st.session_state.setdefault("ops_initial", True)
    st.session_state.setdefault("ops_loaded_successfully", False)
    st.session_state.setdefault("ops_records", [])
    st.session_state.setdefault("ops_error", None)
    st.session_state.setdefault("ops_last_status", None)


def _load_records(live_slot=None) -> None:
    st.session_state.ops_initial = False
    st.session_state.ops_error = None
    if live_slot is not None:
        live_slot.info("Retrieving applications from MuleSoft…")
    with st.spinner("Retrieving applications from MuleSoft…"):
        result = list_applications()

    status = int(result.get("status", 502))
    st.session_state.ops_last_status = status
    if status == 405:
        target = result.get("upstreamUrl") or "the configured MuleSoft GET endpoint"
        message = (
            f"MuleSoft returned HTTP 405 (Method Not Allowed) for GET {target}. "
            "Check that the MuleSoft flow exposes a GET listener on this exact path."
        )
    elif status >= 400 or result.get("ok") is False:
        upstream_message = result.get("data")
        if isinstance(upstream_message, dict):
            upstream_message = (
                upstream_message.get("message")
                or upstream_message.get("description")
                or upstream_message.get("errorDescription")
            )
        elif not isinstance(upstream_message, str):
            upstream_message = None
        message = result.get("error") or upstream_message or result.get("statusText") or f"The API returned HTTP {status}."
    else:
        records = extract_applications(result.get("data", result))
        st.session_state.ops_records = records
        st.session_state.ops_loaded_successfully = True
        st.session_state.ops_error = None
        return

    st.session_state.ops_error = str(message)
    # Keep existing records visible after a failed refresh, matching the source app.


def _records_table(records: list[dict]) -> str:
    headers = [
        "Application ID",
        "Applicant",
        "Date of birth",
        "PAN",
        "Aadhaar",
        "Mobile",
        "Requested amount",
        "Tenure",
    ]
    rows = []
    for record in records:
        values = [
            record.get("applicationId") or "—",
            record.get("fullName") or "—",
            record.get("dob") or "—",
            mask_pan(record.get("pan")),
            mask_aadhaar(record.get("aadhaar")),
            mask_mobile(record.get("mobile")),
            format_currency(record.get("requestedAmount")),
            f"{record.get('tenureMonths')} months" if record.get("tenureMonths") else "—",
        ]
        rows.append("<tr>" + "".join(f"<td>{html.escape(str(value))}</td>" for value in values) + "</tr>")
    header_html = "".join(f"<th>{html.escape(value)}</th>" for value in headers)
    body_html = "".join(rows)
    return (
        '<div class="ops-table-wrap"><table class="ops-table"><thead><tr>'
        f"{header_html}</tr></thead><tbody>{body_html}</tbody></table></div>"
    )


def render_operations_portal() -> None:
    initialize_operations_state()
    st.markdown(
        '<div class="page-topbar"><span>Operations&nbsp;&nbsp; / &nbsp;&nbsp;<strong>Application register</strong></span><span class="ops-environment">● &nbsp;MULESOFT DEMO</span></div>',
        unsafe_allow_html=True,
    )

    heading_col, button_col = st.columns([5, 1.25], vertical_alignment="bottom")
    with heading_col:
        st.markdown(
            '<div class="ops-eyebrow">LOAN SERVICING <span style="display:inline-block;width:19px;height:1px;background:#a8bcae;vertical-align:middle"></span> BACK-OFFICE</div>'
            '<h1 class="ops-heading">Loan application register</h1>'
            '<p class="ops-description">A consolidated list of applications returned by the MuleSoft API.</p>',
            unsafe_allow_html=True,
        )
    with button_col:
        refresh_clicked = st.button("↻  Refresh records", key="ops_refresh", use_container_width=True)
    if refresh_clicked:
        live_slot = st.empty()
        _load_records(live_slot)
        st.rerun()

    st.markdown(
        '<div class="ops-demo-banner"><span style="display:grid;width:17px;height:17px;flex:0 0 17px;place-items:center;border-radius:50%;color:white;background:#a58a4e;font:700 10px Georgia,serif">i</span>'
        '<span><strong>Illustrative demo only.</strong> This is a mocked implementation created to showcase MuleSoft API functionality. Records and workflows are for demonstration purposes only and must not be treated as real loan decisions or production records.</span></div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown(
            '<div class="ops-panel-heading"><div><span class="ops-panel-kicker">APPLICATIONS</span><h2>Submitted applications</h2></div>'
            '<span class="ops-panel-note">Refresh to retrieve the latest records</span></div>',
            unsafe_allow_html=True,
        )
        if st.session_state.ops_initial:
            st.markdown('<div style="min-height:85px;padding:20px;color:#7b8a82;font-size:10px">Select <strong>Refresh records</strong> to load loan applications.</div>', unsafe_allow_html=True)
        if st.session_state.ops_error:
            st.error(st.session_state.ops_error)
            if st.button("Try again", key="ops_retry", type="secondary"):
                live_slot = st.empty()
                _load_records(live_slot)
                st.rerun()
        if st.session_state.ops_loaded_successfully:
            records = st.session_state.ops_records
            if records:
                st.markdown(_records_table(records), unsafe_allow_html=True)
            else:
                st.markdown('<div style="min-height:85px;padding:20px;color:#7b8a82;font-size:10px">No loan applications were returned.</div>', unsafe_allow_html=True)
            count = f"{len(records)} application" + ("" if len(records) == 1 else "s")
            st.markdown(
                f'<div class="ops-panel-footer"><strong style="color:#52705d">{count}</strong><span>Personal identifiers are masked in this view.</span></div>',
                unsafe_allow_html=True,
            )
        elif not st.session_state.ops_initial and not st.session_state.ops_error:
            st.markdown('<div style="min-height:85px;padding:20px;color:#7b8a82;font-size:10px">No loan applications were returned.</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="ops-footer"><span>Loan Operations Portal</span><span>Illustrative MuleSoft API demonstration</span></div>',
        unsafe_allow_html=True,
    )
