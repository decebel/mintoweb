if (window.location.search) {
    var promise = SYMPHONY.remote.hello().catch(function (data) {
        console.log(data);
    }).then(function (data) {
        SYMPHONY.application.connect('obe', ['ui', 'modules', 'applications-nav'], ['obe:module']).then(function (response) {
            //subscribe to system services
            var userId = response.userReferenceId;
            this.uiService = SYMPHONY.services.subscribe('ui');
            this.navService = SYMPHONY.services.subscribe('applications-nav');
            this.modulesService = SYMPHONY.services.subscribe('modules');

            //subscribe to the service we created in the controller.js file
            this.controllerService = SYMPHONY.services.subscribe('obe:controller');

            main();
        }.bind(this))
    }.bind(this));
} else {
    var navService = {
        count: function (a, b) {

        }
    }

    main();
}

function main() {

    setToasterSettings();
    var ObeViewModel = Backbone.Model.extend({
        initialize: function () {
            this.get("alerts").on("add", this.onAlertAdded, this);
            this.get("alerts").on("change:status", this.onStatusChange, this);
        },
        onStatusChange: function (change) {
            refreshNavCount();

            this.updateStatusChartModel();
        },

        onAlertAdded: function (addedAlert) {
            addAlertNotification(addedAlert);
            refreshNavCount();
            filterInt();
            this.refresh();
        },
        refresh: function () {
            this.setCategories();
            this.setCategorySums();
            this.updateTypeChartModel();
            this.updateStatusChartModel();
        },
        search: function (event, context) {
            filterInt();
        },
        filter: function (event, context) {
            context.model.set("filterString", context.category);
            filterInt();
        },
        clearSearchString: function (event, context) {
            context.model.set("searchString", undefined);
            filterInt();
        },
        setSelectedAlert: function (event, rivetsBinding) {
            rivetsBinding.model.set("selectedAlert", rivetsBinding.alert);
        },
        flagSelectedAlert: function (event, rivetsBinding) {
            rivetsBinding.model.get("selectedAlert").set("status", true);
            $('#alertDetailModal').modal('hide');
        },
        dismissSelectedAlert: function (event, rivetsBinding) {
            rivetsBinding.model.get("selectedAlert").set('status', false);
            $('#alertDetailModal').modal('hide');
        },
        setCategories: function () {
            var matches = this.get("alerts");
            this.set("labels",
                Array.from(
                    new Set(union(matches.map(function (el) {
                        return el.get("category");
                    }), addedCategories)
                    )));
        },
        setCategorySums: function () {
            var sums = [];
            var categories = this.get("labels");
            var matches = this.get("alerts");

            categories.forEach(function (category) {
                var s = matches.filter(function (val) {
                    return val.get("category") === category;
                });
                sums.push(s.length);
            })
            this.set("sums", sums);
            this.set("sumTotal", sums.reduce(function (pv, cv) { return pv + cv; }, 0))
        },
        updateTypeChartModel: function () {
            this.get("typeChartModel").set("chartData", new Backbone.Model({
                labels: this.get("labels"),
                sums: this.get("sums"),
                colors: getCategoryColors(this.get("labels").length),
                title: this.get("sumTotal") + " Alerts"
            }));
        },
        updateStatusChartModel: function () {
            this.get("statusChartModel").set("chartData", new Backbone.Model({
                labels: [flaggedString, dismissedString, pendingReviewString],
                sums: [
                    this.get("alerts").where({ status: true }).length,
                    this.get("alerts").where({ status: false }).length,
                    this.get("alerts").reject(
                        function (alert) {
                            return alert.has("status");
                        }).length
                ],
                colors: [flaggedColor, dismissedColor, pendingReviewColor],
                title: Math.floor(this.get("alerts").where({ status: true }).length / this.get("alerts").length * 100) + "% Flagged"
            }));
        }
    });

    function refreshNavCount() {
        navService.count("obe-nav", viewmodel.get("alerts").reject(
            function (alert) {
                return alert.has("status");
            }).length);

    }

    function filterInt() {
        var filterString = viewmodel.get("filterString");
        var searchString = viewmodel.get("searchString");
        var alertSet = viewmodel.get("filteredAlerts");
        if (!filterString && (!searchString || searchString === '')) {
            alertSet.reset(viewmodel.get("alerts").models);
        } else {
            alertSet.reset(viewmodel.get("alerts").filter(function (alertValue) {
                var containsSearchString = searchString === undefined ||
                    searchString === '' ||
                    alertValue.get("category").toLowerCase().includes(searchString) ||
                    alertValue.get("message").toLowerCase().includes(searchString) ||
                    alertValue.get("to").toLowerCase().includes(searchString) ||
                    alertValue.get("from").toLowerCase().includes(searchString) ||
                    convertStatusToText(alertValue.get("status")).toLowerCase().includes(searchString);

                var equalsCategory = filterString === undefined || alertValue.get("category") === filterString;

                return containsSearchString && equalsCategory;
            }));
        }
    };

    var ChartView = Backbone.View.extend({
        initialize: function () {
            this.listenTo(this.model, "change", this.render);
            this.render();
        },
        render: function () {
            var categories = this.model.get("chartData").get("labels");
            var categorySums = this.model.get("chartData").get("sums");
            var categoryColors = this.model.get("chartData").get("colors");
            var title = this.model.get("chartData").get("title");
            var data = {
                labels: categories.map(function(c){
                    return c + ": " + categorySums[categories.indexOf(c)];
                }),
                datasets: [
                    {
                        data: categorySums,
                        backgroundColor: categoryColors,
                        hoverBackgroundColor: categoryColors,
                    }]
            };
            var myDoughnutChart = new Chart(this.el, {
                type: 'doughnut',
                data: data,
                options: {
                    legend: {
                        position: "right",
                        fullWidth: false
                    },
                    cutoutPercentage: 80,
                    animation: {
                        onComplete: function (animation) {
                            // Draw info in the centre
                            var ctx = animation.chartInstance.chart.ctx;
                            var cx = myDoughnutChart.chartArea.right / 2;
                            var cy = myDoughnutChart.chartArea.bottom / 2;
                            // horizontally align text around the specified point (cx)
                            ctx.textAlign = 'center';
                            // vertically align text around the specified point (cy)
                            ctx.textBaseline = 'middle';
                            ctx.font = '20px Lato';
                            ctx.fillStyle = '#2c3e50';
                            ctx.fillText(title, cx, cy);
                        }
                    },
                    tooltips: {
                        callbacks: {
                            label: function (tooltipItem, data) {
                                return data.labels[tooltipItem.index];
                            }
                        }
                    }
                }
            });
        }
    });
    var viewmodel;
    $(document).ready(function () {

        getMatches()
            .then(function (result) {

                var initAlerts = new Backbone.Collection(result.data);
                viewmodel = new ObeViewModel(
                    {
                        alerts: initAlerts,
                        typeChartModel: new Backbone.Model(),
                        statusChartModel: new Backbone.Model(),
                        filteredAlerts: initAlerts.clone()
                });
                this.viewmodel = viewmodel;
                refreshNavCount();
                setRivetsFormatters();
                viewmodel.refresh();
                rivets.bind($("#dashboardContainer"), { model: viewmodel });
                var statusChart = new ChartView({ el: "#categoryChart", model: viewmodel.get("typeChartModel") });
                var typeChart = new ChartView({ el: "#statusChart", model: viewmodel.get("statusChartModel") });

                var socket = io('http://localhost:5000');
                // var onevent = socket.onevent;
              // socket.onevent = function (packet) {
              //    var args = packet.data || [];
              //    onevent.call (this, packet);    // original call
              //    packet.data = ["*"].concat(args);
              //    onevent.call(this, packet);      // additional call to catch-all
              // };


              //   socket.on("*",function(event,data) {
              //      console.log(event);
              //      console.log(data);
              //      viewmodel.get("alerts").unshift(data);
              //   });

                socket.on('updates', function (data) {
                    console.log(data);
                    viewmodel.get("alerts").unshift(data);
                })
            })

    });

    function setRivetsFormatters() {
        rivets.binders.categorycolor = function (el, value) {
            var i = viewmodel.get("labels").indexOf(value);
            el.style.backgroundColor = categoryColors[i];
        };
        rivets.binders.statuscolor = function (el, value) {
            if (value === undefined) {
                el.style.backgroundColor = pendingReviewColor;
            }
            if (value === true) {
                el.style.backgroundColor = flaggedColor;
            }
            if (value === false) {
                el.style.backgroundColor = dismissedColor;
            }
        };
        rivets.formatters.status = function (value) {
            return convertStatusToText(value);
        };
        rivets.formatters.eq = function (value, args) {
            return value === args;
        };
        rivets.formatters.negate = function (value) {
            if (value === undefined) {
                return false;
            }
            return !value;
        }
    }

    function addAlertNotification(alertValue) {
        viewmodel.set("selectedAlert", alertValue);
        var messageDiv = document.createElement("div");
        messageDiv.className = "notification-message";
        messageDiv.innerHTML = '<strong>' + alertValue.get("category") + '</strong>: ' + alertValue.get("message");
        $.toaster({ priority: 'danger', title: 'New Alert', message: messageDiv });
    }

    function showAlertDetail(alertValue) {
        alert(alertValue.message);
    }

    function setToasterSettings() {
        $.toaster({
            settings:
            {
                timeout: 5000,
                toast:
                {
                    template:
                    '<div class="alert alert-%priority% alert-dismissible clickable" role="alert" data-toggle="modal" data-target="#alertDetailModal">' +
                    '<button type="button" class="close" data-dismiss="alert">' +
                    '<span aria-hidden="true">&times;</span>' +
                    '<span class="sr-only">Close</span>' +
                    '</button>' +
                    '<p class="title"></p><div><span class="message"></span></div>' +
                    '</div>'
                }
            }
        });
    }
}
