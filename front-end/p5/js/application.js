// signed url from meetup api, taken from https://secure.meetup.com/meetup_api/console/?path=/2/open_events
var meetupApiUrl = 'http://api.meetup.com/2/open_events?status=upcoming&radius=5&category=34&and_text=False&limited_events=False&text=coding+programming+ruby+python+javascript+html&desc=False&offset=0&photo-host=public&format=json&lat=41.878114&page=100&lon=-87.629798&sig_id=178346822&sig=1a186723262b63d4b2deee474b8d95bc0ec2ec9f';

/* Capitalizes first letter of each word if sentence is longer than 10 characters */
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

/* Checks if a substring `other` is found inside the string */
String.prototype.contains = function(other) {
  return this.indexOf(other) !== -1;
};

/* Represents a coding "corner", or a geographical place or venue.
 * @constructor
 * @param {object} venueObject - JSON-like venue from the Meetup open_venue API
 */
var Corner = function(venueObject, map) {
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

  // initialize marker
  self.marker = (function(corner) {
    var marker;

    // validate that the corner has a location (see `Corner` model for pseudo-validation)
    if (corner.location()) {
      marker = new google.maps.Marker({
        position: corner.location(),
        map: map,
      });
    }

    // return the marker object
    return marker;
  })(self);

  // returns the formatted HTML for a corner's upcoming open meetups
  self.formattedMeetupList = function() {
    meetupSubstring = '<ul class="info-window-list">';
    self.meetups().forEach(function(meetup) {
      meetupSubstring += '<li>' + '<a href="' + meetup.url() + '">' +
                           meetup.name() +
                         '</a>' + ' on ' + meetup.date() + '</li>';
    });
    meetupSubstring += '</ul>';
    return '<div class="info-window-content">' +
              '<span class="info-window-header">' + self.name() + '</span>' +
              '<p>' + self.address() + '</p>' +
              meetupSubstring +
              '</div>';
  };
};

/* Represents a Meetup event.
 * @constructor
 * @param {object} meetup - JSON-like meetup from the Meetup open_venue API
 */
var Meetup = function(meetup) {
  var self = this;

  // attach venue object
  self.venueObject = meetup.venue;

  // returns if the meetup has a venue that is listed
  self.hasVenue = ko.computed(function() {
    if (self.venueObject) {
      return true;
    } else {
      return false;
    }
  });

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

/* Represents a Google Map object */
var GoogleMap = function(center, element) {
  var self = this;

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

  return map;
};

/* Main application view model */
var AppViewModel = function() {
  var self = this;

  function initialize() {
    map = GoogleMap(center, mapCanvas);
    fetchMeetups(meetupApiUrl);
  }

  // check that Google Maps loaded
  if (typeof google !== 'object' || typeof google.maps !== 'object') {
    $('#search-summary').text("Could not load Google Maps API");
  }

  // initialize defaults
  var map,
      mapCanvas = $('#map-canvas')[0],
      center = new google.maps.LatLng(41.8886, -87.6310); // Chicago

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
  self.query = ko.observable('');

  // bound to `#search-btn`
  /* Search function. */
  self.search = function() {
    // empty function for future functionality, keep present to avoid page reload
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

  // triggered when a corner in `#list` is clicked or a marker is clicked
  /* Fetches from marker/infowindow data and animate markers
   * @param {object} corner - Corner instance
   */
  self.selectCorner = function(corner) {
    // fetch and set html to info window content
    infoWindow.setContent(corner.formattedMeetupList());

    // open up the appropriate info window at the selected corner's marker
    infoWindow.open(map, corner.marker);

    // scroll the map to the marker's position
    map.panTo(corner.marker.position);

    // animate markers
    corner.marker.setAnimation(google.maps.Animation.BOUNCE);
    self.cornerList().forEach(function(old_corner) {
      if (corner != old_corner) {
        old_corner.marker.setAnimation(null);
      }
    });
  };

  /* Fetches meetups via JSON-P from Meetup API
   * @params {string} url - Meetup API URL */
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

  /* Parses through the meetupList and extracts Corner objects */
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
          corner = new Corner(meetup.venueObject, map);

          // check if has valid location
          if (corner.location()) {
            // push it to the corner list
            self.cornerList.push(corner);

            // and push the meetup object onto that new corner object
            corner.meetups.push(meetup);

            // add a marker callback
            google.maps.event.addListener(corner.marker, 'click', function () {
              self.selectCorner(corner);
            });
          }
        }
      }
    });
  }

  /* Checks if a specific corner by `id` already exists in `cornerList`
   * @param {int} id - id number
   */
  function hasCornerId(id) {
    var result = false;
    self.cornerList().forEach(function(corner) {
      if (corner.id.toString() === id.toString()) {
        result = true;
      }
    });
    return result;
  }

  /* Fetches a corner from `cornerList` by `id`
   * @param {int} id - id number
   */
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

  // initialization listener
  google.maps.event.addDomListener(window, 'load', initialize);
};

ko.applyBindings(new AppViewModel());