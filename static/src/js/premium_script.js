/**
 * Ghana Real Estate Premium Website JavaScript
 * Elite Development Team
 */

(function($) {
    'use strict';

    /**
     * Initialize all functionality when document is ready
     */
    $(document).ready(function() {
        // Initialize components
        PremiumWebsite.init();
    });

    /**
     * Main Premium Website Object
     */
    const PremiumWebsite = {
        init: function() {
            this.initNavigation();
            this.initSearchTabs();
            this.initPropertyCarousel();
            this.initTestimonialCarousel();
            this.initImageGallery();
            this.initMapIntegration();
            this.initFormValidation();
            this.initAnimations();
            this.initCompareFunctionality();
            this.initFavoriteFunctionality();
            this.initLazyLoading();
        },

        /**
         * Navigation functionality
         */
        initNavigation: function() {
            // Sticky header effect
            const $header = $('.premium-header');
            $(window).scroll(function() {
                if ($(this).scrollTop() > 50) {
                    $header.addClass('scrolled');
                } else {
                    $header.removeClass('scrolled');
                }
            });

            // Mobile menu toggle
            $('.navbar-toggler').on('click', function() {
                $(this).toggleClass('active');
            });

            // Smooth scroll for anchor links
            $('a[href^="#"]').on('click', function(e) {
                const target = $(this.getAttribute('href'));
                if (target.length) {
                    e.preventDefault();
                    $('html, body').stop().animate({
                        scrollTop: target.offset().top - 80
                    }, 1000);
                }
            });

            // Active nav link based on scroll
            const sections = $('section[id]');
            $(window).scroll(function() {
                const scrollPos = $(window).scrollTop() + 100;
                sections.each(function() {
                    const top = $(this).offset().top;
                    const bottom = top + $(this).outerHeight();
                    if (scrollPos >= top && scrollPos <= bottom) {
                        $('.nav-link').removeClass('active');
                        $(`.nav-link[href="#${$(this).attr('id')}"]`).addClass('active');
                    }
                });
            });
        },

        /**
         * Property search tabs
         */
        initSearchTabs: function() {
            $('.search-tab').on('click', function() {
                const tab = $(this).data('tab');
                
                // Update active tab
                $(this).siblings().removeClass('active');
                $(this).addClass('active');
                
                // Update form action or transaction type hidden input
                const $form = $(this).closest('.search-form');
                $form.find('input[name="transaction_type"]').remove();
                
                // You can add logic here to update form submission
                console.log('Active transaction type:', tab);
            });

            // Search form submission
            $('.search-form').on('submit', function(e) {
                const $form = $(this);
                const activeTab = $('.search-tab.active').data('tab');
                
                // Add transaction type to form
                $form.append(`<input type="hidden" name="transaction_type" value="${activeTab}">`);
            });

            // Location autocomplete
            if ($.fn.autocomplete) {
                $('#location-input').autocomplete({
                    source: function(request, response) {
                        // This would typically call an API endpoint
                        // For demo, using static data
                        const ghanaLocations = [
                            'Accra', 'Kumasi', 'Takoradi', 'Cape Coast', 'Tamale',
                            'Tema', 'Ashaiman', 'Koforidua', 'Sunyani', 'Wa',
                            'Greater Accra', 'Ashanti Region', 'Central Region',
                            'Northern Region', 'Western Region', 'Eastern Region'
                        ];
                        
                        const filtered = ghanaLocations.filter(location =>
                            location.toLowerCase().includes(request.term.toLowerCase())
                        );
                        response(filtered);
                    },
                    minLength: 2,
                    delay: 300
                });
            }
        },

        /**
         * Property carousel initialization
         */
        initPropertyCarousel: function() {
            if (typeof $.fn.owlCarousel !== 'undefined') {
                $('.spotlight-carousel').owlCarousel({
                    items: 3,
                    loop: true,
                    margin: 30,
                    autoplay: true,
                    autoplayTimeout: 5000,
                    autoplayHoverPause: true,
                    nav: true,
                    dots: true,
                    responsive: {
                        0: { items: 1 },
                        768: { items: 2 },
                        992: { items: 3 }
                    },
                    navText: [
                        '<i class="fa fa-chevron-left"></i>',
                        '<i class="fa fa-chevron-right"></i>'
                    ],
                    animateOut: 'fadeOut',
                    animateIn: 'fadeIn'
                });
            }
        },

        /**
         * Testimonial carousel initialization
         */
        initTestimonialCarousel: function() {
            if (typeof $.fn.owlCarousel !== 'undefined') {
                $('.testimonials-carousel').owlCarousel({
                    items: 1,
                    loop: true,
                    margin: 0,
                    autoplay: true,
                    autoplayTimeout: 6000,
                    autoplayHoverPause: true,
                    nav: true,
                    dots: true,
                    responsive: {
                        0: { items: 1 },
                        768: { items: 1 }
                    },
                    navText: [
                        '<i class="fa fa-chevron-left"></i>',
                        '<i class="fa fa-chevron-right"></i>'
                    ]
                });
            }
        },

        /**
         * Image gallery functionality
         */
        initImageGallery: function() {
            // Property image gallery
            $('.thumbnail').on('click', function() {
                const imageUrl = $(this).data('image');
                $('#main-image').attr('src', imageUrl);
                $(this).siblings().removeClass('active');
                $(this).addClass('active');
            });

            // Thumbnail hover effect
            $('.thumbnail').hover(
                function() { $(this).css('cursor', 'pointer'); },
                function() { $(this).css('cursor', 'default'); }
            );

            // Lightbox for property images
            $('.property-image').on('click', function(e) {
                if (!$(e.target).closest('.property-actions, .property-badge').length) {
                    // Trigger lightbox - implement based on your lightbox library
                    console.log('Open lightbox for property image');
                }
            });
        },

        /**
         * Map integration placeholder
         */
        initMapIntegration: function() {
            // Property map placeholder
            // In production, integrate with Google Maps or Mapbox
            $('.property-map').each(function() {
                const address = $(this).data('address') || 'Ghana';
                $(this).html(`
                    <div class="map-placeholder">
                        <i class="fa fa-map-marker"></i>
                        <p>Interactive Map</p>
                        <p class="text-muted">${address}</p>
                        <div class="map-controls">
                            <button class="btn btn-sm btn-primary" onclick="window.open('https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}', '_blank')">
                                <i class="fa fa-external-link"></i> Open in Google Maps
                            </button>
                        </div>
                    </div>
                `);
            });
        },

        /**
         * Form validation
         */
        initFormValidation: function() {
            // Contact form validation
            $('.contact-form').on('submit', function(e) {
                const $form = $(this);
                let isValid = true;
                
                $form.find('input[required], textarea[required], select[required]').each(function() {
                    const $input = $(this);
                    const value = $input.val().trim();
                    
                    if (!value) {
                        isValid = false;
                        $input.addClass('is-invalid');
                    } else if ($input.attr('type') === 'email' && !isValidEmail(value)) {
                        isValid = false;
                        $input.addClass('is-invalid');
                    } else {
                        $input.removeClass('is-invalid');
                    }
                });
                
                if (!isValid) {
                    e.preventDefault();
                    $form.find('.is-invalid').first().focus();
                }
            });

            // Real-time validation feedback
            $('input, textarea, select').on('blur', function() {
                const $input = $(this);
                if ($input.attr('required') && !$input.val().trim()) {
                    $input.addClass('is-invalid');
                } else {
                    $input.removeClass('is-invalid');
                }
            });

            // Phone number formatting for Ghana
            $('input[type="tel"]').on('blur', function() {
                let phone = $(this).val().trim();
                phone = phone.replace(/[^0-9+]/g, '');
                
                if (phone.startsWith('233')) {
                    phone = '+' + phone;
                } else if (phone.startsWith('0')) {
                    phone = '+233' + phone.substring(1);
                } else if (!phone.startsWith('+')) {
                    phone = '+233' + phone;
                }
                
                $(this).val(phone);
            });
        },

        /**
         * Scroll animations
         */
        initAnimations: function() {
            // Animate elements when they come into view
            const observerOptions = {
                root: null,
                rootMargin: '0px',
                threshold: 0.1
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animated', 'fadeInUp');
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            // Observe animated elements
            $('.property-card, .type-card, .agent-card, .location-card').each(function() {
                observer.observe(this);
            });

            // Number counter animation
            $('.stat-number').each(function() {
                const $this = $(this);
                const target = parseInt($this.text().replace(/[^0-9]/g, ''));
                
                $(this).text('0');
                
                const counterObserver = new IntersectionObserver((entries) => {
                    if (entries[0].isIntersecting) {
                        animateNumber($this, target);
                        counterObserver.disconnect();
                    }
                });
                counterObserver.observe(this);
            });
        },

        /**
         * Property comparison functionality
         */
        initCompareFunctionality: function() {
            // Add to compare
            $('.action-btn[data-action="compare"]').on('click', function() {
                const propertyId = $(this).data('property-id');
                const properties = JSON.parse(localStorage.getItem('compareProperties') || '[]');
                
                if (properties.includes(propertyId)) {
                    // Remove from compare
                    const index = properties.indexOf(propertyId);
                    properties.splice(index, 1);
                    $(this).removeClass('active');
                    showNotification('Property removed from comparison');
                } else {
                    // Add to compare
                    if (properties.length >= 4) {
                        showNotification('You can compare up to 4 properties', 'warning');
                        return;
                    }
                    properties.push(propertyId);
                    $(this).addClass('active');
                    showNotification('Property added to comparison');
                }
                
                localStorage.setItem('compareProperties', JSON.stringify(properties));
                updateCompareBadge();
            });

            // Update compare badge
            function updateCompareBadge() {
                const properties = JSON.parse(localStorage.getItem('compareProperties') || '[]');
                const badge = $('.compare-badge');
                
                if (properties.length > 0) {
                    badge.text(properties.length).show();
                } else {
                    badge.hide();
                }
            }

            // Initialize compare badge
            updateCompareBadge();
        },

        /**
         * Favorite properties functionality
         */
        initFavoriteFunctionality: function() {
            // Add to favorites
            $('.action-btn[data-action="favorite"]').on('click', function() {
                const propertyId = $(this).data('property-id');
                const properties = JSON.parse(localStorage.getItem('favoriteProperties') || '[]');
                
                if (properties.includes(propertyId)) {
                    // Remove from favorites
                    const index = properties.indexOf(propertyId);
                    properties.splice(index, 1);
                    $(this).removeClass('active');
                    showNotification('Property removed from favorites');
                } else {
                    // Add to favorites
                    properties.push(propertyId);
                    $(this).addClass('active');
                    showNotification('Property added to favorites');
                }
                
                localStorage.setItem('favoriteProperties', JSON.stringify(properties));
                updateFavoriteBadge();
            });

            // Initialize favorite buttons state
            const favorites = JSON.parse(localStorage.getItem('favoriteProperties') || '[]');
            favorites.forEach(id => {
                $(`.action-btn[data-property-id="${id}"][data-action="favorite"]`).addClass('active');
            });

            function updateFavoriteBadge() {
                const properties = JSON.parse(localStorage.getItem('favoriteProperties') || '[]');
                const badge = $('.favorite-badge');
                
                if (properties.length > 0) {
                    badge.text(properties.length).show();
                } else {
                    badge.hide();
                }
            }
        },

        /**
         * Lazy loading for images
         */
        initLazyLoading: function() {
            if ('IntersectionObserver' in window) {
                const lazyImages = document.querySelectorAll('img[data-src]');
                
                const imageObserver = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            img.src = img.dataset.src;
                            img.classList.remove('lazy');
                            img.classList.add('loaded');
                            imageObserver.unobserve(img);
                        }
                    });
                });
                
                lazyImages.forEach(img => imageObserver.observe(img));
            } else {
                // Fallback for older browsers
                $('img[data-src]').each(function() {
                    $(this).attr('src', $(this).data('src'));
                });
            }
        }
    };

    /**
     * Helper Functions
     */
    
    // Email validation
    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Number animation
    function animateNumber($element, target) {
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                $element.text(target.toLocaleString());
                clearInterval(timer);
            } else {
                $element.text(Math.floor(current).toLocaleString());
            }
        }, 16);
    }

    // Show notification
    function showNotification(message, type = 'success') {
        const notification = $(`
            <div class="notification notification-${type}">
                <i class="fa fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
                <span>${message}</span>
            </div>
        `);
        
        $('body').append(notification);
        
        notification.css({
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            padding: '15px 25px',
            background: type === 'success' ? '#28a745' : '#ffc107',
            color: type === 'success' ? '#fff' : '#212529',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            zIndex: 9999,
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            animation: 'slideIn 0.3s ease'
        });
        
        setTimeout(() => {
            notification.fadeOut(300, function() {
                $(this).remove();
            });
        }, 3000);
    }

    // Add notification animation CSS
    const notificationStyles = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    
    $('head').append(`<style>${notificationStyles}</style>`);

    /**
     * AJAX helpers for API calls
     */
    PremiumWebsite.api = {
        searchProperties: function(filters, callback) {
            $.ajax({
                url: '/api/properties/search',
                method: 'POST',
                data: JSON.stringify(filters),
                contentType: 'application/json',
                success: function(response) {
                    callback(null, response);
                },
                error: function(xhr, status, error) {
                    callback(error, null);
                }
            });
        },

        getProperty: function(propertyId, callback) {
            $.ajax({
                url: `/api/property/${propertyId}`,
                method: 'GET',
                success: function(response) {
                    callback(null, response);
                },
                error: function(xhr, status, error) {
                    callback(error, null);
                }
            });
        },

        getLocations: function(callback) {
            $.ajax({
                url: '/api/locations',
                method: 'GET',
                success: function(response) {
                    callback(null, response);
                },
                error: function(xhr, status, error) {
                    callback(error, null);
                }
            });
        },

        getPropertyTypes: function(callback) {
            $.ajax({
                url: '/api/property-types',
                method: 'GET',
                success: function(response) {
                    callback(null, response);
                },
                error: function(xhr, status, error) {
                    callback(error, null);
                }
            });
        },

        getFeaturedProperties: function(limit, callback) {
            $.ajax({
                url: `/api/featured-properties?limit=${limit}`,
                method: 'GET',
                success: function(response) {
                    callback(null, response);
                },
                error: function(xhr, status, error) {
                    callback(error, null);
                }
            });
        }
    };

    // Expose to global scope
    window.PremiumWebsite = PremiumWebsite;

})(jQuery);

/**
 * Additional utility functions
 */

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Format currency (Ghana Cedi)
function formatCurrency(amount, currency = 'GHS') {
    return new Intl.NumberFormat('en-GH', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// Get URL parameters
function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const result = {};
    for (const [key, value] of params) {
        result[key] = value;
    }
    return result;
}

// Update URL without page reload
function updateUrlParams(params) {
    const url = new URL(window.location);
    Object.keys(params).forEach(key => {
        if (params[key]) {
            url.searchParams.set(key, params[key]);
        } else {
            url.searchParams.delete(key);
        }
    });
    window.history.pushState({}, '', url);
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!');
    }).catch(() => {
        showNotification('Failed to copy', 'error');
    });
}

// Print page
function printPage() {
    window.print();
}

// Social share functions
function shareOnFacebook(url) {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`, '_blank');
}

function shareOnTwitter(url, text) {
    window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`, '_blank');
}

function shareOnWhatsApp(url, text) {
    window.open(`https://wa.me/?text=${encodeURIComponent(text + ' ' + url)}`, '_blank');
}

function shareViaEmail(subject, body) {
    window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}
