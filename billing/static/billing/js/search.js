document.getElementById('search-input').addEventListener('input', function(e) {
    const searchTerm = this.value.toLowerCase().trim();
    const productCards = document.querySelectorAll('.grid .card');
    let visibleCount = 0;
    
    productCards.forEach(card => {
        const title = card.querySelector('h3')?.textContent?.toLowerCase() || '';
        if (searchTerm === '' || title.includes(searchTerm)) {
            card.style.display = 'block';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });

    const noResults = document.getElementById('no-results');
    if (visibleCount === 0 && searchTerm !== '') {
        if (!noResults) {
            const msg = document.createElement('div');
            msg.id = 'no-results';
            msg.className = 'text-center py-8 text-base-content/60 col-span-full';
            msg.innerHTML = '<p class="text-lg">🔍 No products found for "' + searchTerm + '"</p>';
            document.querySelector('.grid').appendChild(msg);
        } else {
            noResults.innerHTML = '<p class="text-lg">🔍 No products found for "' + searchTerm + '"</p>';
        }
    } else if (noResults) {
        noResults.remove();
    }
});