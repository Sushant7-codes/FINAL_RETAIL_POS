document.addEventListener('DOMContentLoaded', function() {
    const savedScrollPosition = sessionStorage.getItem('billingPageScrollPosition');
    if (savedScrollPosition) {
        window.scrollTo(0, parseInt(savedScrollPosition));
        sessionStorage.removeItem('billingPageScrollPosition');
    }
});