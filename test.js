var video = document.getElementById('video')
async function getModel() {
    var model = await roboflow
    .auth({
        publishable_key: "7Hl9FLL5IgTbW6A70Nue",
    })
    .load({
        model: "combo-dataset/3",
        version: 3,
    });

    return model;
}

var initialized_model = getModel();

initialized_model.then(function (model) {
    model.detect(video).then(function(predictions) {
        console.log("Predictions:", predictions);
    });
});