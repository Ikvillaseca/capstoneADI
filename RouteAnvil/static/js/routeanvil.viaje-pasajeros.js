function testload() {
    console.log("test")
}

function toggle(source,pasajero) {
    console.log(source)
    console.log(pasajero)
    checkboxes = document.getElementsByName(pasajero);
    for (var i = 0,
        n = checkboxes.length; i < n; i++) {
        checkboxes[i].checked = source.checked;
    }
}
