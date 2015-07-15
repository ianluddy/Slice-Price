Handlebars.registerHelper('decimal', function(value) {
    return new Handlebars.SafeString(value.toFixed(2));
});