$(function() {
    $('#like_btn').on('click', function () {
        let catecategoryIdVar;
        catecategoryIdVar = $(this).attr('data-categoryid');

        $.get('/rango/like_category', {'category_id': catecategoryIdVar},
            function(data) {
                $('#like_count').html(data);
                $('#like_btn').hide();
            })
    });

    $('#search-input').keyup(function() {
        let query;
        query = $(this).val();

        $.get('/rango/suggest/',
            {'suggestion': query},
            function(data) {
                $('#categories-listing').html(data);
            })
    });
});