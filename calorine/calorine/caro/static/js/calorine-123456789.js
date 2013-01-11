/*
 *
 *
 *
 */
onair();

var int=self.setInterval(function(){onair()},42000);
var intervall = null;

function fetchjson(uuid) {
    
    $.ajax({url: '/progress',
	    headers: { 'X-Progress-ID': uuid },
	    success: function(data) {

		$('#progress_status').html(data.state);

		if (data.state == 'done' || data.state == 'uploading') {
		    w = (100 * upload.received / upload.size) + '%';
		    $('#progress_upload').css('width', w);
		}

		/* we are done, stop the interval */
		if (data.state == 'done') {		    
		    window.clearTimeout(interval);
		}
	    }
	  }
	  );
}


function startupload(uuid) {
    interval = window.setInterval(
	function () {
	    fetchjson(uuid);
	},
	500
    );
}

function enable(obj, value) {

    if (value.length > 0) {
	$('#'+obj).removeAttr('disabled');
    } else {
	$('#'+obj).attr("disabled", 'disabled');	
    }
}

function onairbutton(id, user_vote) {
    /*
     * Update on air vote button
     * 
     */
    if (user_vote == 'null') {
	$('#onairplus').css('visibility', 'visible');
	$('#onairstop').css('visibility', 'visible');
	$('#onairplus').attr("onclick" ,"inc_onair("+id+")");
	$('#onairstop').attr("onclick", "dec_onair("+id+")");	
    } else {
	$('#onairplus').css('visibility', 'hidden');
	$('#onairstop').css('visibility', 'hidden');
    }
}

function inc_onair(id) {

    if (id > 0) {

	$('#onairplus').css('visibility', 'hidden');
	$('#onairstop').css('visibility', 'hidden');

	url = '/songvote/inc/' + id;

	$.get(url,
	      function(data) {
		  if(data.entry){
		      $('#onairbuttons').html(" - score " + data.entry.score);
		  }
	      });
    }
}

function dec_onair(id) {
    if (id > 0 ) {
	
	$('#onairplus').css('visibility', 'hidden');
	$('#onairstop').css('visibility', 'hidden');

	url = '/songvote/dec/' + id;

	$.get(url,
	      function(data) {
		  if(data.entry){
		      $('#onairbuttons').html(" - score " + data.entry.score);
		  }
	      });
    }
}


function onair() {

    url = '/onair.json';

    $.get(url,
	  function(data) {
	      text = "On air :";
              text = text + " " + data.artist;
              text = text + " - " + data.title;
	      if (data.album) {
		  text = text + " - " + data.album;		  
	      }

	      onairbutton(data.songid, data.user_vote);
	      $("#onair").html(text);
	  });
}

function initboot() {
    $(".collapse").collapse();
    $('.dropdown-toggle').dropdown();
}


function add_to_playlist(id) {

    url = '/playlist/add/' + id;

    $('.btn_'+id).addClass("btn-info");
    $('.btn_'+id).removeClass("btn-primary");

    $.get(url,
	  function(data) {
	      $('.result').html("ok");
	      $('.btn_'+id).addClass("disabled");
	      $('.btn_'+id).removeClass("btn-info");
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
