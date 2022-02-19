/* feedreader.js
 *
 * This is the spec file that Jasmine will read and contains
 * all of the tests that will be run against your application.
 */

/* We're placing all of our tests within the $() function,
 * since some of these tests may require DOM elements. We want
 * to ensure they don't run until the DOM is ready.
 */

// simple check for valid url (does not pass localhost), credit: http://stackoverflow.com/questions/18364404/javascript-url-validation-regex
function isValidUrl(url) {
    try {
        return !!url.match(/^(ht|f)tps?:\/\/[a-z0-9-\.]+\.[a-z]{2,4}\/?([^\s<>\#%"\,\{\}\\|\\\^\[\]`]+)?$/);
    } catch(error) {
        return false;
    }
}

// checks if a string is blank, null, or undefined, credit: http://stackoverflow.com/questions/154059/how-do-you-check-for-an-empty-string-in-javascript
function isBlank(string) {
    return (!string || /^\s*$/.test(string));
}

$(function() {
    /* This is our first test suite - a test suite just contains
    * a related set of tests. This suite is all about the RSS
    * feeds definitions, the allFeeds variable in our application.
    */
    describe('RSS Feeds', function() {
        /* This is our first test - it tests to make sure that the
         * allFeeds variable has been defined and that it is not
         * empty. Experiment with this before you get started on
         * the rest of this project. What happens when you change
         * allFeeds in app.js to be an empty array and refresh the
         * page?
         */
        it('are defined', function() {
            expect(allFeeds).toBeDefined();
            expect(allFeeds.length).not.toBe(0);
        });

        /* Loops through each feed in the allFeeds object and ensures
         * it has a URL defined and that the URL is not empty.
         */
        it('have valid link URLs defined', function() {
            allFeeds.forEach(function(feed) {
                expect(feed.url).toBeDefined();
                expect(isValidUrl(feed.url)).toBe(true);
            });
        });

        /* Loops through each feed in the allFeeds object and ensures
         * it has a name defined and that the name is not empty.
         */
         it('have valid names defined', function() {
            allFeeds.forEach(function(feed) {
                expect(feed.name).toBeDefined();
                expect(isBlank(feed.name)).not.toBe(true);
            });
         });
    });

    /* Test suite for the menu */
    describe('The menu', function() {
        /* Tests that the menu element is hidden by default, by
         * checking that the body has the class `menu-hidden`
         */
        var body = $('body');
        var menuIcon = $('.menu-icon-link');
        it('is hidden by default', function() {
            expect(body.hasClass('menu-hidden')).toBe(true);
        });

        /* Tests that the menu changes visibility when the menu
         * icon is clicked.
         */
        it('changes visibility when the menu icon is clicked', function() {
            menuIcon.trigger('click');
            expect(body.hasClass('menu-hidden')).toBe(false);
            menuIcon.trigger('click');
            expect(body.hasClass('menu-hidden')).toBe(true);
        });
    });

    /* Test suite for initial entries */
    describe('Initial Entries', function() {
        /* Calls the `loadFeed` function with a callback `done`
         * to ensure that it's complete.
         */
        beforeEach(function(done) {
            loadFeed(0, done);
        });

        /* Once `loadFeed` function is called and completes its work,
         * there is at least one .entry element within the .feed
         * container.
         */
        it('has at least one entry', function(done) {
            var entries = $('.feed').find('.entry');
            expect(entries.length >= 1).toBe(true);
            done();
        });
    });

    /* Test suite for New Feed Selection */
    describe('New Feed Selection', function() {
        var before, after;

        /* Calls the `loadFeed` function with callbacks to ensure that
         * they're complete.
         */
        beforeEach(function(done) {
            /* Make sure that there are at least two feeds to test */
            expect(allFeeds.length >= 2).toBe(true);

            /* Load the first feed at index 0 */
            loadFeed(0, function() {
                /* Set the before to content of feed */
                before = $('.header-title').text() + $('.feed').find('.entry').text().replace(/ +/g, " ");
                /* Load second feed at index 1 */
                loadFeed(1, function() {
                    /* Set the after to content of new feed */
                    after = $('.header-title').text() + $('.feed').find('.entry').text().replace(/ +/g, " ");
                    done();
                });
            });
        });

        /* Tests that when a new feed is loaded by the loadFeed function
         * that the content actually changes.
         */
        it('changes content', function(done) {
            expect(before != after).toBe(true);
            done();
        });
    });

}());
