if (document.location.search.match(/type=embed/gi)) {
window.parent.postMessage("resize", "*");
}
$('document').ready(function() {
var msg = $('#message');
msg.autosize();
});