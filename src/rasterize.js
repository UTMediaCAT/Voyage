var page = require('webpage').create(),
    system = require('system'),
    address, output;

if (system.args.length < 2 || system.args.length > 4) {
    console.log('Usage: rasterize.js URL filename  [zoom]');
    phantom.exit(1);
} else {
    address = system.args[1];
    output = system.args[2];

    if (system.args.length > 3) {
        page.zoomFactor = system.args[3];
    }
    page.settings.resourceTimeout = 3000;
    page.viewportSize = { width: 1920, height: 1080 };
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
            phantom.exit(1);
        } else {
            window.setTimeout(function () {
                page.render(output+".pdf");
                page.render(output+".png");
                phantom.exit();
            }, 500);
        }
    });
}
