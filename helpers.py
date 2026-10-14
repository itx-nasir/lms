"""Small presentation helpers exposed to the Jinja templates."""
import re

_NUM = r"(\d+(?:\.\d+)?)"
_RANGE_BETWEEN = re.compile(rf"{_NUM}\s*-\s*{_NUM}")
_RANGE_BELOW = re.compile(rf"<\s*{_NUM}")
_RANGE_ABOVE = re.compile(rf">\s*{_NUM}")


def money(value) -> str:
    return f"{value or 0:,.0f}"


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
