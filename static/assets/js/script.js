document.addEventListener('DOMContentLoaded', () => {
    // Popup Logic
    const popUp = document.getElementById('pop-up');
    const showPopup = document.getElementById('show-pop-up');
    const hidePopup = document.getElementById('x');

    if (popUp && showPopup && hidePopup) {
        const show = () => {
            popUp.classList.remove('hidden');
        };

        const hide = () => {
            popUp.classList.add('hidden');
        };

        showPopup.addEventListener('click', show);
        hidePopup.addEventListener('click', hide);
    }

    // Basket Logic
    const basket = document.getElementById('basket');
    const basketIcon = document.getElementById('basketIcon');

    if (basket && basketIcon) {
        const toggleBasket = () => {
            basket.classList.toggle('hidden');
        };

        basketIcon.addEventListener('click', toggleBasket);
    }

    // Quantity Increment/Decrement Logic
    const incrementButton = document.getElementById('increment');
    const decrementButton = document.getElementById('decrement');
    const quantityInput = document.getElementById('quantity');
    const ticketPriceElement = document.getElementById('ticket-price');
    const totalPriceElement = document.getElementById('total-price');
  
    if (incrementButton && decrementButton && quantityInput && ticketPriceElement && totalPriceElement) {
        const ticketPrice = parseFloat(ticketPriceElement.textContent); // Base price per ticket
  
        const updateTotalPrice = () => {
            const quantity = parseInt(quantityInput.value);
            const totalPrice = (ticketPrice * quantity).toFixed(2); // Calculate total price
            totalPriceElement.textContent = totalPrice; // Update total price in the UI
        };
  
        incrementButton.addEventListener('click', () => {
            let value = parseInt(quantityInput.value);
            if (value < 75) {
                quantityInput.value = value + 1;
                updateTotalPrice(); // Update total price when quantity changes
            }
        });
  
        decrementButton.addEventListener('click', () => {
            let value = parseInt(quantityInput.value);
            if (value > 1) {
                quantityInput.value = value - 1;
                updateTotalPrice(); // Update total price when quantity changes
            }
        });
  
        quantityInput.addEventListener('input', updateTotalPrice); // Update total price when user manually inputs quantity
    }
  

    // Mobile Menu Toggle Logic
    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');

    if (menuToggle && mobileMenu) {
        const toggleMenu = () => {
            mobileMenu.classList.toggle('hidden');
        };

        menuToggle.addEventListener('click', toggleMenu);
    }

    // Quick Select Links Logic
    const ticketInput = document.getElementById('quantity');
    const quickSelectLinks = document.querySelectorAll('.quick-select');
  
    if (quantityInput && quickSelectLinks) {
        quickSelectLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault(); // Prevent default link behavior
                const value = e.target.getAttribute('data-value');
                quantityInput.value = value; // Set the input value
                const event = new Event('input'); // Trigger input event to recalculate the total
                quantityInput.dispatchEvent(event);
            });
        });
    }
});


