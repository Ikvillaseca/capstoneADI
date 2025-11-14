
document.addEventListener('DOMContentLoaded', function() {
    
    animateStatCards();
    
    initParallaxEffect();
    
});


function animateStatCards() {
    const statCards = document.querySelectorAll('.stat-card');
    
    if (statCards.length === 0) return; 
    
    statCards.forEach((card, index) => {
        setTimeout(() => {
        
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        }, index * 100);
    });
}


function initParallaxEffect() {
    const heroSection = document.querySelector('.hero-section');
    
    if (!heroSection) return; 
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5; 
        heroSection.style.transform = `translateY(${rate}px)`;
    });
}


function animateCounters() {
    const counters = document.querySelectorAll('.stat-card h4');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        let current = 0;
        const increment = target / 50; 
        
        const updateCounter = () => {
            if (current < target) {
                current += increment;
                counter.textContent = Math.ceil(current);
                setTimeout(updateCounter, 20);
            } else {
                counter.textContent = target;
            }
        };
        
        updateCounter();
    });
}


function observeElements() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    });
    
    const serviceCards = document.querySelectorAll('.card-hover');
    serviceCards.forEach(card => observer.observe(card));
}