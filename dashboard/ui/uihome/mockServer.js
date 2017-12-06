var express = require('express');
var app = express();
var fs = require("fs");
var bodyParser = require('body-parser');
var Rx = require('rxjs');
var http = require('http');

var subject = new Rx.Subject();
app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});
app.use(bodyParser.json()); // for parsing application/json
app.use(function (req, res, next) {
    console.log(req.body) // populated!
    next()
})
app.post("/submitchat", function (req, res) {
    subject.next({
        from: req.body.from,
        to: req.body.to,
        message: req.body.message,
        timestamp: getDateTime()
    })
    res.end(JSON.stringify(req.body));

});

app.post("/getsnapshot", function (req, res) {
    res.end(JSON.stringify([{
        category: 'Bloomberg',
        id: 1,
        message: 'So, I got those tickets you want man, I just need to make sure that Im going to get that promotion.',
        from: 'Josh',
        to: 'Harold',
        timestamp: '18-Oct-2017 3:24 PM'
    },
    {
        category: 'Runz',
        id: 5,
        message: 'Might be trying to get one sold to Barkley Management',
        from: 'Josh',
        to: 'Harold',
        timestamp: '18-Oct-2017 3:24 PM'
    },
    {
        category: 'Chat/IM',
        id: 7,
        message: "Market is pricing the current 5 year OTR 2bps cheap. Maybe buy eh? ",
        from: 'Josh',
        to: 'Harold',
        timestamp: '18-Oct-2017 3:24 PM'
    },
        {
        category: 'Chat/IM',
        id: 8,
        message: "I want to offload my position in apple. You want to check with the client? ",
        from: 'Josh',
        to: 'Baseball Jim',
        timestamp: '18-Oct-2017 3:24 PM'
    },
        {
        category: 'Chat/IM',
        id: 9,
        message: "Can we buy HCL @ 123.10",
        from: 'Josh',
        to: 'Harold',
        timestamp: '18-Oct-2017 3:24 PM'
    }]));
});
app.use(express.static(__dirname + "/src/html"));
app.use(express.static(__dirname + "/src"));
app.use(express.static(__dirname + "/dist"));
var server = http.createServer(app)
server.listen(5000,"0.0.0.0");

var io = require("socket.io")(server);
var id = 50;
io.on('connection', function (socket) {
    console.log("Connection to socket");
    var subscription = subject.subscribe(
        function (x) {
            console.log(x.message);
            socket.emit('updates', {
                category: 'Bloomberg',
                id: id++,
                message: x.message,
                from: x.from,
                to: x.to,
                timestamp: x.timestamp
            })
        });
})


function getDateTime() {

    var date = new Date();

    var hour = date.getHours();

    var min = date.getMinutes();
    min = (min < 10 ? "0" : "") + min;

    var year = date.getFullYear();

    var month = date.getMonth() + 1;
    month = (month < 10 ? "0" : "") + month;

    var day = date.getDate();
    day = (day < 10 ? "0" : "") + day;

    var ampm = "AM";
    if (hour >= 12) {
        if (hour > 12) {
            hour = hour - 12;
        }
        ampm = "PM";
    }

    return day+"-"+month+"-"+year + " " + hour + ":" + min + " " +ampm;
}
