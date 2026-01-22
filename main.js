// Simple ShopEase JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // 1. Cart Count with Pulse Animation
    updateCart();
    
    // 2. Simple Quantity Controls
    setupQuantityButtons();
    
    // 3. Add to Cart Animation
    setupAddToCart();
    
    // 4. Smooth Hover Effects
    setupCardHover();
});

// Update cart count with simple animation
function updateCart() {
    const cartCount = document.getElementById('cartCount');
    if (!cartCount) return;
    
    fetch('/api/cart_count')
        .then(response => response.json())
        .then(data => {
            cartCount.textContent = data.count;
            
            // Simple pulse animation when count changes
            cartCount.classList.add('pulse');
            setTimeout(() => cartCount.classList.remove('pulse'), 300);
            
        });
}

// Update cart every 10 seconds
setInterval(updateCart, 10000);

// Simple quantity controls
function setupQuantityButtons() {
    document.querySelectorAll('.qty-minus').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.nextElementSibling;
            if (input.value > 1) input.value = parseInt(input.value) - 1;
        });
    });
    
    document.querySelectorAll('.qty-plus').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.previousElementSibling;
            input.value = parseInt(input.value) + 1;
        });
    });
}

// Add to cart with simple feedback
function setupAddToCart() {
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '✓ Added!';
            this.style.background = '#28a745';
            
            setTimeout(() => {
                this.innerHTML = originalText;
                this.style.background = '';
                updateCart(); // Update cart count
            }, 1500);
        });
    });
}

// Simple card hover effect
function setupCardHover() {
    document.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Simple form validation
function validateForm(form) {
    let isValid = true;
    form.querySelectorAll('[required]').forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = 'red';
            isValid = false;
        } else {
            input.style.borderColor = '';
        }
    });
    return isValid;
}
