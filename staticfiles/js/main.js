// Cyberpunk Terminal Theme - Interactive Effects
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle functionality
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
            mobileMenuButton.setAttribute('aria-expanded', !isExpanded);
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // Add copy button to code blocks with cyberpunk styling
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(function(codeBlock) {
        const pre = codeBlock.parentElement;
        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-code-button';
        copyButton.textContent = '[COPY]';
        copyButton.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            padding: 0.5rem 1rem;
            background-color: transparent;
            color: #06b6d4;
            border: 1px solid #06b6d4;
            border-radius: 0.25rem;
            font-size: 0.75rem;
            font-family: 'Courier New', monospace;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        `;
        
        copyButton.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(6, 182, 212, 0.1)';
            this.style.boxShadow = '0 0 10px rgba(6, 182, 212, 0.5)';
            this.style.textShadow = '0 0 10px rgba(6, 182, 212, 0.8)';
        });
        
        copyButton.addEventListener('mouseleave', function() {
            this.style.backgroundColor = 'transparent';
            this.style.boxShadow = 'none';
            this.style.textShadow = 'none';
        });
        
        copyButton.addEventListener('click', function() {
            const code = codeBlock.textContent;
            navigator.clipboard.writeText(code).then(function() {
                copyButton.textContent = '[COPIED]';
                copyButton.style.color = '#14b8a6';
                copyButton.style.borderColor = '#14b8a6';
                setTimeout(function() {
                    copyButton.textContent = '[COPY]';
                    copyButton.style.color = '#06b6d4';
                    copyButton.style.borderColor = '#06b6d4';
                }, 2000);
            }).catch(function(err) {
                console.error('Failed to copy code:', err);
            });
        });
        
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);
        wrapper.appendChild(copyButton);
    });

    // Add glitch effect to main title on hover
    const mainTitle = document.querySelector('h1');
    if (mainTitle) {
        mainTitle.addEventListener('mouseenter', function() {
            this.style.animation = 'glitch 0.3s ease-in-out';
        });
        mainTitle.addEventListener('animationend', function() {
            this.style.animation = '';
        });
    }

    // Terminal cursor effect for buttons - disabled to preserve underscores in button text
    // The hover effects are handled by CSS instead

    // Add typing effect to status bar
    const statusBar = document.querySelector('.status-bar');
    if (statusBar) {
        setInterval(() => {
            const statusElement = statusBar.querySelector('div:last-child span:last-child');
            if (statusElement && statusElement.textContent === 'ONLINE') {
                statusElement.style.opacity = statusElement.style.opacity === '0.5' ? '1' : '0.5';
            }
        }, 1000);
    }
});
