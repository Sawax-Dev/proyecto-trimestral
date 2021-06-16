$(() => {
    $('body').hide().fadeIn(3000);
});

const openSideNav = () => {
    document.getElementById("slide-out").style.width = "250px";
    document.getElementById("content").style.marginLeft = "250px";
    document.getElementById("slide-out").style.backgroundColor = "rgba(0, 0, 0, 0.9)";
}

const closeSideNav = () => {
    document.getElementById("slide-out").style.width = "0";
    document.getElementById("content").style.marginLeft = "0";
}