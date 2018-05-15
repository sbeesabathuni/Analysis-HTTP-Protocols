var express = require('express');
var app = express();
var bodyParser = require('body-parser');
//var quic = require('quic');
// set the static files location /public/img will be /img for users
app.use(bodyParser.urlencoded({'extended':'true'}));
app.use(bodyParser.json());
app.use(bodyParser.json({ type: 'application/vnd.api+json' }));

app.use(express.static(__dirname));

// listen (start app with node server.js)
app.listen(9000);
console.log("Http/1.1 server listening on port 9000");

app.get('/', function(req, res) {
    res.sendfile('./demo.html'); // load the single view file (angular will handle the page changes on the front-end)
});

var fs = require('fs');
var spdy = require('spdy');

var options = {
  key: fs.readFileSync('keys/server.key'),
  cert: fs.readFileSync('keys/server.crt'),
  ca: fs.readFileSync('keys/server.csr'),

};


var server = spdy.createServer(options, function(request, response) {
  response.writeHead(200, {'content-type': 'text/html'});
  var message = "No SPDY for you!"
  console.log("Spdy Version : "+request.spdyVersion);
  if (request.isSpdy){
    message = "YAY! SPDY Works!"
  }
  var headers = {}
  var body;
  switch(request.url){
    case "/":
      //headers['Content-Type'] = 'text/html';
      body = ""
      break;
    default:
      body = fs.readFileSync(request.url.substring(1,));
      break;
  }
response.end(body);
});

server.listen(9001, function(){
  console.log("SPDY Server started on 9001");
});
