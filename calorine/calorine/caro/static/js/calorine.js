
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