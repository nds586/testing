document.addEventListener('DOMContentLoaded', () => {
    setupHeroSearch();
    setupBookingTotal();
    setupDiscountCode();
    setupProviderStart();
    setupStarWidget();
});

function setupHeroSearch() {
    const form = document.querySelector('[data-hero-search-form]');
    if (!form) return;

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const input = form.querySelector('input[name="postcode"]');
        const status = document.querySelector('[data-hero-status]');
        const postcode = input.value.trim() || 'your area';

        status.textContent = `Searching for top-rated cleaners in ${postcode}...`;
        setTimeout(() => {
            window.location.href = form.dataset.redirectUrl;
        }, 1200);
    });
}

function setupBookingTotal() {
    const container = document.querySelector('[data-booking-total]');
    if (!container) return;

    const base = Number(container.dataset.basePrice || '0');
    const totalTarget = container.querySelector('[data-total-value]');
    const checkboxes = container.querySelectorAll('input[type="checkbox"][data-addon-price]');

    const recalc = () => {
        let total = base;
        checkboxes.forEach((checkbox) => {
            if (checkbox.checked) {
                total += Number(checkbox.dataset.addonPrice || '0');
            }
        });
        totalTarget.textContent = `$${total.toFixed(2)}`;
    };

    checkboxes.forEach((checkbox) => checkbox.addEventListener('change', recalc));
    recalc();
}

function setupDiscountCode() {
    const form = document.querySelector('[data-discount-form]');
    if (!form) return;

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const code = form.querySelector('input[name="discount_code"]').value.trim().toUpperCase();
        const subtotal = Number(form.dataset.subtotal || '0');
        let discount = 0;

        if (code === 'VIBE10') discount = subtotal * 0.1;
        if (code === 'EARTH20') discount = subtotal * 0.2;

        form.querySelector('[data-discount-value]').textContent = `-$${discount.toFixed(2)}`;
        form.querySelector('[data-grand-total]').textContent = `$${(subtotal - discount).toFixed(2)}`;
    });
}

function setupProviderStart() {
    const button = document.querySelector('[data-start-cleaning]');
    if (!button) return;

    button.addEventListener('click', () => {
        const stamp = new Date().toLocaleString();
        const label = document.querySelector('[data-started-at]');
        label.textContent = `Cleaning started at ${stamp}`;
    });
}

function setupStarWidget() {
    const wrapper = document.querySelector('[data-star-widget]');
    if (!wrapper) return;

    const input = wrapper.querySelector('input[name="rating"]');
    const stars = wrapper.querySelectorAll('[data-star]');

    const applyStars = (value) => {
        stars.forEach((star) => {
            const active = Number(star.dataset.star) <= value;
            star.classList.toggle('active', active);
        });
    };

    stars.forEach((star) => {
        star.addEventListener('click', () => {
            const value = Number(star.dataset.star);
            input.value = value;
            applyStars(value);
        });
    });

    applyStars(Number(input.value || '0'));
}
