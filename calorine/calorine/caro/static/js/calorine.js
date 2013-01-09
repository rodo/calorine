/*
 *
 *
 *
 */

var int=self.setInterval(function(){onair()},42000);

var req = new Request({
			  method: 'get',
			  headers: {'X-Progress-ID': uuid},
			  url: '/upload/progress/',
			  initialDelay: 500,
			  delay: 1000,
			  limit: 10000,
			  async: false,
			  onSuccess: function(reply) {
			      test = JSON.decode(reply);
			      switch(test.state) {
			      case "uploading": 
				  percent = 0.00 + parseFloat(Math.floor((test.received / test.size)*1000)/10);
				  $('#progress_filename').set('html','Uploading ' + filename + ' ...' + percent + '%');
				  $('#progress_upload').set('style', 'width: '+ percent);
				  break;
			      case "starting":
				  $('#progress_filename').set('html','Starting Upload... '); 
				  break;
			      case "error":
				  $('#progress_filename').set('html','Upload Error... ' + test.status);
				  break;
			      case "done":
				  $('#progress_filename').set('html','Upload Finished...');
				  req.stopTimer();
				  break;
			      default:
				  console.debug("Oooops!");
				  break;  
			      }
			  }
		      });


function upmeter(uuid) {
    
    req.startTimer('X-Progress-ID=' + uuid);

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
