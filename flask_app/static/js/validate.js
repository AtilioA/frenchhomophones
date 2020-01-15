function validateForm() {
    var x = document.forms["searchForm"]["search"].value;
    if (x.trim() == "") {
        alert("You must enter a word!");
        return false;
    }
}

window.addEventListener("hashchange", function () { scrollBy(0, -50) });
