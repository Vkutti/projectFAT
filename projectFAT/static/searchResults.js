const searchResultsContainer = document.getElementById("search-results-container")

const createBusinessCard = (businessName) => {
    const card = document.createElement("div")
    card.className = "card my-2"
    card.innerHTML = `<div class="card-body">
        <h5 class="card-title">${businessName}</h5>
        <h6 class="card-subtitle mb-2 text-body-secondary">Business Description blah blah blah blah</h6>
        <a href="#" class="card-link">View Details</a>
        <a href="#" class="card-link">Contact</a>
    </div>`
    searchResultsContainer.appendChild(card)
}

window.onload = () => {
    const inputPrompt = localStorage.getItem("prompt");
    const searchTitle = document.getElementById("search-title")

    document.title = document.title += " " + inputPrompt
    searchTitle.innerText += " " + inputPrompt
    
    for (let i=1; i<=10; i++) {
        createBusinessCard("Business " + i);
    }
    
}

console.log("Javascript loaded.");