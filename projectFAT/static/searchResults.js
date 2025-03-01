// Optimize search results with document fragments for better performance
document.addEventListener('DOMContentLoaded', () => {
    const searchResultsContainer = document.getElementById("search-results-container");
    
    const createBusinessCard = (businessName) => {
        const card = document.createElement("div");
        card.className = "card my-2";
        card.innerHTML = `<div class="card-body">
            <h5 class="card-title">${businessName}</h5>
            <h6 class="card-subtitle mb-2 text-body-secondary">Business Description blah blah blah blah</h6>
            <a href="#" class="card-link">View Details</a>
            <a href="#" class="card-link">Contact</a>
        </div>`;
        return card;
    }
    
    // Get the search prompt from localStorage
    const inputPrompt = localStorage.getItem("prompt");
    const searchTitle = document.getElementById("search-title");
    
    // Update document title
    document.title = document.title + " " + inputPrompt;
    
    // Use document fragment for better performance when adding multiple elements
    const fragment = document.createDocumentFragment();
    
    // Create all business cards and append to fragment
    for (let i = 0; i <= bn; i++) {
        fragment.appendChild(createBusinessCard("Business " + i));
    }
    
    // Add all cards to DOM in a single operation
    searchResultsContainer.appendChild(fragment);
    
    console.log("Search results loaded efficiently.");
});