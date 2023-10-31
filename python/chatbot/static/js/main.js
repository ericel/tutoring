/**
 * ChatBot Javascript File
 *
 * @version 1.0
 */
'use strict';

var $ = jQuery.noConflict();


/* jQuery easing */
$.extend($.easing, {
    def: 'easeOutQuad',
    swing: function (x, t, b, c, d) {
        return $.easing[$.easing.def](x, t, b, c, d);
    },
    easeOutQuad: function (x, t, b, c, d) {
        return -c * (t /= d) * (t - 2) + b;
    },
    easeOutQuint: function (x, t, b, c, d) {
        return c * ((t = t / d - 1) * t * t * t * t + 1) + b;
    }
});


/**
     * ChatBot Object
     */
window.ChatBot = {};
/**
 * ChatBot Base
 */
(function ($) {
    
    /**
     * jQuery Window Handle
     * 
     * @var jQuery jQuery window handle
     */
    ChatBot.$window = $(window);

    /**
     * jQuery Body Handle
     * 
     * @var jQuery jQuery body handle
     */
    ChatBot.$body = $(document.body);

    /**
     * Status
     * 
     * @var string Status
     */
    ChatBot.status = '';

    /**
     * Check if the browser is internet explorer.
     * 
     * @var boolean isIE
     */
    ChatBot.isIE = navigator.userAgent.indexOf('Trident') >= 0;

    /**
     * Check if the browser is internet explorer.
     *
     * @var boolean isIE
     */
    ChatBot.isEdge = navigator.userAgent.indexOf('Edge') >= 0;
    ChatBot.isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

    /**
     * Make a macro task
     * 
     * @param {function} fn
     * @param {number} delay
     * @return {void}
     */
    ChatBot.call = function (fn, delay) {
        setTimeout(fn, delay);
    }

    /**
     * Parse options string to object
     *
     * @param {string} options
     * @return {object} options
     */
    ChatBot.parseOptions = function (options) {
        return 'string' == typeof options ?
            JSON.parse(options.replace(/'/g, '"').replace(';', '')) :
            {};
    }

    /**
     * Parse html template with variables.
     *
     * @param {string} template
     * @param {object} vars
     * @return {string} parsed template
     */
    ChatBot.parseTemplate = function (template, vars) {
        return template.replace(/\{\{(\w+)\}\}/g, function () {
            return vars[arguments[1]];
        });
    }

    /**
     * Get dom element by id
     *
     * @param {string} id
     * @return {HTMLElement} element
     */
    ChatBot.byId = function (id) {
        return document.getElementById(id);
    }

    /**
     * Get dom elements by tagName
     *
     * @param {string} tagName
     * @param {HTMLElement} element this can be omitted.
     * @return {HTMLCollection}
     */
    ChatBot.byTag = function (tagName, element) {
        return element ?
            element.getElementsByTagName(tagName) :
            document.getElementsByTagName(tagName);
    }

    /**
     * Get dom elements by className
     *
     * @param {string} className
     * @param {HTMLElement} element this can be omitted.
     * @return {HTMLCollection}
     */
    ChatBot.byClass = function (className, element) {
        return element ?
            element.getElementsByClassName(className) :
            document.getElementsByClassName(className);
    }

    /**
     * Set cookie
     *
     * @param {string} name Cookie name
     * @param {string} value Cookie value
     * @param {number} exdays Expire period
     */
    ChatBot.setCookie = function (name, value, exdays) {
        var date = new Date();
        date.setTime(date.getTime() + (exdays * 24 * 60 * 60 * 1000));
        document.cookie = name + "=" + value + ";expires=" + date.toUTCString() + ";path=/";
    }

    /**
     * Get cookie
     *
     * @param {string} name Cookie name
     * @return {string} Cookie value
     */
    ChatBot.getCookie = function (name) {
        var n = name + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; ++i) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(n) == 0) {
                return c.substring(n.length, c.length);
            }
        }
        return "";
    }

    // if($('.scrollable')[0]){
    //     // Scrollable MCustomScrollbar
    //     $('.scrollable').each(async function (i, obj) {
    //         $(this).mCustomScrollbar({
    //             // For scrollbar on scrollable elements
    //             theme: "light",
    //             axis: "y", // vertical and horizontal scrollbar
    //             //scrollbarPosition: "inside",
    //             alwaysShowScrollbar: 0,
    //             scrollInertia: 200,
    //             advanced: {
    //                 autoScrollOnFocus: false
    //             },
    //             callbacks: {
    //                 onTotalScroll: function () {
    
    //                 }
    //             }
    //         });
    //     });
    // };
})(jQuery);

