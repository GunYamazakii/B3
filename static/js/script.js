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
        // Focus on the input field
        document.getElementById('guest_name').focus();
    } else {
        form.style.display = 'none';
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
            
            if (cardData.length < 10) {
                e.preventDefault();
                alert('Card data must be at least 10 characters long.');
                return false;
            }
            
            // Optional: Show a loading state
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
