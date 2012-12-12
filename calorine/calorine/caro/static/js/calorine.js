
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
              if(data.entry){
                  $('a.'+data.entry.id).hide();
                  $('td.'+data.entry.id).html("<span class='label label-info'>A voté !</span>");
                  $("#message").html("");
		  vote = $('.span_'+id).html();
		  $('.span_'+id).html(parseInt(vote)+1);
              }

              if(data.message){
                  $("#message").html("<span class='label label-info'>"+data.message+"</span>");
              }
	  });
}

function dec_playlist(id) {

    url = '/playlist/dec/' + id;

    $.get(url,
	  function(data) {
              if(data.entry) {
                  $('a.'+data.entry.id).hide();
                  $('td.'+data.entry.id).html("<span class='label label-info'>A voté !</span>");
                  $("#message").html("");

		  vote = parseInt($('.span_'+id).html());
		  if (vote > 0) {
		      $('.span_'+id).html(vote - 1);
		  }

              }
              if(data.message){
                  $("#message").html("<span class='label label-info'>"+data.message+"</span>");
              }
	  });

}