(function ($) {
    ChatBot.chatbotApp = function () {
        const chat_btn = $(".chatbot-icon");
        const chat_box = $(".messenger");
        const chat_home = $(".home-view");
        const home_icon = $(".home-icon");
        const back_to_assistant_button = $(".back-to-assistant");
        const minimize_chatbot = $(".toggle-close-chatbot");

        // Handle and populate welcome to bot
        function welcome_text() {
            $.ajax({
                url: "/openaibot", // the endpoint
                type: "POST", // http method
                headers: {
                    "X-CSRFToken": ChatBot.getCookie('csrftoken'),
                    "POST-TYPE": "entry_home"
                },
                data: { }, // data sent with the post request
                // handle a successful response
                success: function (json) {
                    chat_home.find('.welcome_text').text(json.message)
                    chat_home.addClass("expanded active");
                    // Append each frequently asked question to homeview
                    $('.bot_faqs').html('');
                    $.each(json.bot_faqs, function(index, value) {
                        // Create a new button element
                        var $button = $(`<button class="bot-faq" data-prompt="${value}">`).text(value);

                        // Hide the button initially
                        $button.css('opacity', 0);

                        // Append the button to the container
                        $('.bot_faqs').append($button);

                        // Delay and animate each item
                        $button.delay(index * 200).animate({
                            opacity: 1,
                            marginTop: '10px'
                        }, 700, 'easeOutBounce');
                      });
                    
                },
                // handle a non-successful response
                error: function (xhr, errmsg, err) {
                    chat_home.find('.welcome_text').text("something went wrong!!!")
                    console.log("something went wrong!!!")
                    
                }
            });
        }

        function promptCompletion(prompt){
            $.ajax({
                url: "/openaibot", // the endpoint
                type: "POST", // http method
                headers: {
                    "X-CSRFToken": ChatBot.getCookie('csrftoken'),
                    "POST-TYPE": "prompt_completion"
                },
                data: {'prompt': prompt}, // data sent with the post request
                // handle a successful response
                success: function (json) {
                    // Append return completion to assistant
                    // Create a new answer element
                    var $bubble = $(`<div class="msg msg-left">
                    <div class="bubble">
                      ${json.completion}
                    </div>
                  </div>`);
                    // Hide the button initially
                    $bubble.css('opacity', 0);
                    // Append the button to the container
                    chat_box.find('.chatroom').append($bubble);
                    // Delay and animate each item
                    $bubble.delay(200).animate({
                        opacity: 1,
                        marginTop: '10px'
                    }, 700, 'easeOutBounce');
                    $(".scrollable").mCustomScrollbar("update");
                     $(".scrollable").mCustomScrollbar("scrollTo", "bottom");
                    },
                // handle a non-successful response
                error: function (xhr, errmsg, err) {
                    chat_box.find('.chatroom').append(`<div class="msg msg-left">
                    <div class="bubble">
                      Something went wrong! Try again.
                    </div>
                  </div>`)
                    console.log("something went wrong!!!")
                    
                }
            });
        }
        if(chat_home[0]){
            console.log("chat home available");
            console.log('got here')
           /*  $.ajax({
                url: "/api/account/auth2/", // the endpoint
                type: "POST", // http method
                headers: {
                    "X-CSRFToken": ChatBot.getCookie('csrftoken')
                },
                data: { token: token, GoogleAuth: true }, // data sent with the post request
                // handle a successful response
                success: function (json) {
                    // Just Reload Page
                    location.reload();
                },
                // handle a non-successful response
                error: function (xhr, errmsg, err) {
                    console.log("something went wrong!!!")
                    window.location.href = '/account/logout';
                }
            }); */
        }
        // On each bot-faq click, open assitant with prompt
        ChatBot.$body.on('click', '.bot-faq', function (e) {
            e.stopPropagation();
            e.preventDefault();
            var prompt = $(this).attr('data-prompt');
            // Open assistant
            chat_box.addClass("expanded active");
            attachScrollbar()
            chat_home.removeClass("expanded active");
            chat_box.find('.chatroom').append(`
            <div class="msg msg-right">
                <div class="bubble">
                    ${prompt}
                </div>
                </div>
            `);
            // Then send prompt to back end
            promptCompletion(prompt)
        });
       // Attach a click event handler to the body element that listens for clicks on elements with the 'chatbot-icon' class within it
       ChatBot.$body.on('click', '.chatbot-icon', function (e) {
            e.stopPropagation(); // Prevent the event from bubbling up the DOM tree
            e.preventDefault(); // Prevent the default behavior of the event (e.g., following a link)

            // Store a reference to the clicked element
            const $this = $(this);

            // Execute the following code after a delay of 100 milliseconds
            setTimeout(() => {
                $this.addClass('display-none'); // Add the 'display-none' class to the clicked element

                if (chat_box.hasClass('active')) {
                    chat_box.addClass("expanded active"); // Add the 'expanded' and 'active' classes to the chat_box element
                    attachScrollbar()
                
                } else if (chat_home.hasClass('active')) {
                    // Update or write the welcome text
                    welcome_text();

                    if (back_to_assistant_button.hasClass('display_none')) {
                        back_to_assistant_button.removeClass('display-none'); // Remove the 'display-none' class from the back_to_assistant_button element
                    }
                } else {
                    // Update or write the welcome text
                    welcome_text();

                    back_to_assistant_button.addClass('display-none'); // Add the 'display-none' class to the back_to_assistant_button element
                }

            }, 100);
        });

        // Attach a click event handler to the body element that listens for clicks on elements with the 'home-icon' class within it
        ChatBot.$body.on('click', '.home-icon', function (e) {
            e.stopPropagation(); // Prevent the event from bubbling up the DOM tree
            e.preventDefault(); // Prevent the default behavior of the event (e.g., following a link)

            // Check if the height of the chat_home element is 0
            if (chat_home.height() === 0) {
                chat_home.css("height", ""); // Set the height of the chat_home element to its default value
            }

            // Execute the following code after a delay of 100 milliseconds
            setTimeout(() => {
                // Call the welcome_text() function to update or write the welcome text
                welcome_text();

                // Remove the 'expanded' and 'active' classes from the chat_box element
                chat_box.removeClass("expanded active");

                // Remove the 'display-none' class from the back_to_assistant_button element
                back_to_assistant_button.removeClass('display-none');
            }, 100);
        });
        ChatBot.$body.on('click', '.back-to-assistant', function (e) {
            e.stopPropagation();
            e.preventDefault();
            setTimeout(() => {
                chat_home.removeClass("expanded active");
                chat_box.addClass("expanded active");
                attachScrollbar()
            }, 100);
        });
        


        ChatBot.$body.on('click', '.toggle-close-chatbot', function (e) {
            e.preventDefault();
            e.stopPropagation();
            
            chat_box.animate({
                height: 0
            }, 100, function() {
                // Animation complete, remove the expanded class and reset height
                chat_box.removeClass("expanded").css("height", "");
                chat_btn.removeClass('display-none');
            });

            chat_home.animate({
                height: 0
            }, 100, function() {
                // Animation complete, remove the expanded class and reset height
                chat_home.removeClass("expanded").css("height", "");
                chat_btn.removeClass('display-none');
            });
            
        });
        ChatBot.$body.on('input', '.typing', function (e) {
        ///$('.typing').on('input', function() {
            var inputValue = $(this).val().trim();
            var sendButton = $('#chat-bot .type-area .send');
            
            if (inputValue !== '') {
              sendButton.addClass('active');
            } else {
              sendButton.removeClass('active');
            }
          });


        // Send chat to backend
        ChatBot.$body.on('click', '.send', function (e) {

              e.preventDefault();
              e.stopPropagation();
          
              if (chat_home.hasClass("expanded") || chat_home.hasClass("active")) {
                chat_home.removeClass("expanded active");
              }
          
              if (!chat_box.hasClass("expanded active")) {
                chat_box.addClass("expanded active");
                back_to_assistant_button.removeClass('display-none');
              }
          
              // Do a prompt completion request and also add user bubble
              var prompt = $(this).parent().find('.typing').val().trim();
              if (prompt) {
                chat_box.find('.chatroom').append(`
                  <div class="msg msg-right">
                    <div class="bubble">
                      ${prompt}
                    </div>
                  </div>
                `);
                promptCompletion(prompt);
                $('.typing').val('');
              }
            
          }).on('keyup', '.typing', function (e) {
            if (e.type === 'keyup' && e.keyCode === 13) {
              e.preventDefault();
              e.stopPropagation();
          
              if (chat_home.hasClass("expanded") || chat_home.hasClass("active")) {
                chat_home.removeClass("expanded active");
              }
          
              if (!chat_box.hasClass("expanded active")) {
                chat_box.addClass("expanded active");
                back_to_assistant_button.removeClass('display-none');
              }
          
              // Do a prompt completion request and also add user bubble
              var prompt = $(this).parent().find('.typing').val().trim();
              if (prompt) {
                chat_box.find('.chatroom').append(`
                  <div class="msg msg-right">
                    <div class="bubble">
                      ${prompt}
                    </div>
                  </div>
                `);
                promptCompletion(prompt);
                $('.typing').val('');
              }
            }
          });

          // Attach Scrollbar
          function attachScrollbar(){
            //$('.scrollable').each(async function (i, obj) {
                $('.scrollable').mCustomScrollbar({
                    // For scrollbar on scrollable elements
                    theme: "minimal",
                    axis: "y", // vertical and horizontal scrollbar
                    //scrollbarPosition: "inside",
                    alwaysShowScrollbar: 0,
                    scrollInertia: 200,
                    advanced: {
                        autoScrollOnFocus: false
                    },
                    callbacks: {
                        onTotalScroll: function () {
        
                        }
                    }
                });
           // });
          }
    }
})(jQuery);
(function ($) {
    ChatBot.authenticationApp = function () {
        /// public variables
        const googleprovider = new firebase.auth.GoogleAuthProvider();
        const facebookprovider = new firebase.auth.FacebookAuthProvider();
        const twitterprovider = new firebase.auth.TwitterAuthProvider();
        const config = {
            apiKey: "AIzaSyA3CY-Bp3ZlMQ6HiD4nKhG2uXqt-7al6Og",
            authDomain: "otcollect.firebaseapp.com",
            databaseURL: "https://otcollect.firebaseio.com",
            projectId: "otcollect",
            storageBucket: "otcollect.appspot.com",
            messagingSenderId: "19029682316",
            appId: "1:19029682316:web:272a69564ca079909a33a9"
        };
        firebase.initializeApp(config);
        ChatBot.auth = firebase.auth();

        // Logout User Front and backend
        function authLogout() {
            ChatBot.auth.signOut().then(function () {
                // Sign-out successful.
                console.log("logged Out successfully!!");
                window.location.href = '/account/logout';
            }, function (error) {
                // An error happened.
            });
        }

        //this.authLogout();
        ChatBot.auth.getRedirectResult()
        .then(async (result) => {
            if (result.user) {
                result.user.getIdToken().then((idToken) => {
                    this.handleMethod(idToken, false)
                });
            }
            //console.log(user)
        }).catch((error) => {
            // Handle Errors here.
            const errorCode = error.code;
            console.log(error);
        });
        // Check if there is a logged in user
        // If not, and auth is present
        // logged them in backend
        ChatBot.auth.onAuthStateChanged((user) => {
            if (user !== null) {
                if ($("body.anonymous")[0]) {
                    // Logged in on Front End but not Backend
                    user.getIdToken().then((idToken) => {
                        handleMethod(idToken, false, )
                    });
                }
            } else if (user === null && $("body.anonymous")[0]) {
                google.accounts.id.initialize({
                    client_id: "19029682316-2d6dfn0gc8ms259iqkuf1jv6vd0kfncn.apps.googleusercontent.com",
                    callback: handleCredentialResponse,
                    auto_select: "false",
                    ux_mode: "redirect",//popup// redirect//popup
                    prompt_parent_id: "g_id_onload",
                    login_uri: `${window.location.origin}/api/account/auth2/`,
                    style: "position: fixed; top: 40px; right: 30px;  z-index: 1001;"
                });
                google.accounts.id.renderButton(
                    document.getElementById("g_id_signin"),
                    { theme: "outline", size: "large", width: 250, shape: "pill" }  // customization attributes
                );
                google.accounts.id.prompt(); // also display the One Tap dialog
                
            }
        });

        // Handle google auth prompt
        function handleCredentialResponse(response) {
            var token = response.credential;
            $.ajax({
                url: "/api/account/auth2/", // the endpoint
                type: "POST", // http method
                headers: {
                    "X-CSRFToken": ChatBot.getCookie('csrftoken')
                },
                data: { token: token, GoogleAuth: true }, // data sent with the post request
                // handle a successful response
                success: function (json) {
                    // Just Reload Page
                    location.reload();
                },
                // handle a non-successful response
                error: function (xhr, errmsg, err) {
                    console.log("something went wrong!!!")
                    window.location.href = '/account/logout';
                }
            });
        }

        // Handle firebackend login
        function handleMethod(token, googleAuth) {
            $.ajax({
                url: "/api/account/auth2/", // the endpoint
                type: "POST", // http method
                headers: {
                    "X-CSRFToken": ChatBot.getCookie('csrftoken')
                },
                data: { token: token, GoogleAuth: googleAuth }, // data sent with the post request
                // handle a successful response
                success: function (json) {
                    // Just Reload Page
                    location.reload();
                    //window.location.href = JSON.parse(json)['next'];
                },
                error: function (xhr, errmsg, err) { // handle a non-successful response

                    console.log(xhr.responseText)
                }
            });

        }

        // google signup with popup
        ChatBot.$body.on('click', '.googleLogin', function (e) {
            e.preventDefault();
            ChatBot.auth.signInWithPopup(googleprovider).catch((error) => {
                console.log(error);
                // Handle Errors here.
                const errorCode = error.code;
                if (errorCode === "auth/popup-closed-by-user") {
                    // try redirect login
                    console.log("try google redirect login!!!")
                    //ChatBot.auth.signInWithRedirect(googleprovider);
                }
            });
        });

        // facebook signup with popup
        ChatBot.$body.on('click', '.facebookLogin', function (e) {
            ChatBot.auth.signInWithPopup(facebookprovider).catch((error) => {
                console.log(error)
                // Handle Errors here.
                const errorCode = error.code;
                if (errorCode === "auth/popup-closed-by-user") {
                    // try redirect login
                    console.log("try facebook redirect login!!!")
                    //ChatBot.auth.signInWithRedirect(facebookprovider);
                }

            });
        })

        // Twitter signup with popup
        ChatBot.$body.on('click', '.twitterLogin', function (e) {

            ChatBot.auth.signInWithPopup(twitterprovider).catch((error) => {
                // Handle Errors here.
                const errorCode = error.code;
                if (errorCode === "auth/popup-closed-by-user") {
                    // try redirect login
                    console.log("try twitter redirect login!!!")
                    ChatBot.auth.signInWithRedirect(twitterprovider);
                }

            });
        })

        // Auth Logout
        $('.logoutbtn').click(function () {
            return authLogout();
        });

    }
})(jQuery);


(function ($) {
    // Initialize Method after document has been loaded
    ChatBot.init = function () {                           // Initialize Slider
        ChatBot.authenticationApp(); // The Authentication App
        ChatBot.chatbotApp();
    };
})(jQuery);
/**
 * App Initializer
 */
(function ($) {
    'use strict';

    window.onload = function () {
        // Canvas Size
        ChatBot.canvasWidth = window.innerWidth;
        ChatBot.resizeTimeStamp = 0;
        ChatBot.resizeChanged = false;

        // loaded
        ChatBot.status = 'loaded';
        document.body.classList.add('loaded');
        ChatBot.call(ChatBot.init);
        ChatBot.status = 'complete';
    }
})(jQuery);
