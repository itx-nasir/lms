// Lab Management System JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => alert.remove(), 5000);
    });

    // Confirm delete actions
    document.querySelectorAll('[data-confirm]').forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) e.preventDefault();
        });
    });

    // Pakistani phone number formatting
    document.querySelectorAll('input[name="phone"]').forEach(input => {
        input.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            
            // Format as 03XX-XXXXXXX for Pakistani mobile numbers
            if (value.length >= 4 && value.length <= 11) {
                this.value = value.substring(0, 4) + '-' + value.substring(4);
            } else if (value.length > 11) {
                // Limit to 11 digits total
                value = value.substring(0, 11);
                this.value = value.substring(0, 4) + '-' + value.substring(4);
            } else {
                this.value = value;
            }
        });
        
        // Validate Pakistani mobile number format on blur
        input.addEventListener('blur', function() {
            const phonePattern = /^03[0-9]{2}-[0-9]{7}$/;
            if (this.value && !phonePattern.test(this.value)) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });

    // Price formatting
    document.querySelectorAll('input[name="price"]').forEach(input => {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value)) this.value = value.toFixed(2);
        });
    });

    // Search functionality with debounce
    document.querySelectorAll('input[name="search"]').forEach(input => {
        let timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                if (this.value.length >= 2 || this.value.length === 0) {
                    this.closest('form').submit();
                }
            }, 500);
        });
    });

    // Form submission with loading state
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner me-1"></span>Processing...';
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 10000);
            }
        });
    });

    // Print functionality
    window.printReport = function() {
        const printContent = document.getElementById('reportContent');
        if (printContent) {
            window.print();
        }
    };

    // Real-time validation feedback
    document.querySelectorAll('input[required], select[required], textarea[required]').forEach(input => {
        input.addEventListener('blur', function() {
            this.classList.toggle('is-invalid', this.value.trim() === '');
            this.classList.toggle('is-valid', this.value.trim() !== '');
        });
    });
});

