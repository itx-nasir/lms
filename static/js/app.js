document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.alert:not(.d-none)').forEach(alert => {
        setTimeout(() => alert.remove(), 5000);
    });

    document.querySelectorAll('[data-confirm]').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm(this.getAttribute('data-confirm') || 'Are you sure?')) e.preventDefault();
        });
    });

    document.querySelectorAll('input[name="phone"]').forEach(input => {
        input.addEventListener('input', function() {
            let v = this.value.replace(/\D/g, '');
            if (v.length > 11) v = v.substring(0, 11);
            this.value = v.length >= 4 ? v.substring(0, 4) + '-' + v.substring(4) : v;
        });
        input.addEventListener('blur', function() {
            const ok = /^03[0-9]{2}-[0-9]{7}$/.test(this.value);
            this.classList.toggle('is-invalid', this.value && !ok);
        });
    });

    document.querySelectorAll('input[name="price"]').forEach(input => {
        input.addEventListener('blur', function() {
            const v = parseFloat(this.value);
            if (!isNaN(v)) this.value = v.toFixed(2);
        });
    });

    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const btn = this.querySelector('button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                const orig = btn.innerHTML;
                btn.innerHTML = '<span class="spinner me-1"></span>Processing...';
                setTimeout(() => { btn.disabled = false; btn.innerHTML = orig; }, 10000);
            }
        });
    });

    document.querySelectorAll('input[required], select[required], textarea[required]').forEach(input => {
        input.addEventListener('blur', function() {
            const empty = this.value.trim() === '';
            this.classList.toggle('is-invalid', empty);
            this.classList.toggle('is-valid', !empty);
        });
    });
});

// ── Shared PDF & Print Utilities ────────────────────────────────────────

function _formatNow() {
    var d = new Date();
    return d.toLocaleDateString('en-GB', {day:'2-digit', month:'short', year:'numeric'})
        + ', ' + d.toLocaleTimeString('en-US', {hour:'2-digit', minute:'2-digit', hour12:true});
}

function _stampTimestamps(root, selector) {
    root.querySelectorAll(selector || '.print-timestamp').forEach(function(el) {
        el.textContent = _formatNow();
    });
}

function printElement(elementId, title, tsSelector) {
    var content = document.getElementById(elementId);
    if (!content) return;
    var w = window.open('', '_blank', 'width=900,height=700');
    w.document.write('<!DOCTYPE html><html><head><title>' + (title || 'Print') + '</title>');
    w.document.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">');
    w.document.write('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">');
    w.document.write('<link href="/static/css/style.css" rel="stylesheet">');
    w.document.write('<style>body{background:#fff!important;margin:0;padding:10px}.report-wrapper{box-shadow:none!important;padding:0!important;background:#fff!important}.report-card{box-shadow:none!important}</style>');
    w.document.write('</head><body>');
    w.document.write(content.outerHTML);
    w.document.write('</body></html>');
    w.document.close();
    w.onload = function() {
        _stampTimestamps(w.document, tsSelector);
        setTimeout(function(){ w.print(); }, 500);
    };
}

function downloadElementPDF(elementId, fileName, tsSelector) {
    var element = document.getElementById(elementId);
    if (!element) return;

    _stampTimestamps(element, tsSelector);

    var btn = event.target.closest('button');
    var orig = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner me-1"></span>Generating…';

    html2canvas(element, {
        scale: 2, useCORS: true, allowTaint: true, backgroundColor: '#ffffff', logging: false
    }).then(function(canvas) {
        var pdf = new jspdf.jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
        var pw = pdf.internal.pageSize.getWidth(), ph = pdf.internal.pageSize.getHeight();
        var iw = pw - 10, ih = (canvas.height * iw) / canvas.width;
        var sy = 0, rh = ih;
        while (rh > 0) {
            var sh = Math.min(rh, ph - 10);
            var sc = document.createElement('canvas');
            sc.width = canvas.width;
            sc.height = (sh / iw) * canvas.width;
            sc.getContext('2d').drawImage(canvas, 0, sy, canvas.width, sc.height, 0, 0, canvas.width, sc.height);
            if (sy > 0) pdf.addPage();
            pdf.addImage(sc.toDataURL('image/jpeg', 0.95), 'JPEG', 5, 5, iw, sh);
            sy += sc.height;
            rh -= sh;
        }
        pdf.save(fileName);
        btn.disabled = false;
        btn.innerHTML = orig;
    }).catch(function() {
        btn.disabled = false;
        btn.innerHTML = orig;
        alert('PDF generation failed. Please try the print option.');
    });
}
