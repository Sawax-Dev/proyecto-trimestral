$(() => {
    $('body').hide().fadeIn(1500);
});

const openSideNav = () => {
    document.getElementById("slide-out").style.width = "250px";
    document.getElementById("slide-out").style.backgroundColor = "rgba(0, 0, 0, 0.9)";
}

const closeSideNav = () => {
    document.getElementById("slide-out").style.width = "0";
}

const productForm = (event) => {
    event.preventDefault();
    return false
}