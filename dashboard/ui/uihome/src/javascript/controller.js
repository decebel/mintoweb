//create our own service
var tickerService = SYMPHONY.services.register("obe:controller");

SYMPHONY.remote.hello().then(function(data) {
    SYMPHONY.application.register("obe", ["ui", "modules", "applications-nav"], ["obe:controller"]).then(function(response) {

        //system services
        var userId = response.userReferenceId;
        var uiService = SYMPHONY.services.subscribe("ui");
        var navService = SYMPHONY.services.subscribe("applications-nav");
        var modulesService = SYMPHONY.services.subscribe("modules");

        //add an entry to the left nav
        navService.add("obe-nav", {title: "Obe"}, "obe:controller");

        //add a button to the hovercard that appears when hovering over cashtags
        //uiService.registerExtension("cashtag", "obe", "obe:controller", {label: "Obé"});

        //implement some methods on our custom service. these will be invoked by user actions
        tickerService.implement({
            select: function(id) {
                //invoke the module service to show our own application in the grid
                modulesService.show("obe", {title: "Obe App"}, "obe:controller", "http://localhost:4000/dashboard.html", {});
            },
           
        });
    }.bind(this))
}.bind(this));
