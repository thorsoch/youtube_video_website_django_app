$(document).ready(function() {
    $('.thumbnail').mouseover(function() {
        $(this).fadeTo('fast', 0.5);
    });
    $('.thumbnail').mouseleave(function() {
        $(this).fadeTo(50, 1);
    })
});