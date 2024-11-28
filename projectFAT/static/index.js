console.log('Loading Javascript..')

const categories = ["Salon", "Tutor", "Catering", "Daycare", "Boutiques"]
const categoryBtnContainer = document.getElementById("category-btns")
const createCategoryBtn = (categoryName) => {
    const btn = document.createElement("button")
    btn.className = "btn btn-primary rounded category-btn mx-1"
    btn.style = "width: 7rem; height: 2.6rem"
    btn.innerHTML = categoryName
    categoryBtnContainer.appendChild(btn)
}
categories.forEach((val, ind) => {
    createCategoryBtn(val);
})


const promptInput = document.getElementById("prompt-input")

const enterPrompt = () => {
    const inputVal = promptInput.value
    if (inputVal == "") return;
    console.log("inputting: " + inputVal);
    localStorage.setItem("prompt", inputVal)

    window.location.href = '/templates/searchResults.html';
}

promptInput.addEventListener("keypress", (event) => {
    if (event.keyCode == 13) {
        enterPrompt();
    }
})

console.log('Javascript loaded.')
