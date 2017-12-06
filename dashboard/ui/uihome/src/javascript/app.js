SYMPHONY.remote.hello().then(function(data) {
    SYMPHONY.application.connect('hello', ['ui', 'modules', 'applications-nav'], ['hello:module']).then(function(response) {

        //subscribe to system services
        var userId = response.userReferenceId;
        var uiService = SYMPHONY.services.subscribe('ui');
        var navService = SYMPHONY.services.subscribe('applications-nav');
        var modulesService = SYMPHONY.services.subscribe('modules');

        //subscribe to the service we created in the controller.js file
        var controllerService = SYMPHONY.services.subscribe('hello:controller');

        //bind a click event handler
        var button = document.getElementById("increment");
        button.addEventListener("click", function(){
            //invoke the nav service to increment the badge count on the left nav
            navService.count("hello-nav", 12);
        });

        //if entering the app via clicking on a cashtag hovercard then log out the URL param
        if (window.location.search && /cashtag/.test(window.location.search)) {
            document.getElementById("cashtag").innerHTML =  "URL parameters: " + window.location.search;
        }
    }.bind(this))
}.bind(this));
