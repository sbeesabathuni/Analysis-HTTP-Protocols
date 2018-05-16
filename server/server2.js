'use strict'

const fs = require('fs')
const path = require('path')
const http2 = require('http2')
const helper = require('./helper')

var express = require('express');
var app = express();
var bodyParser = require('body-parser');
// set the static files location /public/img will be /img for users
app.use(bodyParser.urlencoded({'extended':'true'}));
app.use(bodyParser.json());
app.use(bodyParser.json({ type: 'application/vnd.api+json' }));

app.use(express.static(__dirname));

const { HTTP2_HEADER_PATH } = http2.constants
const PORT = process.env.PORT || 3000
const PUBLIC_PATH = path.join(__dirname, '../server')

const publicFiles = helper.getFiles(PUBLIC_PATH)

const server = http2.createSecureServer({
  cert: fs.readFileSync(path.join(__dirname, '../server/keys/cert.pem')),
  key: fs.readFileSync(path.join(__dirname, '../server/keys/key.pem'))
}, onRequest)

// Push file
function push (stream, path) {

  const file = publicFiles.get(path)

  if (!file) {
    return
  }

  console.log("file.fileDescriptor !!!!!!"+file.fileDescriptor);
  console.log("file.headers !!!!!!"+file.headers);
  console.log("stream : "+stream);
  console.log("path :"+path);

  stream.pushStream({ [HTTP2_HEADER_PATH]: path }, (pushStream) => {
    pushStream.respondWithFD(file.fileDescriptor, file.headers)
  })
}

// Request handler
function onRequest (req, res) {
    console.log("req.url===="+req.url);
  const reqPath = req.url === '/' ? '/index.html' : req.url
  const file = publicFiles.get(reqPath)
    //console.log("file======"+file);
  // File not found
  if (!file) {
    res.statusCode = 404
    res.end()
    return
  }

     if (reqPath === '/moreobjectslesssize.html') {
       push(res.stream, '/images/MOSS/img1.jpeg')
       push(res.stream, '/images/MOSS/img3.jpg')
       push(res.stream, '/images/MOSS/img5.jpg')
       push(res.stream, '/images/MOSS/img31.jpg')
       push(res.stream, '/images/MOSS/img51.jpg')
       push(res.stream, '/images/MOSS/img32.jpg')
       push(res.stream, '/images/MOSS/img52.jpg')
       push(res.stream, '/images/MOSS/img4.png')
       push(res.stream, '/images/MOSS/img41.png')
       push(res.stream, '/images/MOSS/img42.png')
     }


  // Serve file
  res.stream.respondWithFD(file.fileDescriptor, file.headers)
}

server.listen(PORT, (err) => {
  if (err) {
    console.error(err)
    return
  }

  console.log(`Server listening on ${PORT}`)
})
