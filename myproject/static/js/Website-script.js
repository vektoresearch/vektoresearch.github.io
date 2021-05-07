$(document).ready(function() { 
    $('.js--go-to-research').click(function() {
        $('html,body').animate({scrollTop: $('.js--research-section').offset().top}, 1000);
    });

    document.querySelector('.hello').scrollIntoView({
        behavior:'smooth'
    });
    
});