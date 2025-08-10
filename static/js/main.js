// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltip
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Function to calculate booking price based on selected dates
    function calculateBookingPrice() {
        const startDateEl = document.getElementById('id_start_date');
        const endDateEl = document.getElementById('id_end_date');
        const pricePerDayEl = document.getElementById('price_per_day');
        const totalPriceEl = document.getElementById('total_price');
        
        if (startDateEl && endDateEl && pricePerDayEl && totalPriceEl) {
            const startDate = new Date(startDateEl.value);
            const endDate = new Date(endDateEl.value);
            const pricePerDay = parseFloat(pricePerDayEl.textContent);
            
            if (!isNaN(startDate.getTime()) && !isNaN(endDate.getTime()) && !isNaN(pricePerDay)) {
                // Calculate the time difference in milliseconds
                const timeDiff = Math.abs(endDate.getTime() - startDate.getTime());
                
                // Convert time difference to days
                const diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
                
                // Calculate total price
                const totalPrice = diffDays * pricePerDay;
                
                // Update total price in the UI
                totalPriceEl.textContent = totalPrice.toFixed(2);
                
                // Show booking summary
                document.getElementById('booking_summary').classList.remove('d-none');
            }
        }
    }
    
    // Add event listeners to date inputs in booking form
    const startDateEl = document.getElementById('id_start_date');
    const endDateEl = document.getElementById('id_end_date');
    
    if (startDateEl && endDateEl) {
        startDateEl.addEventListener('change', calculateBookingPrice);
        endDateEl.addEventListener('change', calculateBookingPrice);
    }
    
    // Filter functionality for car listings
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            // Set minimum price if max is set but min is not
            const minPrice = document.getElementById('min_price');
            const maxPrice = document.getElementById('max_price');
            
            if (maxPrice.value && !minPrice.value) {
                minPrice.value = '0';
            }
        });
    }
    
    // Image gallery functionality on car detail page
    const thumbnails = document.querySelectorAll('.car-thumbnail');
    const mainImage = document.getElementById('main-car-image');
    
    if (thumbnails.length > 0 && mainImage) {
        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', function() {
                // Update main image source
                mainImage.src = this.src;
                
                // Remove active class from all thumbnails
                thumbnails.forEach(t => t.classList.remove('active'));
                
                // Add active class to clicked thumbnail
                this.classList.add('active');
            });
        });
    }
    
    // Animated counter for stats on homepage
    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
    
    // Animate stats if they exist
    const statsCounters = document.querySelectorAll('.stats-counter');
    if (statsCounters.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counterEl = entry.target;
                    const endValue = parseInt(counterEl.getAttribute('data-count'));
                    animateValue(counterEl, 0, endValue, 2000);
                    observer.unobserve(counterEl);
                }
            });
        }, { threshold: 0.5 });
        
        statsCounters.forEach(counter => {
            observer.observe(counter);
        });
    }
});
