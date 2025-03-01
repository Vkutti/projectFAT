/**
 * Business Form JavaScript
 * Provides enhanced functionality for the business submission form
 */

document.addEventListener('DOMContentLoaded', function() {
    // Form validation enhancements
    const form = document.getElementById('BusinessF');
    const submitBtn = document.getElementById('submitBtn');
    
    if (form) {
        // Format phone number as user types
        const phoneInput = document.getElementById('phoneNumber');
        if (phoneInput) {
            phoneInput.addEventListener('input', function(e) {
                const formatted = formatPhoneNumber(e.target.value);
                phoneInput.value = formatted;
            });
        }
        
        // Handle form submission with validation
        form.addEventListener('submit', function(e) {
            // The form will submit normally for backend processing
            
            // Show a loading indicator
            document.body.classList.add('form-submitting');
            
            // Form is valid, continue with normal submission
            return true;
        });
    }
    
    // Community dropdown handler
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    const communityInput = document.getElementById('community');
    
    dropdownItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const selectedValue = this.getAttribute('data-value');
            communityInput.value = selectedValue;
            
            // Update the dropdown button text to show selection
            const dropdownButton = this.closest('.input-group').querySelector('.dropdown-toggle');
            if (dropdownButton) {
                dropdownButton.textContent = selectedValue;
            }
        });
    });
    
    // Helper functions
    function formatPhoneNumber(value) {
        // Remove all non-digit characters
        const numbers = value.replace(/\D/g, '');
        
        // Format as (123) 456-7890
        const match = numbers.match(/^(\d{0,3})(\d{0,3})(\d{0,4})$/);
        
        if (match) {
            const part1 = match[1] ? `(${match[1]}` : '';
            const part2 = match[2] ? `) ${match[2]}` : '';
            const part3 = match[3] ? `-${match[3]}` : '';
            return `${part1}${part2}${part3}`;
        }
        
        return value;
    }
    
    // Update business hours from selectors
    const updateBusinessHours = function() {
        const openingHour = document.getElementById("openingHour");
        const openingMinute = document.getElementById("openingMinute");
        const openingAMPM = document.getElementById("openingAMPM");
        const closingHour = document.getElementById("closingHour");
        const closingMinute = document.getElementById("closingMinute");
        const closingAMPM = document.getElementById("closingAMPM");
        const days = document.getElementById("days");
        const businessHoursInput = document.getElementById("businessHours");
        
        if (openingHour && openingMinute && closingHour && businessHoursInput) {
            const openingTime = `${openingHour.value}:${openingMinute.value}${openingAMPM.value}`;
            const closingTime = `${closingHour.value}:${closingMinute.value}${closingAMPM.value}`;
            const daysValue = days.value;
            
            businessHoursInput.value = `${openingTime}-${closingTime} ${daysValue}`;
        }
    };
    
    // Set up business hours selectors
    const hourSelectors = [
        "openingHour", "openingMinute", "openingAMPM",
        "closingHour", "closingMinute", "closingAMPM", "days"
    ];
    
    hourSelectors.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener("change", updateBusinessHours);
        }
    });
    
    // Initialize business hours on page load
    updateBusinessHours();
    
    console.log('Business form JS loaded successfully');
}); 