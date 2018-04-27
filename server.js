var express = require('express');
var app = express();
var bodyParser = require('body-parser');
const NewsAPI = require('newsapi');
const newsapi = new NewsAPI('3de1dfbfc34546a287444f31f5c6465c');
const low = require('lowdb')
const FileSync = require('lowdb/adapters/FileSync')

const adapter = new FileSync('db.json')
const db = low(adapter)


app.use(express.static(__dirname + '/public'));                 // set the static files location /public/img will be /img for users
app.use(bodyParser.urlencoded({'extended':'true'}));
app.use(bodyParser.json());
app.use(bodyParser.json({ type: 'application/vnd.api+json' }));

// listen (start app with node server.js)
app.listen(8080);
console.log("App listening on port 8080");

app.get('/', function(req, res) {
    res.sendfile('./public/index.html'); // load the single view file (angular will handle the page changes on the front-end)
});

//get all sources
app.get('/api/sources', function(req, res) {
   newsapi.v2.sources({
     language: 'en',
   }).then(response => {
    //sending only id and name back to the UI
     var obj = {}
     var key = 'sources';
     obj[key] = [];
     for (var i=0;i<response.sources.length;i++) {
        var requiredObj = {"id": response.sources[i].id, "name": response.sources[i].name};
        obj[key].push(requiredObj);
     }
     if (response.status === "ok") {
        res.json(obj);
     } else {
        res.send("Could not fetch sources");
     }

   });
});

//get all saved articles from the db
app.get('/api/getfavarticles', function(req, res) {
    var savedArticles = db.get('savedArticles').value()
    res.json(savedArticles);
});

//Get articles by source
app.get('/api/articlesbysource/:sourceId', function(req, res) {

    newsapi.v2.everything({
      sources: req.params.sourceId,
      language: 'en',
      sortBy: 'relevancy',
      pageSize: 10
    }, (err, articlesResponse) => {
           if (err)  {
             res.send("No articles available for this source");
             console.error(err);
           }
           else  {
             res.json(articlesResponse.articles);
           }
         });
});

//save an article to db
app.post('/api/savearticle', function(req, res){
    // Add an article
    db.get('savedArticles')
      .push({ id: req.body.id, name: req.body.name, title: req.body.title, publishedAt: req.body.publishedAt,
      description: req.body.description, author: req.body.author, urlToImage: req.body.urlToImage})
      .write()

    var savedArticles = db.get('savedArticles').value()

    res.json(savedArticles);

});

//Remove a saved article
app.delete('/api/removearticle/:title', function(req, res){
    // Remove an article
    db.get('savedArticles')
      .remove({ title: req.params.title})
      .write()

    var savedArticles = db.get('savedArticles').value()
    res.json(savedArticles);

});

//Verify Log in
app.post('/api/login', function(req, res){
    var user = db
      .get('users')
      .find({ username: req.body.username, password: req.body.password})
      .value()

    if (typeof user === "undefined") {
        res.send("Username or password is incorrect. Please Try again");
    } else {
        res.send(user);
    }

});




