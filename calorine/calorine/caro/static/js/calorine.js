
function initboot() {
    $(".collapse").collapse();
    $('.dropdown-toggle').dropdown();
}
    

function add_to_playlist(id) {

    url = '/playlist/add/' + id;

    $.get(url, 
	  function(data) {
	      $('.result').html("ok");	      
	  });
}

function inc_playlist(id) {

    url = '/playlist/inc/' + id;

    $.get(url, 
	  function(data) {
	      $('.result').html("ok");	      
	  });
}

function dec_playlist(id) {

    url = '/playlist/dec/' + id;

    $.get(url, 
	  function(data) {
	      $('.result').html("ok");	      
	  });
}