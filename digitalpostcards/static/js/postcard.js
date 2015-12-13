/**
 * Digital Postcards
 * =================
 * Is a jQuery module to write and send a postcard with your site's content
 * You need to put the Digital Postcard webservice in place
 * to be able to save and send the postcard.
 *
 */
(function($) {
    /**
     * [postcard description]
     * @param  {Object/String} param an object of options
     *                               or a string corresponding to an action
     * @return {boolean}
     */
    $.fn.postcard = function(param) {

        var container = $(this);
        var options = {};
        if (_.isObject(param)) options = param;
        /**
         * settings: defaul settings of the module. All can be overridden
         * @type {Object}
         */
        var settings = $.extend({
            api_post_url: "/api/1/postcard",
            tmpl_url: "js/postcard.tmpl",
            // placeholder poscard details
            title: "Lorem ipsum dolor sit amet.",
            short_desc: "Omnis quod error magni nobis",
            long_desc: "Eius vel aliquam similique ad dolorum magnam inventore \
            praesentium dolore totam, rem vero animi mollitia fuga accusantium \
            nesciunt voluptates. Aliquam, corporis, cumque! Quasi, voluptatibus\
            , labore. Nobis, ullam.",
            image: "http://placehold.it/800x600",
            image_attribution: "© Lorem ipsum, Omnis",
            // transtatables & customisables
            btn_cancel: "Cancel",
            btn_send: "Send Postcard",
            help_text: "Click here to flip the postcard",
            // input placeholders
            placeholders: {
                subject: "Subject",
                body: "Message",
                recipient_name: "Recipient name",
                recipient: "Recipient email",
                address_line_1: "Address",
                address_line_2: "Address",
                address_city: "Town",
                address_postcode: "Postcode",
                sender_name: "Your name",
                sender: "Your email",
            },
            // misc
            stamp: "img/postage-stamp.png",
            source_url: window.location.href,
            redirect_timeout: 10000
        }, options);

        /**
         * actions: an ojects of fonctions provided by the module
         * @type {Object}
         */
        var actions = {
            /**
             * render: loads a template asynchronously and populates it
             * @param  {string} tmpl_url  template url (loaded asynchronously)
             * @param  {Object} tmpl_data params to be injected in the template
             * @return {string}           rendered template
             */
            render: function(tmpl_url, tmpl_data) {
                if (!this.render.tmpl_cache) {
                    this.render.tmpl_cache = {};
                }

                if (!this.render.tmpl_cache[tmpl_url]) {

                    var tmpl_string;
                    $.ajax({
                        url: tmpl_url,
                        method: 'GET',
                        async: false,
                        success: function(data) {
                            tmpl_string = data;
                        }
                    });

                    this.render.tmpl_cache[tmpl_url] = _.template(tmpl_string);
                }

                return this.render.tmpl_cache[tmpl_url](tmpl_data);
            },
            /**
             * build: calls render with the appropriate arguments
             * @return {boolead} true
             */
            build: function() {

                // Define our render data (to be put into the "rc" variable).
                var tmpl_data = {
                    postcard: settings
                };

                var template = this.render(settings.tmpl_url, tmpl_data);

                $(container).html(
                    template
                );

                /**
                 * Register events listers based on data-action attributes
                 */
                $(container).on('click', '[data-action]', function() {
                    var action = $(this).data('action');
                    if (action in actions) actions[action]();
                });

                $(container).find('form').submit(function(e){
                    e.preventDefault();
                    actions.send();
                });

                actions.handlers();

                return true;
            },
            /**
             * send: submits the user input and the application settings
             * to the webservice and provides feedback
             * @return {boolean} true/false
             */
            send: function() {
                if (!actions.validate()) return false;

                var inputs = $(container).find('form').find(':input').not(':button').get();

                var user_data = _.object(_.pluck(inputs, 'name'),
                                          _.pluck(inputs, 'value'));

                var stamp_url;
                if (settings.stamp.indexOf('http') > -1 || settings.stamp.indexOf('//') > -1) {
                    stamp_url = settings.stamp;
                }
                if (!location.origin) {
                    location.origin = location.protocol + "//" + location.host;
                }
                stamp_url = location.origin + '/' + settings.stamp;
                
                var page_data = {
                    "title": settings.title,
                    "short_desc": settings.short_desc,
                    "long_desc": settings.long_desc,
                    "stamp": stamp_url,
                    "image": settings.image,
                    "image_attribution": settings.image_attribution,
                    "body": settings.body,
                    "source_url": settings.source_url,
                };

                var data = $.extend(user_data, page_data);

                var request = $.ajax({
                    url: settings.api_post_url,
                    method: "POST",
                    data: JSON.stringify(data),
                    dataType: "json"
                });

                request.done(function(data, textStatus, jqXHR) {
                    if (data && data.postcard) {
                        $(".postcard .back .alert").remove();
                        $(".postcard .back .content").html('').after('<div class="alert alert-success">'+
                                '<strong>Postcard sent successfully to '+
                                data.postcard.recipient + '</strong><br>' +
                                '<hr>' +
                                'Link to the postcard: <a href="' + data.postcard.url + '">' +
                                data.postcard.url + '</a>' +
                            '</div>');
                        if (settings.redirect_timeout) {
                            $(".postcard .back .alert-success").after('<div class="alert alert-info">'+
                                'You will be redirected to your postcard in '+
                                (settings.redirect_timeout / 1000) +
                                ' seconds' +
                            '</div>');
                            setTimeout(function() {
                                window.location = data.postcard.url;
                            }, settings.redirect_timeout);
                        }
                    }
                    return true;
                });

                request.fail(function(jqXHR, textStatus, errorThrown) {
                    if (jqXHR.responseJSON && jqXHR.responseJSON.errors) {
                        actions.alert(jqXHR.responseJSON.errors, jqXHR.responseJSON.error)
                    } else {
                        $(".postcard .back .content").after('<div class="alert alert-danger">'+
                                textStatus+
                                '<br>'+
                                errorThrown+
                            '</div>');
                    }
                    return false;
                });

            },

            /**
             * handlers: register handlers
             * @return {boolean}
             */
            validate: function() {
                var inputs = $(container).find('form').find(':input.required').not(':button').get();
                var errors = [];
                _.each(inputs, function(input) {
                    if (_.isEmpty($(input).val())) {
                        $('.'+$(input).attr( "name" )+'.form-group').addClass('has-error');
                        errors.push($(input).attr( "name" ));
                    }
                });

                if (!_.isEmpty(errors)) actions.alert(errors, 'Please fill in the required fields');

                return _.isEmpty(errors);
            },

            alert: function(errors, msg) {
                actions.send_btn_disabled(true);
                _.each(errors, function(input_name) {
                    $('.'+input_name+'.form-group').addClass('has-error');
                });
                $(".postcard .back .alert").remove();
                $(".postcard .back .content").after('<div class="alert alert-danger">'+msg+'</div>');

                return true;
            },

            send_btn_disabled: function(disabled) {
                $(container).find("[data-action='send']").prop('disabled', disabled);
                return true;
            },

            /**
             * handlers: register handlers
             * @return {boolean}
             */
            handlers: function() {
                $('.postcard').on('click', function() {
                    $('.postcard').addClass('flipped');
                    $('.btns').addClass('flipped');
                });
                $('.btns').on('click', function() {
                    $('.postcard').toggleClass('flipped');
                    $('.btns').toggleClass('flipped');
                });
                $(container).find('form').find(':input').on('click', function() {
                    actions.send_btn_disabled(false);
                });
                return true;
            },

            /**
             * open: flips the postcard
             * @return {boolean}
             */
            open: function() {
                if (_.isEmpty($('#mail_popup').html())) actions.build();
                $('body').toggleClass('mail_popup_open');
                $('html, body').animate({ scrollTop: container.offset().top -30 });
                return true;
            },

            /**
             * close: flips the postcard
             * @return {boolean}
             */
            close: function() {
                $('body').toggleClass('mail_popup_open');
                return true;
            }

        };

        /**
         * Init
         * Call the action request if 'param' is a string
         * Or build the postcard otherwise
         */
        if (_.isString(param)) {
            if (param in actions) actions[param]();
        }
        else {
            if (_.isEmpty($('#mail_popup').html())) actions.build();
        }
    };

}(jQuery));
