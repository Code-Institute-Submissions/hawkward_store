$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
});

function scrollToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
};

const navUl = document.getElementById("navUl");
const navBtns = navUl.getElementsByClassName("btn");
for (var i = 0; i < navBtns.length; i++) {
    navBtns[i].addEventListener("click", function () {
        const current = document.getElementsByClassName("activeBtnNavbar");
        current[0].className = current[0].className.replace(" activeBtnNavbar", "");
        this.className += " activeBtnNavbar";
    });
};
