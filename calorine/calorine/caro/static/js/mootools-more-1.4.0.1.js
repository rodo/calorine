// MooTools: the javascript framework.
// Load this file's selection again by visiting: http://mootools.net/more/086550e82f68aa948f48c2a94742b4dd 
// Or build this file again with packager using: packager build More/More More/Request.JSONP More/Request.Queue More/Request.Periodical
/*
---
copyrights:
  - [MooTools](http://mootools.net)

licenses:
  - [MIT License](http://mootools.net/license.txt)
...
*/
MooTools.More={version:"1.4.0.1",build:"a4244edf2aa97ac8a196fc96082dd35af1abab87"};Request.JSONP=new Class({Implements:[Chain,Events,Options],options:{onRequest:function(a){if(this.options.log&&window.console&&console.log){console.log("JSONP retrieving script with url:"+a);
}},onError:function(a){if(this.options.log&&window.console&&console.warn){console.warn("JSONP "+a+" will fail in Internet Explorer, which enforces a 2083 bytes length limit on URIs");
}},url:"",callbackKey:"callback",injectScript:document.head,data:"",link:"ignore",timeout:0,log:false},initialize:function(a){this.setOptions(a);},send:function(c){if(!Request.prototype.check.call(this,c)){return this;
}this.running=true;var d=typeOf(c);if(d=="string"||d=="element"){c={data:c};}c=Object.merge(this.options,c||{});var e=c.data;switch(typeOf(e)){case"element":e=document.id(e).toQueryString();
break;case"object":case"hash":e=Object.toQueryString(e);}var b=this.index=Request.JSONP.counter++;var f=c.url+(c.url.test("\\?")?"&":"?")+(c.callbackKey)+"=Request.JSONP.request_map.request_"+b+(e?"&"+e:"");
if(f.length>2083){this.fireEvent("error",f);}Request.JSONP.request_map["request_"+b]=function(){this.success(arguments,b);}.bind(this);var a=this.getScript(f).inject(c.injectScript);
this.fireEvent("request",[f,a]);if(c.timeout){this.timeout.delay(c.timeout,this);}return this;},getScript:function(a){if(!this.script){this.script=new Element("script",{type:"text/javascript",async:true,src:a});
}return this.script;},success:function(b,a){if(!this.running){return;}this.clear().fireEvent("complete",b).fireEvent("success",b).callChain();},cancel:function(){if(this.running){this.clear().fireEvent("cancel");
}return this;},isRunning:function(){return !!this.running;},clear:function(){this.running=false;if(this.script){this.script.destroy();this.script=null;
}return this;},timeout:function(){if(this.running){this.running=false;this.fireEvent("timeout",[this.script.get("src"),this.script]).fireEvent("failure").cancel();
}return this;}});Request.JSONP.counter=0;Request.JSONP.request_map={};Class.Mutators.Binds=function(a){if(!this.prototype.initialize){this.implement("initialize",function(){});
}return Array.from(a).concat(this.prototype.Binds||[]);};Class.Mutators.initialize=function(a){return function(){Array.from(this.Binds).each(function(b){var c=this[b];
if(c){this[b]=c.bind(this);}},this);return a.apply(this,arguments);};};Request.Queue=new Class({Implements:[Options,Events],Binds:["attach","request","complete","cancel","success","failure","exception"],options:{stopOnFailure:true,autoAdvance:true,concurrent:1,requests:{}},initialize:function(a){var b;
if(a){b=a.requests;delete a.requests;}this.setOptions(a);this.requests={};this.queue=[];this.reqBinders={};if(b){this.addRequests(b);}},addRequest:function(a,b){this.requests[a]=b;
this.attach(a,b);return this;},addRequests:function(a){Object.each(a,function(c,b){this.addRequest(b,c);},this);return this;},getName:function(a){return Object.keyOf(this.requests,a);
},attach:function(a,b){if(b._groupSend){return this;}["request","complete","cancel","success","failure","exception"].each(function(c){if(!this.reqBinders[a]){this.reqBinders[a]={};
}this.reqBinders[a][c]=function(){this["on"+c.capitalize()].apply(this,[a,b].append(arguments));}.bind(this);b.addEvent(c,this.reqBinders[a][c]);},this);
b._groupSend=b.send;b.send=function(c){this.send(a,c);return b;}.bind(this);return this;},removeRequest:function(b){var a=typeOf(b)=="object"?this.getName(b):b;
if(!a&&typeOf(a)!="string"){return this;}b=this.requests[a];if(!b){return this;}["request","complete","cancel","success","failure","exception"].each(function(c){b.removeEvent(c,this.reqBinders[a][c]);
},this);b.send=b._groupSend;delete b._groupSend;return this;},getRunning:function(){return Object.filter(this.requests,function(a){return a.running;});
},isRunning:function(){return !!(Object.keys(this.getRunning()).length);},send:function(b,a){var c=function(){this.requests[b]._groupSend(a);this.queue.erase(c);
}.bind(this);c.name=b;if(Object.keys(this.getRunning()).length>=this.options.concurrent||(this.error&&this.options.stopOnFailure)){this.queue.push(c);}else{c();
}return this;},hasNext:function(a){return(!a)?!!this.queue.length:!!this.queue.filter(function(b){return b.name==a;}).length;},resume:function(){this.error=false;
(this.options.concurrent-Object.keys(this.getRunning()).length).times(this.runNext,this);return this;},runNext:function(a){if(!this.queue.length){return this;
}if(!a){this.queue[0]();}else{var b;this.queue.each(function(c){if(!b&&c.name==a){b=true;c();}});}return this;},runAll:function(){this.queue.each(function(a){a();
});return this;},clear:function(a){if(!a){this.queue.empty();}else{this.queue=this.queue.map(function(b){if(b.name!=a){return b;}else{return false;}}).filter(function(b){return b;
});}return this;},cancel:function(a){this.requests[a].cancel();return this;},onRequest:function(){this.fireEvent("request",arguments);},onComplete:function(){this.fireEvent("complete",arguments);
if(!this.queue.length){this.fireEvent("end");}},onCancel:function(){if(this.options.autoAdvance&&!this.error){this.runNext();}this.fireEvent("cancel",arguments);
},onSuccess:function(){if(this.options.autoAdvance&&!this.error){this.runNext();}this.fireEvent("success",arguments);},onFailure:function(){this.error=true;
if(!this.options.stopOnFailure&&this.options.autoAdvance){this.runNext();}this.fireEvent("failure",arguments);},onException:function(){this.error=true;
if(!this.options.stopOnFailure&&this.options.autoAdvance){this.runNext();}this.fireEvent("exception",arguments);}});Request.implement({options:{initialDelay:5000,delay:5000,limit:60000},startTimer:function(b){var a=function(){if(!this.running){this.send({data:b});
}};this.lastDelay=this.options.initialDelay;this.timer=a.delay(this.lastDelay,this);this.completeCheck=function(c){clearTimeout(this.timer);this.lastDelay=(c)?this.options.delay:(this.lastDelay+this.options.delay).min(this.options.limit);
this.timer=a.delay(this.lastDelay,this);};return this.addEvent("complete",this.completeCheck);},stopTimer:function(){clearTimeout(this.timer);return this.removeEvent("complete",this.completeCheck);
}});