
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
                  $('a.'+data.entry.id).removeClass("btn-success")
                  $('td.'+data.entry.id).html(data.entry.score+"<span class='label label-info'>A voté !</span>");
                  $("#message").html("");
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
              if(data.entry){
                  $('a.'+data.entry.id).removeClass("btn-danger")
          $('td.'+data.entry.id).html(data.entry.score+"<span class='label label-info'>A voté !</span>");
                  $("#message").html("");
                  }
              if(data.message){
                  $("#message").html("<span class='label label-info'>"+data.message+"</span>");
              }
	  });

}
