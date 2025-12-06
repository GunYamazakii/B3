/**
 * Card Validator - Interactive JavaScript
 * Educational Content Only
 */

/**
 * Toggle the name change form visibility
 */
function toggleNameChange() {
    const form = document.getElementById('nameChangeForm');
    if (form.style.display === 'none') {
        form.style.display = 'block';
        document.getElementById('guest_name').focus();
    } else {
        form.style.display = 'none';
    }
}

/**
 * Toggle the site input visibility based on gateway selection
 */
function toggleSiteInput() {
    const gateway = document.getElementById('gateway').value;
    const siteInputGroup = document.getElementById('siteInputGroup');
    
    if (gateway === 'auto_shopify') {
        siteInputGroup.style.display = 'block';
    } else {
        siteInputGroup.style.display = 'none';
    }
}

/**
 * Validate card data on client-side before submission
 */
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.validation-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const cardData = document.getElementById('card_data').value.trim();
            const gateway = document.getElementById('gateway').value;
            
            // Validate card data format
            if (cardData.length < 5) {
                e.preventDefault();
                alert('Card data must be at least 5 characters long.');
                return false;
            }

            // Validate gateway selection
            if (!gateway) {
                e.preventDefault();
                alert('Please select a gateway.');
                return false;
            }

            // Validate site URL for AutoShopify
            if (gateway === 'auto_shopify') {
                const site = document.getElementById('site').value.trim();
                if (site && !isValidUrl(site)) {
                    e.preventDefault();
                    alert('Please enter a valid URL for the Shopify site.');
                    return false;
                }
            }

            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = '⏳ Processing...';
            submitBtn.disabled = true;
            
            // Re-enable after form submission
            setTimeout(() => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 1000);
        });
    }
});

/**
 * Validate URL format
 */
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

/**
 * Fetch current session status via API
 */
async function fetchSessionStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        console.log('Session Status:', data);
        return data;
    } catch (error) {
        console.error('Error fetching session status:', error);
    }
}

/**
 * Clear the textarea after successful submission
 */
document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('card_data');
    if (textarea && window.location.hash === '#success') {
        textarea.value = '';
    }
});

// Log for debugging (remove in production)
console.log('Card Validator - Educational Application Loaded');
