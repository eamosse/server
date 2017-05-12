var MongoClient = require("mongodb").MongoClient;

exports.findAll = function (req, res, next) {
    //res.send(sessions);
    MongoClient.connect("mongodb://localhost/solutions", function(error, db) {
    if (error) {
        res.send(error);
    }
    db.collection("cities").find().toArray(function (error, results) {
        if (error) res.send(error);
        res.send(results);
    })
});
};

exports.findById = function (req, res, next) {
    var id = req.params.id;
    res.send(sessions[id]);
};