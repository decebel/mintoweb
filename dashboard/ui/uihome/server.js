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
app.use(express.static(__dirname + "/src/html"));
app.use(express.static(__dirname + "/src"));
app.use(express.static(__dirname + "/dist"));

var server = http.createServer(app)
//server.listen(4000,"0.0.0.0");
server.listen(4000,"127.0.0.1")
