var map;
var center = new google.maps.LatLng(41.878114, -87.629798);

function initialize() {
  // http://stackoverflow.com/questions/6588549/make-google-maps-plugin-black-white-or-with-sepia-filter
  var roadAtlasStyles = [
    {
      "featureType": "road.highway",
      "elementType": "geometry",
      "stylers": [
        { "saturation": -100 },
        { "lightness": -8 },
        { "gamma": 1.18 }
      ]
    }, {
      "featureType": "road.arterial",
      "elementType": "geometry",
      "stylers": [
        { "saturation": -100 },
        { "gamma": 1 },
        { "lightness": -24 }
      ]
    }, {
      "featureType": "poi",
      "elementType": "geometry",
      "stylers": [
        { "saturation": -100 }
      ]
    }, {
      "featureType": "administrative",
      "stylers": [
        { "saturation": -100 }
      ]
    }, {
      "featureType": "transit",
      "stylers": [
        { "saturation": -100 }
      ]
    }, {
      "featureType": "water",
      "elementType": "geometry.fill",
      "stylers": [
        { "saturation": -100 }
      ]
    }, {
      "featureType": "road",
      "stylers": [
        { "saturation": -100 }
      ]
    }, {
      "featureType": "administrative",
      "stylers": [
        { "saturation": -100 }
      ]
    }, {
      "featureType": "landscape",
      "stylers": [
        { "saturation": -100 }
      ]
    }, {
      "featureType": "poi",
      "stylers": [
        { "saturation": -100 }
      ]
    }
  ];

  var mapOptions = {
    zoom: 14,
    center: center,
    mapTypeControlOptions: {
      mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'usroadatlas']
    },

    // customize controls
    mapTypeControl: false,
    panControl: false,
    streetViewControl: false,
    zoomControlOptions: {
      style: google.maps.ZoomControlStyle.SMALL
    }
  };
  map = new google.maps.Map($('#map-canvas')[0], mapOptions);
  var styledMapOptions = {};
  var usRoadMapType = new google.maps.StyledMapType(roadAtlasStyles, styledMapOptions);
  map.mapTypes.set('usroadatlas', usRoadMapType);
  map.setMapTypeId('usroadatlas');
}

google.maps.event.addDomListener(window, 'load', initialize);