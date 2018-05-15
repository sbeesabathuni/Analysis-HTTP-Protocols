var fs = require('fs');
var spdy = require('spdy');

var lessobjectslesssize = fs.readFileSync('lessobjectslesssize.html');
var moreobjectslesssize = fs.readFileSync('moreobjectslesssize.html');
var lessobjectsmoresize = fs.readFileSync('lessobjectsmoresize.html');
var moreobjectsmoresize = fs.readFileSync('moreobjectsmoresize.html');

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
    case "/lessobjectslesssize":
      headers['Content-Type'] = 'text/html';
      body = lessobjectslesssize
      break;
    case "/moreobjectslesssize":
      headers['Content-Type'] = 'text/html';
      body = moreobjectslesssize
      break;
    case "/lessobjectsmoresize":
      headers['Content-Type'] = 'text/html';
      body = lessobjectsmoresize
      break;
    case "/moreobjectsmoresize":
      headers['Content-Type'] = 'text/html';
      body = moreobjectsmoresize
      break;
    case "/favicon.ico":
      //headers['Content-Type'] = 'text/html';
      body = ""
      break;
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

server.listen(8083, function(){
  console.log("SPDY Server started on 8083");
});

