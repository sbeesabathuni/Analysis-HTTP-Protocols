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