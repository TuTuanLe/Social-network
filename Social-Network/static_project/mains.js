$(document).ready(function(){
    console.log('hello world')
    $('#modal-btn').click(function(){
        console.log('working')
        $('.ui.modal')
        .modal('show')
        ;
    })

    // $('.header_option').onclick(function(){
    //     console.log('ltt')
    //     $(this).toggleClass('header_option header_option--active');
    // });


})