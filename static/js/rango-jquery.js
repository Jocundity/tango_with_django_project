$(function() {
    
    $('#about-btn').on('click', function() {
        msgStr = $('#msg').html();
        msgStr = msgStr + ' ooo, fancy!';

        $('#msg').html(msgStr);
    });

    $('#about-btn').removeClass('btn-primary').addClass('btn-success');

    $('p').on({
        mouseenter: function() {
            $('this').css('color', 'red');
        },
        mouseleave: function() {
            $('this').css('color', 'black');
        }
    });
});