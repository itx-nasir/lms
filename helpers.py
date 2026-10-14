"""Small presentation helpers exposed to the Jinja templates."""
import re
from typing import Optional

_NUM = r"(\d+(?:\.\d+)?)"
_RANGE_BETWEEN = re.compile(rf"{_NUM}\s*-\s*{_NUM}")
_RANGE_BELOW = re.compile(rf"<\s*{_NUM}")
_RANGE_ABOVE = re.compile(rf">\s*{_NUM}")

_UAE_LOCAL = re.compile(r"05\d{8}")
_UAE_INTL = re.compile(r"9715\d{8}")
_PK_LOCAL = re.compile(r"03\d{9}")
_PK_INTL = re.compile(r"923\d{9}")
_E164 = re.compile(r"[1-9]\d{7,14}")


def money(value) -> str:
    return f"{value or 0:,.0f}"


def whatsapp_number(phone) -> Optional[str]:
    """Return the phone as digits-only international format for wa.me
    ("971501234567"), or None if it is missing or invalid. Local UAE (05x)
    and Pakistan (03x) mobiles get their country code added; other countries
    are only accepted when written with a leading + or 00."""
    raw = (phone or "").strip()
    digits = re.sub(r"\D", "", raw)
    if _UAE_LOCAL.fullmatch(digits):
        return "971" + digits[1:]
    if _PK_LOCAL.fullmatch(digits):
        return "92" + digits[1:]

    explicit_international = raw.startswith("+") or digits.startswith("00")
    if digits.startswith("00"):
        digits = digits[2:]
    if _UAE_INTL.fullmatch(digits) or _PK_INTL.fullmatch(digits):
        return digits
    if explicit_international and not digits.startswith(("971", "92")) and _E164.fullmatch(digits):
        return digits
    return None


def result_flag(value, reference_range) -> str:
    """Return "H" / "L" when a numeric result falls outside its reference
    range ("4-10", "<5", ">90"), otherwise "". Mirrors resultFlag() in app.js."""
    try:
        v = float(str(value).strip())
    except (TypeError, ValueError):
        return ""
    ref = (reference_range or "").strip()
    if m := _RANGE_BETWEEN.fullmatch(ref):
        low, high = float(m[1]), float(m[2])
        return "L" if v < low else "H" if v > high else ""
    if m := _RANGE_BELOW.fullmatch(ref):
        return "H" if v >= float(m[1]) else ""
    if m := _RANGE_ABOVE.fullmatch(ref):
        return "L" if v <= float(m[1]) else ""
    return ""


def group_order_items(order):
    """Group an order's items by the panel they were ordered with; tests
    ordered individually are collected into a trailing "Other Tests" group."""
    groups, by_panel_order, others = [], {}, []
    for item in order.items:
        if item.panel_order_id:
            group = by_panel_order.get(item.panel_order_id)
            if group is None:
                group = {"label": item.panel_order.panel.name, "items": []}
                by_panel_order[item.panel_order_id] = group
                groups.append(group)
            group["items"].append(item)
        else:
            others.append(item)
    if others:
        groups.append({"label": "Other Tests", "items": others})
    return groups
