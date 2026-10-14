'use strict';

// ── Generic page behaviour ──────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
    var toast = document.getElementById('appToast');
    if (toast) new bootstrap.Toast(toast, { delay: toast.classList.contains('text-bg-danger') ? 7000 : 3500 }).show();

    // Drop ?msg / ?error from the address bar so a refresh does not re-show the toast.
    if (/[?&](msg|error)=/.test(location.search)) {
        var url = new URL(location.href);
        url.searchParams.delete('msg');
        url.searchParams.delete('error');
        history.replaceState(null, '', url.pathname + url.search + url.hash);
    }

    document.querySelectorAll('input[name="phone"], input[type="tel"]').forEach(function (input) {
        input.addEventListener('input', function () {
            var v = this.value.replace(/\D/g, '').substring(0, 11);
            this.value = v.length > 4 ? v.substring(0, 4) + '-' + v.substring(4) : v;
        });
    });

    document.addEventListener('submit', function (e) {
        if (e.defaultPrevented) return;
        var form = e.target;
        var btn = e.submitter;
        var message = (btn && btn.dataset.confirm) || form.dataset.confirm;
        if (message && !confirm(message)) { e.preventDefault(); return; }
        if (btn && !btn.dataset.noSpinner) {
            var label = btn.innerHTML;
            // Disable after the browser has captured the form data.
            setTimeout(function () {
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Please wait…';
            }, 0);
            setTimeout(function () { btn.disabled = false; btn.innerHTML = label; }, 15000);
        }
    });

    document.querySelectorAll('[data-list-filter]').forEach(initListFilter);
    document.querySelectorAll('[data-pdf-target]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var name = btn.dataset.pdfName.replace(/[^\w\-]+/g, '_') + '.pdf';
            downloadPDF(btn, btn.dataset.pdfTarget, name);
        });
    });
    document.querySelectorAll('.print-timestamp').forEach(function (el) { el.textContent = formatNow(); });
});

function formatNow() {
    var d = new Date();
    return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) + ', ' +
        d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
}

// ── Client-side list filtering (orders, reports, patients) ──────────────────
// Rows carry data-search (lower-case text) and optionally data-status / data-date.
function initListFilter(root) {
    var rows = Array.prototype.slice.call(root.querySelectorAll('[data-row]'));
    var search = root.querySelector('[data-filter-search]');
    var date = root.querySelector('[data-filter-date]');
    var statusButtons = root.querySelectorAll('[data-filter-status]');
    var clear = root.querySelector('[data-filter-clear]');
    var empty = root.querySelector('[data-filter-empty]');
    var status = '';

    function apply() {
        var term = search ? search.value.toLowerCase().trim() : '';
        var day = date ? date.value : '';
        var visible = 0;
        rows.forEach(function (r) {
            var show = (!term || r.dataset.search.indexOf(term) !== -1) &&
                (!status || r.dataset.status === status) &&
                (!day || r.dataset.date === day);
            r.classList.toggle('d-none', !show);
            if (show) visible++;
        });
        if (empty) empty.classList.toggle('d-none', visible > 0 || rows.length === 0);
        if (clear) clear.classList.toggle('d-none', !term && !day && !status);
    }

    if (search) search.addEventListener('input', apply);
    if (date) date.addEventListener('change', apply);
    statusButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            status = btn.dataset.filterStatus;
            statusButtons.forEach(function (b) { b.classList.toggle('active', b === btn); });
            apply();
        });
    });
    if (clear) clear.addEventListener('click', function () {
        if (search) search.value = '';
        if (date) date.value = '';
        status = '';
        statusButtons.forEach(function (b) { b.classList.toggle('active', b.dataset.filterStatus === ''); });
        apply();
        if (search) search.focus();
    });
    apply();
}

// ── Result entry ────────────────────────────────────────────────────────────
// Mirrors result_flag() in helpers.py.
function resultFlag(value, range) {
    var v = String(value || '').trim();
    if (!/^-?\d+(\.\d+)?$/.test(v)) return '';
    var n = parseFloat(v), ref = String(range || '').trim(), m;
    if ((m = ref.match(/^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)$/))) {
        return n < parseFloat(m[1]) ? 'L' : n > parseFloat(m[2]) ? 'H' : '';
    }
    if ((m = ref.match(/^<\s*(\d+(?:\.\d+)?)$/))) return n >= parseFloat(m[1]) ? 'H' : '';
    if ((m = ref.match(/^>\s*(\d+(?:\.\d+)?)$/))) return n <= parseFloat(m[1]) ? 'L' : '';
    return '';
}

