try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False

from jinja2 import Template
from crud import group_order_items

# Single shared HTML template used for both PDF generation and the HTML fallback.
# The print button is hidden via @media print so it does not appear in WeasyPrint output.
_REPORT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Lab Report – RPT-{{ order.id }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 0;
            color: #333;
            line-height: 1.4;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #007bff;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .header h1 { color: #007bff; margin: 0; font-size: 2em; }
        .header h2 { color: #666; margin: 10px 0; font-weight: normal; font-size: 1.2em; }
        .patient-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
            border: 1px solid #dee2e6;
        }
        .patient-info h3 { margin-top: 0; color: #007bff; font-size: 1.3em; }
        .info-row { margin-bottom: 8px; }
        .info-label { font-weight: bold; display: inline-block; width: 120px; }
        .results-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            border: 1px solid #ddd;
        }
        .results-table th,
        .results-table td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        .results-table th { background-color: #007bff; color: white; font-weight: bold; }
        .results-table tr:nth-child(even) { background-color: #f8f9fa; }
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 0.9em;
        }
        .print-button {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            z-index: 1000;
        }
        .print-button:hover { background: #0056b3; }
        @media print {
            body { margin: 0; font-size: 12pt; }
            .print-button { display: none !important; }
            .header h1 { font-size: 24pt; }
            .header h2 { font-size: 14pt; }
            .patient-info h3 { font-size: 16pt; }
        }
    </style>
</head>
<body>
    <button class="print-button" onclick="window.print()">&#128438; Print / Save PDF</button>

    <div class="header">
        <h1>Laboratory Report</h1>
        <h2>Medical Laboratory Services</h2>
        <p>Report Date: {{ order.ordered_at.strftime('%B %d, %Y') }}</p>
    </div>

    <div class="patient-info">
        <h3>Patient Information</h3>
        <div class="info-row"><span class="info-label">Name:</span> {{ order.patient.name }}</div>
        <div class="info-row"><span class="info-label">Age:</span> {{ order.patient.age }} years</div>
        <div class="info-row"><span class="info-label">Gender:</span> {{ order.patient.gender }}</div>
        <div class="info-row"><span class="info-label">Phone:</span> {{ order.patient.phone }}</div>
        <div class="info-row"><span class="info-label">Report ID:</span> RPT-{{ order.id }}</div>
    </div>

    <h3>Test Results</h3>
    {% for group in groups %}
    <h4 style="color:#0b5ed7; margin-bottom:6px;">{{ group.label }}</h4>
    <table class="results-table">
        <thead>
            <tr>
                <th>Test Name</th>
                <th>Result</th>
                <th>Unit</th>
                <th>Reference Range</th>
                <th>Notes</th>
            </tr>
        </thead>
        <tbody>
            {% for item in group['items'] %}
            <tr>
                <td>{{ item.test.name }}</td>
                <td style="font-weight:bold;">{{ item.result_value or '-' }}</td>
                <td>{{ item.test.unit or '-' }}</td>
                <td>{{ item.test.reference_range or '-' }}</td>
                <td>{{ item.result_notes or '-' }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% endfor %}

    <div class="footer">
        <p><strong>This report is computer generated and does not require signature.</strong></p>
        <p>For any queries, please contact the laboratory.</p>
    </div>
</body>
</html>
"""

def _render_report(order) -> str:
    """Render the shared report HTML template for the given order."""
    template = Template(_REPORT_TEMPLATE)
    return template.render(order=order, groups=group_order_items(order))


def generate_report_pdf(order) -> bytes:
    """Return a PDF byte string for a completed order. Falls back to HTML if WeasyPrint is unavailable."""
    if not WEASYPRINT_AVAILABLE:
        return generate_report_html(order).encode("utf-8")
    try:
        return HTML(string=_render_report(order)).write_pdf()
    except Exception:
        return generate_report_html(order).encode("utf-8")


def generate_report_html(order) -> str:
    """Return a printable HTML string for a completed order."""
    return _render_report(order)
