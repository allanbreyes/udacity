// signed url from meetup api, taken from https://secure.meetup.com/meetup_api/console/?path=/2/open_events
var meetupApiUrl = 'http://api.meetup.com/2/open_events?status=upcoming&radius=5&category=34&and_text=False&limited_events=False&text=coding+programming+ruby+python+javascript+html&desc=False&offset=0&photo-host=public&format=json&lat=41.878114&page=100&lon=-87.629798&sig_id=178346822&sig=1a186723262b63d4b2deee474b8d95bc0ec2ec9f';

/* monkey patches for additional string functionality */
// capitalizes first letter of each word if sentence is longer than 10 characters
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

// checks if a substring `other` is found inside the string
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
  // pseudo-model validation: if no lat/lon data, set location to null
  // otherwise, instantiate a google maps coordinate
    if (self.lat === 0 || self.lon === 0) {
      return null;
    } else {
      return new google.maps.LatLng(self.lat, self.lon);
    }
  });

  // load metadata
  self.id = venueObject.id;
  self.name = ko.observable(venueObject.name.titleize());
  self.address = ko.observable(venueObject.address_1);

  // initialize empty meetup
  self.meetups = ko.observableArray([]);

  // initialize empty marker
  self.marker = new google.maps.Marker();
};

// meetup model constructor, where `meetup` == item from Meetup API `open_venue` JSON response
var Meetup = function(meetup) {
  var self = this;

  // attach venue object
  self.venueObject = meetup.venue;

  // returns if the meetup has a venue that's listed
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

  // converts date in milliseconds to a human-friendly string, e.g. 1/2/2015
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

  // future google map object, assigned in `drawMap`
  var map;

  // target map canvas from DOM
  var mapCanvas = $('#map-canvas')[0];

  // default center location, currently set to chicago
  var center = new google.maps.LatLng(41.8886, -87.6310);

  // google map marker tooltip
  var infoWindow = new google.maps.InfoWindow();

  // list of meetups, not currently used in view
  self.meetupList = ko.observableArray([]);

  // list of corners, bound to `#list`
  self.cornerList = ko.observableArray([]);

  // number of corners, bound to `#search-summary p`
  self.numCorners = ko.observable(0);

  /* SEARCH */

  // search query, bound to `#search-input` search box
  // TODO: should be a computable
  self.query = ko.observable('');

  // bound to `#search-btn`
  self.search = function() {
    // empty function for future functionality
    // keep present to avoid page reload
  };

  // returns a filtered list of corners if name contains `self.query` data
  self.filteredCornerList = ko.computed(function() {
    // loop through corners and clear map markers
    self.cornerList().forEach(function(corner) {
      corner.marker.setMap(null);
    });

    // filter results where name contains `self.query`
    var results = ko.utils.arrayFilter(self.cornerList(), function(corner) {
      return corner.name().toLowerCase().contains(self.query().toLowerCase());
    });

    // go through results and set marker to visible
    results.forEach(function(corner) {
      corner.marker.setMap(map);
    });

    // update the number of corners (couldn't get `ko.computed` to work)
    self.numCorners(results.length);
    return results;
  });

  /* SELECTION */

  // triggered when a corner in `#list` is clicked or a marker is clicked
  self.selectCorner = function(corner) {

    /* STUDENT NOTE: I was unable to get proper separation of concerns here, as I could not find
     *  an intelligent way to use partials or layouts for Google Maps info windows.  I think that
     *  this is also a security concern for injection attacks, and I would like feedback on how to
     *  handle this.  Thank you!
     */

    // generate html for a corner's upcoming open meetups
    var formattedMeetupList = (function(corner) {
      result = '<ul class="info-window-list">';
      corner.meetups().forEach(function(meetup) {
        result += '<li>' +
                  '<a href="' +
                  meetup.url() +
                  '">' +
                    meetup.name() +
                  '</a>' +
                  ' on ' +
                  meetup.date() +
                  '</li>';
      });
      result += '</ul>';
      return result;
    })(corner);
    // generate additional html and set to info window content
    infoWindow.setContent('<div class="info-window-content">' +
                          '<span class="info-window-header">' +
                            corner.name() +
                          '</span>' +
                          '<p>' +
                            corner.address() +
                          '</p>' +
                            formattedMeetupList +
                          '</div>'
                         );

    // open up the appropriate info window at the selected corner's marker
    infoWindow.open(map, corner.marker);

    // scroll the map to the marker's position
    map.panTo(corner.marker.position);
  };

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
          { "color": '#D0B2B2' },
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
      zoomControl: false
    };

    // assign a google maps element
    map = new google.maps.Map(element, mapOptions);

    // apply custom map styling
    var styledMapOptions = {};
    var usRoadMapType = new google.maps.StyledMapType(roadAtlasStyles, styledMapOptions);
    map.mapTypes.set('usroadatlas', usRoadMapType);
    map.setMapTypeId('usroadatlas');
  }

  // create a map marker
  function addMarker(corner) {
    var marker;

    // validate that the corner has a location (see `Corner` model for pseudo-validation)
    if (corner.location()) {
      marker = new google.maps.Marker({
        position: corner.location(),
        map: map,
      });
      // add a listener for when it's clicked
      google.maps.event.addListener(marker, 'click', function () {
        self.selectCorner(corner);
      });
    }

    // return the marker object
    return marker;
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

      // loop through results and populate `meetupList`
      data.forEach(function(meetup) {
        self.meetupList.push(new Meetup(meetup));
      });

      // run the `extractCorners` function to pull location data
      extractCorners();

    // if failed
    }).fail(function(response, status, error) {
      $('#search-summary').text('Meetup data could not load...');
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
          // instantiate a new corner object
          corner = new Corner(meetup.venueObject);

          // check if has valid location
          if (corner.location()) {
            // push it to the corner list
            self.cornerList.push(corner);

            // and push the meetup object onto that new corner object
            corner.meetups.push(meetup);

            // add a marker
            corner.marker = addMarker(corner);
          }
        }
      }
    });
  }

  // checks if a specific corner by `id` already exists in `cornerList`
  // TODO: check if they have the same lat/lon--but how to handle multiple floors?
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
  // TODO: check if they have the same lat/lon--but how to handle multiple floors?
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

  /* INITIALIZATION */

  function initialize() {
    drawMap(center, mapCanvas);
    fetchMeetups(meetupApiUrl);
  }

  /* LISTENERS */

  google.maps.event.addDomListener(window, 'load', initialize);
};

ko.applyBindings(new ViewModel());