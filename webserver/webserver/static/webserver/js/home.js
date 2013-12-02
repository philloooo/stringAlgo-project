function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){
	$('.search-button').click(function(){
		console.log('clicked')
		$('.search-form').submit();
	})
	// var csrftoken = getCookie('csrftoken');

	// $.ajaxSetup({
	//     // crossDomain: false, // obviates need for sameOrigin test
	//     beforeSend: function(xhr, settings) {
	//         if (!csrfSafeMethod(settings.type)) {
	//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
	//         }
	//     }
	// });
	// $('.search-button').click(function(){
	// 	disease=$('.disease').html()
	// 	$('.disease').html('')
	// 	$.ajax({
	// 		type:"POST",
	// 		url:'search',
	// 	    data:{disease:disease}
	// 	}).done(function(){console.log('succsess')})
	// })
})