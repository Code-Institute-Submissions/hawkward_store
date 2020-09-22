$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
});

function scrollToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
};

const ul = document.getElementById("navUl");
const btns = ul.getElementsByClassName("btn");
for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function () {
        const current = document.getElementsByClassName("activeBtnNavbar");
        current[0].className = current[0].className.replace(" activeBtnNavbar", "");
        this.className += " activeBtnNavbar";
    });
};