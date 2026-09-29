// ============================================
// SCROLL ANIMATIONS & INTERACTIVE EFFECTS
// Proyecto Digital - Modern JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // --- INTERSECTION OBSERVER FOR SCROLL ANIMATIONS ---
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Add staggered animation for list items
                if (entry.target.tagName === 'SECTION') {
                    const listItems = entry.target.querySelectorAll('ul li');
                    listItems.forEach((item, index) => {
                        setTimeout(() => {
                            item.style.animation = `fadeInUp 0.6s ease-out forwards`;
                            item.style.opacity = '1';
                        }, index * 100);
                    });
                }
            }
        });
    }, observerOptions);

    // Observe all sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        observer.observe(section);
    });

    // --- PARALLAX EFFECT FOR IMAGES ---
    const parallaxImages = document.querySelectorAll('#tu_negocio section img');
    
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        
        parallaxImages.forEach(img => {
            const rect = img.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                const speed = 0.5;
                const yPos = -(rect.top * speed);
                img.style.transform = `translateY(${yPos}px) scale(1.1)`;
            }
        });
    });

    // --- SMOOTH HOVER EFFECTS FOR PORTFOLIO ITEMS ---
    const portfolioItems = document.querySelectorAll('section ul li');
    
    portfolioItems.forEach(item => {
        item.addEventListener('mouseenter', function(e) {
            const rect = item.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('div');
            ripple.style.position = 'absolute';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.background = 'rgba(0, 224, 234, 0.6)';
            ripple.style.borderRadius = '50%';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.transform = 'translate(-50%, -50%) scale(0)';
            ripple.style.animation = 'ripple 0.6s ease-out';
            ripple.style.pointerEvents = 'none';
            
            item.style.position = 'relative';
            item.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });

        // 3D tilt effect
        item.addEventListener('mousemove', function(e) {
            const rect = item.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            item.style.transform = `
                translateY(-10px) 
                scale(1.02) 
                perspective(1000px) 
                rotateX(${rotateX}deg) 
                rotateY(${rotateY}deg)
            `;
        });
        
        item.addEventListener('mouseleave', function() {
            item.style.transform = 'translateY(0) scale(1) perspective(1000px) rotateX(0) rotateY(0)';
        });
    });

    // --- ANIMATED COUNTER (if you want to add statistics) ---
    function animateCounter(element, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);
        
        const counter = setInterval(() => {
            start += increment;
            if (start >= target) {
                element.textContent = Math.round(target);
                clearInterval(counter);
            } else {
                element.textContent = Math.round(start);
            }
        }, 16);
    }

    // --- FORM VALIDATION WITH VISUAL FEEDBACK ---
    const contactForm = document.querySelector('form#contacto');
    
    if (contactForm) {
        const inputs = contactForm.querySelectorAll('input, textarea');
        
        inputs.forEach(input => {
            // Real-time validation
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('error')) {
                    validateField(this);
                }
            });
        });
        
        contactForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Por favor, completa todos los campos correctamente', 'error');
            } else {
                showNotification('Enviando mensaje...', 'info');
            }
        });
    }

    function validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        
        // Remove previous error
        field.classList.remove('error');
        const existingError = field.parentElement.querySelector('.error-message');
        if (existingError) existingError.remove();
        
        // Validate based on field type
        if (field.hasAttribute('required') && value === '') {
            isValid = false;
            showFieldError(field, 'Este campo es obligatorio');
        } else if (field.type === 'email' && value !== '') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                showFieldError(field, 'Email inválido');
            }
        } else if (field.type === 'tel' && value !== '') {
            const phoneRegex = /^[\d\s\-\+\(\)]+$/;
            if (!phoneRegex.test(value) || value.length < 10) {
                isValid = false;
                showFieldError(field, 'Teléfono inválido');
            }
        }
        
        if (isValid) {
            field.style.borderColor = 'rgba(0, 224, 234, 0.5)';
            field.style.boxShadow = '0 0 10px rgba(0, 224, 234, 0.2)';
        }
        
        return isValid;
    }

    function showFieldError(field, message) {
        field.classList.add('error');
        field.style.borderColor = '#ff4444';
        field.style.boxShadow = '0 0 10px rgba(255, 68, 68, 0.3)';
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.color = '#ff4444';
        errorDiv.style.fontSize = '0.9rem';
        errorDiv.style.marginTop = '5px';
        errorDiv.style.animation = 'fadeIn 0.3s ease-out';
        
        field.parentElement.appendChild(errorDiv);
    }

    // --- NOTIFICATION SYSTEM ---
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            background: ${type === 'error' ? '#ff4444' : type === 'success' ? '#00b09f' : '#00b0b9'};
            color: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            z-index: 10000;
            animation: slideInRight 0.5s ease-out;
            font-weight: 600;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.5s ease-out';
            setTimeout(() => notification.remove(), 500);
        }, 3000);
    }

    // --- NEWSLETTER FORM HANDLER ---
    const newsletterForm = document.querySelector('#newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            const emailInput = this.querySelector('#newsletter-email');
            const email = emailInput.value.trim();
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (!emailRegex.test(email)) {
                e.preventDefault();
                emailInput.style.borderColor = '#ff4444';
                showNotification('Por favor, ingresa un email válido', 'error');
            }
        });
    }

    // --- HEADER BACKGROUND ON SCROLL (OPTIONAL - DISABLED TO AVOID CONTENT OVERLAP) ---
    // Si quieres un header que cambie al hacer scroll, descomenta este código
    // y agrega padding-top al body para compensar la altura del header
    /*
    const header = document.querySelector('header');
    let lastScroll = 0;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            header.style.background = 'rgba(10, 10, 10, 0.95)';
            header.style.backdropFilter = 'blur(20px)';
            header.style.boxShadow = '0 5px 30px rgba(0, 176, 185, 0.3)';
            // No cambiar a fixed para evitar que cubra el contenido
        } else {
            header.style.background = 'linear-gradient(135deg, rgba(0, 176, 185, 0.1) 0%, transparent 100%)';
            header.style.backdropFilter = 'none';
            header.style.boxShadow = 'none';
        }
        
        lastScroll = currentScroll;
    });
    */

    // --- SCROLL TO TOP BUTTON ---
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.innerHTML = '↑';
    scrollToTopBtn.id = 'scroll-to-top';
    scrollToTopBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #00b0b9, #008a91);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 24px;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 1000;
        box-shadow: 0 5px 20px rgba(0, 176, 185, 0.4);
    `;
    
    document.body.appendChild(scrollToTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 500) {
            scrollToTopBtn.style.opacity = '1';
            scrollToTopBtn.style.visibility = 'visible';
        } else {
            scrollToTopBtn.style.opacity = '0';
            scrollToTopBtn.style.visibility = 'hidden';
        }
    });
    
    scrollToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    scrollToTopBtn.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1) translateY(-5px)';
        this.style.boxShadow = '0 10px 30px rgba(0, 176, 185, 0.6)';
    });
    
    scrollToTopBtn.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1) translateY(0)';
        this.style.boxShadow = '0 5px 20px rgba(0, 176, 185, 0.4)';
    });

    // --- MOBILE MENU CLOSE ON LINK CLICK ---
    const checkbox = document.getElementById('checkbox');
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (checkbox && window.innerWidth <= 860) {
                checkbox.checked = false;
            }
        });
    });

    // --- ADD LOADING ANIMATION ---
    window.addEventListener('load', function() {
        document.body.style.opacity = '0';
        setTimeout(() => {
            document.body.style.transition = 'opacity 1s ease-out';
            document.body.style.opacity = '1';
        }, 100);
    });

    // --- TYPING EFFECT FOR H1 (OPTIONAL) ---
    const h1Element = document.querySelector('h1');
    if (h1Element && h1Element.textContent) {
        const originalText = h1Element.textContent;
        h1Element.textContent = '';
        h1Element.style.display = 'block';
        
        let charIndex = 0;
        const typingInterval = setInterval(() => {
            if (charIndex < originalText.length) {
                h1Element.textContent += originalText[charIndex];
                charIndex++;
            } else {
                clearInterval(typingInterval);
            }
        }, 50);
    }

    // --- ADDITIONAL CSS ANIMATIONS ---
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: translate(-50%, -50%) scale(20);
                opacity: 0;
            }
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    console.log('🚀 Proyecto Digital - Animations Loaded Successfully!');
});