import handlebars from 'handlebars';

// Register a helper to check if an object or array is empty
handlebars.registerHelper('isEmpty', function (value) {
    return (
        (Array.isArray(value) && value.length === 0) ||
        (typeof value === 'object' && Object.keys(value).length === 0)
    );
});
