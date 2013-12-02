$(document).ready(function(){
	$(".menu").click(function(){
		var slideMenu=$('.slide-menu')
		if ($('.slide-menu').hasClass('slide')){
			slideMenu.removeClass('slide');
		}
		else {
			slideMenu.addClass('slide');
		}
	})
	$(".slide-menu").click(function(){
		var slideMenu=$('.slide-menu')
		if ($('.slide-menu').hasClass('slide')){
			slideMenu.removeClass('slide');
		}
	})
})