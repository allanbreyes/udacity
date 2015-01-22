# Website Performance Optimization Project

### About
The objective for this project was to optimize [Cameron Pittman's portfolio](https://github.com/gosukiwi/web-performance-portfolio) page for speed. The strategy was to optimize the critical rendering path, making the page render as quickly as possible, using techniques you've picked up in the [Website Performance Optimization](https://www.udacity.com/course/ud884).

### How to run
To get started, download the entire directory, `p4`, and open it in a browser locally.

### Page load speed optimization
- Image compression: images were rescaled and resized to the final layout dimensions.
- Inline critical CSS: critical above-the-fold content styles are inlined and applied to the document immediately vs. blocking loading. This was done using the methods prescribed by Google Developers (see references).
- Defer alternative media CSS: print stylesheets, although small, were deliberately chosen not to be served inline in HTML documents due to at least three different pages using it.  A media attribute was added to ensure that it would only be downloaded when printing.
- Minifying CSS/JS: all CSS and JS files were minified--but not obfuscated--to ensure faster downloading.  The formatted and indented files are still present in their respective directories, without the `.min` in their filenames.

### Frame rate optimization
- Loop optimization: unnecessary JS operations were pulled out of `for` loops where possible, in `views/js/main.js`.
- Debouncing: scroll events were 'debounced' to decouple the animations and only reflow/repaint when needed.

**Framerate timelines**: saved JSON timelines and screenshots for `pizza.html` are located in the `dev/` directory, and shown below:

*Original*

![Original](https://raw.githubusercontent.com/allanbreyes/udacity-front-end/master/p4/dev/0-pizza-original.png)


*After loop optimization*

![After loop optimization](https://raw.githubusercontent.com/allanbreyes/udacity-front-end/master/p4/dev/1-pizza-loop-optimization.png)


*After debouncing*

![After debouncing](https://raw.githubusercontent.com/allanbreyes/udacity-front-end/master/p4/dev/2-pizza-animation-optimization.png)


*After minify*

![After minify](https://raw.githubusercontent.com/allanbreyes/udacity-front-end/master/p4/dev/3-pizza-minify.png)

### Further areas of improvement
- Browser caching, configured server-side, could have reduced page loading time.
- Using a CDN for Bootstrap files could have reduced page loading time as well, but was minified for the purposes of this exercise.

### Resources
- [PageSpeed Insights](https://developers.google.com/speed/pagespeed/insights/)
- [Optimize CSS Delivery](https://developers.google.com/speed/docs/insights/OptimizeCSSDelivery)
- [Leaner, Meaner, Faster Animations with requestAnimationFrame](http://www.html5rocks.com/en/tutorials/speed/animations/)