function validateForm() {
    var searchInput = document.forms["searchForm"]["search"].value;
    if (searchInput.trim() === "") {
        alert("You must enter a word!");
        return false;
    }
}

window.addEventListener("hashchange", function () { scrollBy(0, -50); });
