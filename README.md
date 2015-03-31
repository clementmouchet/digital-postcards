Digital Postcards: Share content with others in a personal manner
=================================================================

A simple Flask webservice that manages postcard details and a JavaScript module.

## Webservice Requirements

|Name			|Version		|Comment										|
|:--------------|:-------------:|:----------------------------------------------|
|Python			|>= 2.7 		| The webservie is based on Flask				|
|Mongo 			|>= 2.6 		| Mongo is used to store collections			|
|SMTP server	|any	 		| Required to email details about the postcard	|
|OS				|any	 		|												|

Python requirements are maintained in a pip requirements file: `requirements.txt`

## JavaScript Requirements

|Name			|Version		|Comment										|
|:--------------|:-------------:|:----------------------------------------------|
|JQuery			|>= 1.? 		| postcard() is a JQuery module					|
|UnderscoreJS 	|>= 1.? 		| UnderscoreJS is used in the module			|
|Bootstrap		|>= 3.x			| Required to email details about the postcard	|


## Installation

_Installation of Python & Mongo is beyond the scope of this Read Me._

1. Create virtual environment to install pip requirements & activate it
2. Install pip requirements
3. Edit the configuration as required
4. Run the app


## Using the JavaScript module


_The module uses [UnderscoreJS](http://underscorejs.org/) to populate the postcard template,
it must be loaded before the module_

_The module css uses [Bootstrap 3](http://getbootstrap.com/) it must be loaded before the module_

It is configurable with the following options:
```javascript
	{
	    api_post_url:           "{ domain of the webservice /api/1/postcard }",
	    tmpl_url:               "{ domain of the webservice /js/postcard.tmpl }",

	    // placeholder postcard details
	    title:                  "{ title of the postcard }",
	    short_desc:             "{ a short description shown below the title }",
	    long_desc:              "{ a longer description shown in the heading of the postcard }",
	    image:                  "{ the url of the image }",
	    image_attribution:      "{ the attribution of the image }",

	    // transtatables & customisables
	    btn_cancel:             "{ label of the cancel button }",
	    btn_send:               "{ label of the send button }",
	    help_text:              "{ help text of the menu bar }",

	    // input placeholders
	    placeholders: {
	        subject:            "{ placeholder of the subject input }",
	        body:               "{ placeholder of the body text area }",
	        recipient_name:     "{ placeholder of the recipient_name input }",
	        recipient:          "{ placeholder of the recipient input }",
	        address_line_1:     "{ placeholder of the address_line_1 input }",
	        address_line_2:     "{ placeholder of the address_line_2 input }",
	        address_city:       "{ placeholder of the address_city input }",
	        address_postcode:   "{ placeholder of the address_postcode input }",
	        sender_name:        "{ placeholder of the sender_name input }",
	        sender:             "{ placeholder of the sender input }",
	    },

	    // misc
	    stamp:                  "{ the url of the stamp logo }",
	    source_url:             "{ the source url }",
	    redirect_timeout:       "{ a timeout if you want to redirect the user }"
	}
```

Every option has default values which can be overridden as required.

If you don't use Underscore, you should load it before the module.
You can load all the js and css dependencies in Javascript

```html
	<script type="text/javascript">
	 /**
	  * Digital Postcards module
	  */

	  // load underscorejs
	  $.getScript("https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.2/underscore-min.js")
	  .done(function( script, textStatus ) {
	    // load the postcard module
	    $.getScript("http://localhost:5000/js/postcard.js")
	    .done(function( script, textStatus ) {
	      // initialise the postcard module
	      ...
	    })
	  });
	  // load the plugin css
	  url = 'http://localhost:5000/css/postcard.css';
	  if (document.createStyleSheet) {
	      document.createStyleSheet(url); // IE < 11 only
	  }
	  else {
	      $('<link rel="stylesheet" type="text/css" href="' + url + '" />').appendTo('head');
	  }
	</script>
```

Or you can simply add them normally

```html
	<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.2/underscore-min.js"></script>
	<script type="text/javascript" src="http://{domain of the webservice}/js/postcard.js"></script>
	<link rel="stylesheet" href="http://{domain of the webservice}/css/postcard.css') }}">
```

Initialising the module is easy, all you ned to do is map the options to fields on you page (or provide values)

```html
	<script type="text/javascript">
	 $('#mail_popup').postcard({
	    api_post_url: "http://localhost:5000/api/1/postcard",
	    tmpl_url: "http://localhost:5000/js/postcard.tmpl",
	    // placeholder poscard details
	    title: $('.memory .title').html(),
	    short_desc: $('.memory .subtitle').html(),
	    long_desc: $('#memory-description').html(),
	    image: $('#image img').attr("src"),
	    image_attribution: $('#memory-attribution').html(),
	    stamp: "http://localhost:5000/img/postage-stamp.png"
	});
	</script>
```

And add the following element to your DOM.

```html
	<div id="mail_popup"></div>
```

## Markup & CSS

Load the css file to style the popup

```html
	<link rel="stylesheet" href="http://{domain of the webservice}/css/postcard.css') }}">
```

`.postcard-blur-wrapper` can be used to apply a blur filter to the container below the popup.
