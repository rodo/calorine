/*
 * Small sample of Leaflet usage
 *
 */
var map = new L.Map('divleaf', {zoomControl: false });

var Url = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

var myAttribution = "Map data &copy; 2011 <a href='http://www.openstreetmap.org/'>OpenStreetMap</a> contributors";

var myLayer = new L.TileLayer(Url, {maxZoom: 18, attribution: myAttribution});

var center = new L.LatLng(45.505, 2.09);

var zoom = 17;

map.setView(center, zoom);

map.addLayer(myLayer);
