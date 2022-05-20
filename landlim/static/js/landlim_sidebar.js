$(".sidebar-dropdown > a").click(function () {
$(".sidebar-submenu").slideUp(200);
if (
$(this).
parent().
hasClass("active"))
{
    $(".sidebar-dropdown").removeClass("active");
    $(this).
    parent().
    removeClass("active");
} else {
    $(".sidebar-dropdown").removeClass("active");
    $(this).
    next(".sidebar-submenu").
    slideDown(200);
    $(this).
    parent().
    addClass("active");
}
});
$("#show-sidebar").click(function () {
$(".page-wrapper").addClass("toggled");
});
function switchByWidth(){
    if (window.matchMedia('(max-width: 780px)').matches) {
    $("#close-sidebar").click(function () {
    $(".page-wrapper").removeClass("toggled");});
    } else if (window.matchMedia('(min-width:781px)').matches) {
    ;
    }
}
window.onload = switchByWidth;
window.onresize = switchByWidth;