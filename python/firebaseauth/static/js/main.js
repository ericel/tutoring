/**
 * FirebaseAuth Javascript File
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
     * FirebaseAuth Object
     */
window.FirebaseAuth = {};
/**
 * FirebaseAuth Base
 */
(function ($) {
    
    /**
     * jQuery Window Handle
     * 
     * @var jQuery jQuery window handle
     */
    FirebaseAuth.$window = $(window);

    /**
     * jQuery Body Handle
     * 
     * @var jQuery jQuery body handle
     */
    FirebaseAuth.$body = $(document.body);

    /**
     * Status
     * 
     * @var string Status
     */
    FirebaseAuth.status = '';

    /**
     * Check if the browser is internet explorer.
     * 
     * @var boolean isIE
     */
    FirebaseAuth.isIE = navigator.userAgent.indexOf('Trident') >= 0;

    /**
     * Check if the browser is internet explorer.
     *
     * @var boolean isIE
     */
    FirebaseAuth.isEdge = navigator.userAgent.indexOf('Edge') >= 0;
    FirebaseAuth.isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

    /**
     * Make a macro task
     * 
     * @param {function} fn
     * @param {number} delay
     * @return {void}
     */
    FirebaseAuth.call = function (fn, delay) {
        setTimeout(fn, delay);
    }

    /**
     * Parse options string to object
     *
     * @param {string} options
     * @return {object} options
     */
    FirebaseAuth.parseOptions = function (options) {
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
    FirebaseAuth.parseTemplate = function (template, vars) {
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
    FirebaseAuth.byId = function (id) {
        return document.getElementById(id);
    }

    /**
     * Get dom elements by tagName
     *
     * @param {string} tagName
     * @param {HTMLElement} element this can be omitted.
     * @return {HTMLCollection}
     */
    FirebaseAuth.byTag = function (tagName, element) {
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
    FirebaseAuth.byClass = function (className, element) {
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
    FirebaseAuth.setCookie = function (name, value, exdays) {
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
    FirebaseAuth.getCookie = function (name) {
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

    /**
   * ERROR & SUCCESS alert
   */
  FirebaseAuth.alertSuccess = function (message, notifyclass) {
    $(`.${notifyclass}`).css("display", "block");
    $(`.${notifyclass}`)
      .html(`<div style="color:green;">
         <h4>Success!</h4> ${message}
         </button>
     </div>
    `); // add the error to the dom

    setTimeout(function () {
      $(`.${notifyclass}`).css("display", "none");
    }, 5000);
  };

  FirebaseAuth.alertError = function (message, notifyclass) {
    $(`.${notifyclass}`).css("display", "block");
    $(`.${notifyclass}`)
      .html(`<div style="color:red;">
             <h4>Oops!</h4> ${message} 
         </div>`); // add the error to the dom

    setTimeout(function () {
      $(`.${notifyclass}`).css("display", "none");
    }, 5000);
  };
})(jQuery);


(function ($) {
    FirebaseAuth.authenticationApp = function () {
        // class public variables
        const googleprovider = new firebase.auth.GoogleAuthProvider();
        const facebookprovider = new firebase.auth.FacebookAuthProvider();
        const twitterprovider = new firebase.auth.TwitterAuthProvider();
        const csrftoken = FirebaseAuth.getCookie("csrftoken");
    
        const config = {
           [FIREBASE WEB PROJECT SETTINGS GO HERE]
        };
        firebase.initializeApp(config);
        FirebaseAuth.auth = firebase.auth();
    
        // Check is email
        function IsEmail(email) {
          var regex =
            /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
          if (!regex.test(email)) {
            return false;
          } else {
            return true;
          }
        }
    
        // Logout User Front and backend
        function authLogout() {
          FirebaseAuth.auth.signOut().then(
            function () {
              // Sign-out successful.
              console.log("logged Out successfully!!");
              window.location.href = "/account/logout";
            },
            function (error) {
              // An error happened.
            }
          );
        }
    
        //this.authLogout();
        FirebaseAuth.auth
          .getRedirectResult()
          .then(async (result) => {
            if (result.user) {
              result.user.getIdToken().then((idToken) => {
                handleMethod(idToken, false);
              });
            }
            //console.log(user)
          })
          .catch((error) => {
            // Handle Errors here.
            const errorCode = error.code;
            console.log(error);
          });
        // Check if there is a logged in user
        // If not, and auth is present
        // logged them in backend
        FirebaseAuth.auth.onAuthStateChanged((user) => {
          if (user !== null) {
            if ($("body.anonymous")[0]) {
              // Logged in on Front End but not Backend
              user.getIdToken().then((idToken) => {
                handleMethod(idToken, false);
              });
            }
          } else if (user === null && $("body.anonymous")[0]) {
            google.accounts.id.initialize({
              client_id:
                "[GOOGLE IDENTITY CLIENT API ID]", // Get this from your google apps credentials
              callback: handleCredentialResponse,
              auto_select: "false",
              ux_mode: "redirect", //popup// redirect//popup
              prompt_parent_id: "g_id_onload",
              login_uri: `${window.location.origin}/api/account/google_prompt_login/`,
              style: "position: fixed; top: 40px; right: 30px;  z-index: 1001;",
            });
            google.accounts.id.renderButton(
              document.getElementById("g_id_signin"),
              { theme: "outline", size: "large", width: 250, shape: "pill" } // customization attributes
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
              "X-CSRFToken": FirebaseAuth.getCookie("csrftoken"),
            },
            data: { token: token, GoogleAuth: true }, // data sent with the post request
            // handle a successful response
            success: function (json) {
              // Just Reload Page
              location.reload();
            },
            // handle a non-successful response
            error: function (xhr, errmsg, err) {
              console.log("something went wrong!!!");
              window.location.href = "/account/logout";
            },
          });
        }
    
        // Handle firebackend login
        function handleMethod(token, googleAuth) {
          $.ajax({
            url: "/api/account/auth2/", // the endpoint
            type: "POST", // http method
            headers: {
              "X-CSRFToken": FirebaseAuth.getCookie("csrftoken"),
            },
            data: { token: token, GoogleAuth: googleAuth }, // data sent with the post request
            // handle a successful response
            success: function (json) {
              // Just Reload Page
              FirebaseAuth.alertSuccess("Success in login.", "alert-notify");
    
              location.reload();
            },
            error: function (xhr, errmsg, err) {
              // handle a non-successful response
              //self.authLogout();
              setTimeout(function () {
                if (el) {
                  $("document").removeClass("load-more-overlay loading");
                }
                FirebaseAuth.alertError(xhr.responseText, "alert-notify");
              }, 5000);
            },
          });
        }
    
        // google signup with popup
        FirebaseAuth.$body.on("click", ".googleLogin", function (e) {
          e.preventDefault();
          $(this).addClass("load-more-overlay loading");
          FirebaseAuth.auth.signInWithPopup(googleprovider).catch((error) => {
            console.log(error);
            // Handle Errors here.
            const errorCode = error.code;
            if (errorCode === "auth/popup-closed-by-user") {
              // try redirect login
              console.log("try google redirect login!!!");
              //FirebaseAuth.auth.signInWithRedirect(googleprovider);
            }
          });
        });
    
        // facebook signup with popup
        FirebaseAuth.$body.on("click", ".facebookLogin", function (e) {
          e.preventDefault();
          $(this).addClass("load-more-overlay loading");
          FirebaseAuth.auth.signInWithPopup(facebookprovider).catch((error) => {
            console.log(error);
            // Handle Errors here.
            const errorCode = error.code;
            if (errorCode === "auth/popup-closed-by-user") {
              // try redirect login
              console.log("try facebook redirect login!!!");
              //FirebaseAuth.auth.signInWithRedirect(facebookprovider);
            }
          });
        });
    
        // Twitter signup with popup
        FirebaseAuth.$body.on("click", ".twitterLogin", function (e) {
          e.preventDefault();
          $(this).addClass("load-more-overlay loading");
          FirebaseAuth.auth.signInWithPopup(twitterprovider).catch((error) => {
            // Handle Errors here.
            const errorCode = error.code;
            if (errorCode === "auth/popup-closed-by-user") {
              // try redirect login
              console.log("try twitter redirect login!!!");
              FirebaseAuth.auth.signInWithRedirect(twitterprovider);
            }
          });
        });
    
      
      
    
        // Auth Logout
        FirebaseAuth.$body.on("click", ".logoutbtn", function (e) {
          return authLogout();
        });
    
      
       
      };
})(jQuery);


(function ($) {
    // Initialize Method after document has been loaded
    FirebaseAuth.init = function () {                           // Initialize Slider
        FirebaseAuth.authenticationApp(); // The Authentication App
    };
})(jQuery);
/**
 * App Initializer
 */
(function ($) {
    'use strict';

    window.onload = function () {
        // Canvas Size
        FirebaseAuth.canvasWidth = window.innerWidth;
        FirebaseAuth.resizeTimeStamp = 0;
        FirebaseAuth.resizeChanged = false;

        // loaded
        FirebaseAuth.status = 'loaded';
        document.body.classList.add('loaded');
        FirebaseAuth.call(FirebaseAuth.init);
        FirebaseAuth.status = 'complete';
    }
})(jQuery);
