var meetupApiUrl = 'http://api.meetup.com/2/open_events?status=upcoming&radius=5&category=34&and_text=False&limited_events=False&text=coding+programming+ruby+python+javascript+html&desc=False&offset=0&photo-host=public&format=json&lat=41.878114&page=100&lon=-87.629798&sig_id=178346822&sig=1a186723262b63d4b2deee474b8d95bc0ec2ec9f';

String.prototype.titleize = function() {
  var words = this.split(' ');
  var array = [];
  var firstLetter, remainder;
  for (var i=0; i<words.length; ++i) {
    firstLetter = words[i].charAt(0).toUpperCase();
    if (this == this.toUpperCase() && this.length > 10) {
      remainder = words[i].toLowerCase().slice(1);
    } else {
      remainder = words[i].slice(1);
    }
    array.push(firstLetter + remainder);
  }
  return array.join(' ');
};

String.prototype.contains = function(other) {
  return this.indexOf(other) !== -1;
};

// corner model constructor, where `venueObject` == sub-item from Meetup API `open_venue` JSON response
var Corner = function(venueObject) {
  var self = this;

  // load and check for latitude/longitude and set to `location`
  self.lat = venueObject.lat;
  self.lon = venueObject.lon;
  self.location = ko.computed(function() {
    if (self.lat === 0 || self.lon === 0) {
      return null;
    } else {
      return new google.maps.LatLng(self.lat, self.lon);
    }
  });

  // load metadata
  // self.id = ko.observable(venueObject.id);
  self.id = venueObject.id;
  self.name = ko.observable(venueObject.name.titleize());
  self.address = ko.observable(venueObject.address_1);

  // initialize empty meetup
  self.meetups = ko.observableArray([]);
};

// meetup model constructor, where `meetup` == item from Meetup API `open_venue` JSON response
var Meetup = function(meetup) {
  var self = this;

  // attach venue object
  self.venueObject = meetup.venue;
  self.hasVenue = ko.computed(function() {
    if (self.venueObject) {
      return true;
    } else {
      return false;
    }
  });

  // load metadata
  self.id = ko.observable(meetup.id);
  self.name = ko.observable(meetup.name.titleize());
  self.group = ko.observable(meetup.group.name);
  self.date = ko.computed(function() {
    var milliseconds = meetup.time;
    var date = new Date(milliseconds);
    return date.toLocaleDateString();
  });
  self.url = ko.observable(meetup.event_url);
};

// main application View Model
var ViewModel = function() {
  var self = this;
  var map;
  var mapCanvas = $('#map-canvas')[0];
  var center = new google.maps.LatLng(41.878114, -87.629798); // Chicago City Center
  var infoWindow = new google.maps.InfoWindow();

  self.meetupList = ko.observableArray([]);
  self.cornerList = ko.observableArray([]);

  /* SEARCH */

  // initialize search query to empty
  self.query = ko.observable('');

  // initialize selected corner
  self.selectedCorner = ko.observable();

  self.search = function() {};

  self.filteredCornerList = ko.computed(function() {
    return ko.utils.arrayFilter(self.cornerList(), function(corner) {
      return corner.name().toLowerCase().contains(self.query());
    });
  });

  console.log(self.filteredCornerList());

  /* INITIALIZATION */

  function initialize() {
    drawMap(center, mapCanvas);
    fetchMeetups(meetupApiUrl);
  }

  /* GOOGLE MAPS */

  // creates a black and white google map centered on 'center' onto the 'element' DOM element
  function drawMap(center, element) {
    // styling elements from http://stackoverflow.com/questions/6588549/make-google-maps-plugin-black-white-or-with-sepia-filter
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

    map = new google.maps.Map(element, mapOptions);
    var styledMapOptions = {};
    var usRoadMapType = new google.maps.StyledMapType(roadAtlasStyles, styledMapOptions);
    map.mapTypes.set('usroadatlas', usRoadMapType);
    map.setMapTypeId('usroadatlas');
  }

  // create a map marker
  function addMarker(corner) {
    if (corner.location()) {
      var marker = new google.maps.Marker({
        position: corner.location(),
        map: map,
      });
      google.maps.event.addListener(marker, 'click', function () {
        console.log('Clicked!');
      });
    }
  }

  /* MEETUP */

  // fetch meetups via JSON-P from Meetup API
  function fetchMeetups(url) {
    var data;

    // execute JSON-P request
    $.ajax({
      type: "GET",
      url: url,
      timeout: 5000,
      contentType: "application/json",
      dataType: "jsonp",
      cache: false,

    // when done
    }).done(function(response) {
      // pull `results` array from JSON
      data = response.results;
      console.log(data.length + ' meetups fetched...');

      // loop through results and populate `meetupList`
      data.forEach(function(meetup) {
        self.meetupList.push(new Meetup(meetup));
      });

      // run the `extractCorners` function to pull location data
      extractCorners();

    // if failed
    }).fail(function(response, status, error) {
      // TODO: write error state to DOM
      console.log(error);
    });
  }

  // parse through `meetupList` and extract `Corner` objects
  function extractCorners() {
    // loop through meetup list
    self.meetupList().forEach(function(meetup){
      // check if meetup object has a valid venue id
      if (meetup.hasVenue()) {
        var corner;
        var id = meetup.venueObject.id;

        // if exists
        if (hasCornerId(id)) {
          // push the meetup object onto the corner's meetups
          corner = getCornerById(id);
          corner.meetups.push(meetup);

        // if does not exist
        } else {
          // instantiate a new corner object and push it to the corner list
          corner = new Corner(meetup.venueObject);
          self.cornerList.push(corner);

          // and push the meetup object onto that new corner object
          corner.meetups.push(meetup);

          // add a marker
          addMarker(corner);
        }
      }
    });
    console.log(self.cornerList().length + ' unique corners fetched...');
  }

  // checks if a specific corner by `id` already exists in `cornerList`
  function hasCornerId(id) {
    var result = false;
    self.cornerList().forEach(function(corner) {
      if (corner.id.toString() === id.toString()) {
        result = true;
      }
    });
    return result;
  }

  // fetches a corner from `cornerList` by `id`
  function getCornerById(id) {
    var foundCorner = null;
    if (hasCornerId(id)) {
      self.cornerList().forEach(function(corner) {
        if (corner.id.toString() === id.toString()) {
          foundCorner = corner;
        }
      });
    }
    return foundCorner;
  }

  google.maps.event.addDomListener(window, 'load', initialize);
};

ko.applyBindings(new ViewModel());