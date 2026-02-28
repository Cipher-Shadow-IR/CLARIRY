/* script.js - CLARIRY Cosmic Theme Interactions */

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. INITIALIZE AOS
    if (window.AOS) {
        AOS.init({
            duration: 1000,
            once: true,
            easing: 'ease-out-cubic'
        });
    }

    // 2. PRELOADER
    const preloader = document.getElementById('preloader');
    window.addEventListener('load', () => {
        setTimeout(() => {
            preloader.style.opacity = '0';
            preloader.style.visibility = 'hidden';
            document.body.style.overflow = 'auto';
        }, 1200); 
    });

    // 3. CUSTOM CURSOR
    const cursor = document.querySelector('.cursor');
    const glow = document.querySelector('.cursor-glow');
    
    if(window.innerWidth > 768) {
        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
            
            glow.animate({
                left: `${e.clientX}px`,
                top: `${e.clientY}px`
            }, { duration: 800, fill: "forwards" });
        });

        const hoverElements = document.querySelectorAll('a, .btn, .glass-panel, .step-marker');
        
        hoverElements.forEach(el => {
            el.addEventListener('mouseenter', () => {
                cursor.style.transform = 'translate(-50%, -50%) scale(2)';
                cursor.style.backgroundColor = 'var(--knowledge-blue)';
            });
            el.addEventListener('mouseleave', () => {
                cursor.style.transform = 'translate(-50%, -50%) scale(1)';
                cursor.style.backgroundColor = 'var(--text-main)';
            });
        });
    } else {
        cursor.style.display = 'none';
        glow.style.display = 'none';
    }

    // 4. NAV SCROLL EFFECT
    const nav = document.querySelector('.glass-nav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.style.background = 'rgba(2, 6, 23, 0.9)';
            nav.style.padding = '10px 0';
            nav.style.boxShadow = '0 10px 30px rgba(0,0,0,0.5)';
        } else {
            nav.style.background = 'rgba(2, 6, 23, 0.6)';
            nav.style.padding = '15px 0';
            nav.style.boxShadow = 'none';
        }
    });

    // 5. STARFIELD CANVAS ANIMATION
    const canvas = document.getElementById('starfield');
    if(canvas) {
        const ctx = canvas.getContext('2d');
        let width, height, stars;

        function initStars() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            stars = [];
            const numStars = window.innerWidth < 768 ? 50 : 150;
            
            for(let i=0; i<numStars; i++) {
                stars.push({
                    x: Math.random() * width,
                    y: Math.random() * height,
                    size: Math.random() * 2,
                    speedY: Math.random() * 0.2 + 0.05,
                    opacity: Math.random()
                });
            }
        }

        function drawStars() {
            ctx.clearRect(0, 0, width, height);
            ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
            
            stars.forEach(star => {
                ctx.globalAlpha = star.opacity;
                ctx.beginPath();
                ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
                ctx.fill();
                
                // Move star
                star.y -= star.speedY;
                
                // Twinkle
                star.opacity += (Math.random() - 0.5) * 0.05;
                if(star.opacity < 0.1) star.opacity = 0.1;
                if(star.opacity > 1) star.opacity = 1;
                
                // Reset if off screen
                if(star.y < 0) {
                    star.y = height;
                    star.x = Math.random() * width;
                }
            });
            
            requestAnimationFrame(drawStars);
        }

        initStars();
        drawStars();

        window.addEventListener('resize', () => {
            initStars();
        });
    }

});
