var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var quic = require('quic');
// set the static files location /public/img will be /img for users
app.use(bodyParser.urlencoded({'extended':'true'}));
app.use(bodyParser.json());
app.use(bodyParser.json({ type: 'application/vnd.api+json' }));

app.use(express.static(__dirname));

// listen (start app with node server.js)
app.listen(8080);
console.log("App listening on port 8080");

app.get('/', function(req, res) {
    res.sendfile('./index.html'); // load the single view file (angular will handle the page changes on the front-end)
});


app.get('/lessobjectsmoresize', function(req, res) {
    res.sendfile('./lessobjectsmoresize.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/lessobjectslesssize', function(req, res) {
    res.sendfile('./lessobjectslesssize.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/moreobjectslesssize', function(req, res) {
    res.sendfile('./moreobjectslesssize.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/moreobjectsmoresize', function(req, res) {
    res.sendfile('./moreobjectsmoresize.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/objects1', function(req, res) {
    res.sendfile('./objects1.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/objects2', function(req, res) {
    res.sendfile('./objects2.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/objects5', function(req, res) {
    res.sendfile('./objects5.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/objects10', function(req, res) {
    res.sendfile('./objects10.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/objects50', function(req, res) {
    res.sendfile('./objects50.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/5KB', function(req, res) {
    res.sendfile('./5KB.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/10KB', function(req, res) {
    res.sendfile('./10KB.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/100KB', function(req, res) {
    res.sendfile('./100KB.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/200KB', function(req, res) {
    res.sendfile('./200KB.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/500KB', function(req, res) {
    res.sendfile('./500KB.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/1MB', function(req, res) {
    res.sendfile('./1MB.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/10MB', function(req, res) {
    res.sendfile('./10MB.html'); // load the single view file (angular will handle the page changes on the front-end)
});

app.get('/20MB', function(req, res) {
    res.sendfile('./20MB.html'); // load the single view file (angular will handle the page changes on the front-end)
});