function initResultsForm(form) {
    var results = Array.prototype.slice.call(form.querySelectorAll('.result-input'));
    var fields = Array.prototype.slice.call(form.querySelectorAll('.result-input, .notes-input'));
    var progressText = form.querySelector('[data-progress-text]');
    var progressBar = form.querySelector('[data-progress-bar]');
    var finalButton = form.querySelector('[data-final-action]');
    var dirty = false;

    function refreshRow(input) {
        var row = input.closest('tr');
        var flag = resultFlag(input.value, input.dataset.range);
        var badge = row.querySelector('.result-flag');
        badge.textContent = flag === 'H' ? 'High' : flag === 'L' ? 'Low' : '';
        badge.className = 'result-flag' + (flag ? ' flag-' + flag : '');
        input.classList.toggle('is-abnormal', !!flag);
        row.classList.toggle('row-done', input.value.trim() !== '');
    }

    function refreshProgress() {
        var done = results.filter(function (i) { return i.value.trim() !== ''; }).length;
        if (progressText) progressText.textContent = done + ' of ' + results.length + ' entered';
        if (progressBar) progressBar.style.width = (results.length ? (done / results.length) * 100 : 0) + '%';
        return results.length - done;
    }

    function focusField(field) {
        field.focus();
        field.select();
        field.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }

    function nextResultAfter(field) {
        var row = field.closest('tr');
        for (var i = 0; i < results.length; i++) {
            if (results[i].compareDocumentPosition(row) & Node.DOCUMENT_POSITION_PRECEDING) return results[i];
        }
        return null;
    }

    results.forEach(function (input) {
        refreshRow(input);
        input.addEventListener('input', function () { refreshRow(input); refreshProgress(); });
    });
    fields.forEach(function (f) {
        f.addEventListener('input', function () { dirty = true; });
    });
    refreshProgress();

    form.addEventListener('keydown', function (e) {
        var field = e.target;
        if (fields.indexOf(field) === -1) return;
        var idx = results.indexOf(field);

        if (e.key === 'Enter') {
            e.preventDefault();
            if (e.shiftKey) {
                var prev = idx > 0 ? results[idx - 1] : (idx === -1 ? field.closest('tr').querySelector('.result-input') : null);
                if (prev) focusField(prev);
                return;
            }
            var next = idx !== -1 ? results[idx + 1] : nextResultAfter(field);
            if (next) focusField(next);
            else if (finalButton) finalButton.focus();
        } else if ((e.key === 'ArrowDown' || e.key === 'ArrowUp') && idx !== -1) {
            var target = results[idx + (e.key === 'ArrowDown' ? 1 : -1)];
            if (target) { e.preventDefault(); focusField(target); }
        }
    });

    form.addEventListener('submit', function (e) {
        var btn = e.submitter;
        if (btn && btn.dataset.completeAction) {
            var missing = refreshProgress();
            var msg = missing > 0
                ? missing + (missing === 1 ? ' test has' : ' tests have') + ' no result yet.\n\nComplete the order and create the report anyway?'
                : 'All results entered. Complete the order and create the report?';
            if (!confirm(msg)) { e.preventDefault(); e.stopImmediatePropagation(); return; }
        }
        dirty = false;
    });

    window.addEventListener('beforeunload', function (e) {
        if (dirty) { e.preventDefault(); e.returnValue = ''; }
    });

    var firstEmpty = results.filter(function (i) { return !i.value.trim(); })[0];
    if (firstEmpty) firstEmpty.focus({ preventScroll: true });
}

// ── PDF download ────────────────────────────────────────────────────────────
function downloadPDF(btn, elementId, fileName) {
    var element = document.getElementById(elementId);
    if (!element) return;
    var label = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Preparing…';
    element.querySelectorAll('.print-timestamp').forEach(function (el) { el.textContent = formatNow(); });

    // Render at desktop width so a PDF made on a phone gets the same A4 layout.
    html2canvas(element, { scale: 2, useCORS: true, backgroundColor: '#ffffff', logging: false, windowWidth: 1200 })
        .then(function (canvas) {
            var pdf = new jspdf.jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
            var margin = 5;
            var pageW = pdf.internal.pageSize.getWidth(), pageH = pdf.internal.pageSize.getHeight();
            var imgW = pageW - margin * 2;
            var pxPerMm = canvas.width / imgW;
            var sliceH = Math.floor((pageH - margin * 2) * pxPerMm);
            for (var y = 0; y < canvas.height; y += sliceH) {
                var h = Math.min(sliceH, canvas.height - y);
                var slice = document.createElement('canvas');
                slice.width = canvas.width;
                slice.height = h;
                slice.getContext('2d').drawImage(canvas, 0, y, canvas.width, h, 0, 0, canvas.width, h);
                if (y > 0) pdf.addPage();
                pdf.addImage(slice.toDataURL('image/jpeg', 0.95), 'JPEG', margin, margin, imgW, h / pxPerMm);
            }
            pdf.save(fileName);
        })
        .catch(function () { alert('Could not create the PDF. Please use the Print button instead.'); })
        .finally(function () { btn.disabled = false; btn.innerHTML = label; });
}
