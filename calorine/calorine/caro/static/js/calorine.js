/*
 *
 *
 *
 */

var int=self.setInterval(function(){onair()},42000);
var intervall = null;

function fetch(uuid) {
    
    req = new XMLHttpRequest();
    req.open("GET", "/progress", 1);
    req.setRequestHeader("X-Progress-ID", uuid);
    req.onreadystatechange = function () {
	
	if (req.readyState == 4) {
	    
	    if (req.status == 200) {
		
		/* poor-man JSON parser */
		var upload = eval(req.responseText);
		
		document.getElementById('tp').innerHTML = upload.state;
		
		/* change the width if the inner progress-bar */
		if (upload.state == 'done' || upload.state == 'uploading') {
		    
		    bar = document.getElementById('progress_upload');
		    w = 400 * upload.received / upload.size;
		    bar.style.width = w + 'px';
		}
		/* we are done, stop the interval */
		if (upload.state == 'done') {		    
		    window.clearTimeout(interval);
		}
	    }
	}
    }
    req.send(null);
}


function startupload(uuid) {
    $('#progress_filename').html(uuid);
    interval = window.setInterval(
	function () {
	    fetch(uuid);
	},
	1000
    );
}

function enable(obj, value) {

    if (value.length > 0) {
	$('#'+obj).removeAttr('disabled');
    } else {
	$('#'+obj).attr("disabled", 'disabled');	
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
