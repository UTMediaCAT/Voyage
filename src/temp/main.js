/* crawl.js
   Author: Sherry Ma, Raiyan Rahman
   Description: This script takes in one url and then crawl the
   dynamically rendered webpages and it prints the result through console log.
   Use: "node main.js -l <url>"
*/
// This is the main Node.js source code file of your actor.
// It is referenced from the "scripts" section of the package.json file,
// so that it can be started by running "npm start".

// Include Apify SDK. For more information, see https://sdk.apify.com/
const Apify = require('apify');
var fs = require('fs');
var util = require('util');
var log_file = fs.createWriteStream(__dirname + '/debug.log', {flags : 'w'});
var log_stdout = process.stdout;

console.log = function(d) {
  log_file.write(util.format(d) + '\n');
  log_stdout.write(util.format(d) + '\n');
};


Apify.main(async () => {
    // Get input of the actor (here only for demonstration purposes).
    // If you'd like to have your input checked and have Apify display
    // a user interface for it, add INPUT_SCHEMA.json file to your actor.
    // For more information, see https://apify.com/docs/actor/input-schema

    var is_url = false;
    var url_list = [];
    process.argv.forEach(function (val, index, array) {
        // Add the links.
        if(is_url) {
            url_list.push(val);
        }
        // If it is a flag for the link.
        if (val === "-l") {
            is_url = true;
        }
      });
    console.log(url_list);  // Ouput the links provided.

    var output_dict = {};

    if (!url_list[0]) throw new Error('Input must be a JSON object with the "url" field!');

    console.log('Launching Puppeteer...');
    const browser = await Apify.launchPuppeteer({
        headless: true,
        stealth: false,
        useChrome: false,
    });

    console.log(`Opening page ${url_list[0]}...`);
    const page = await browser.newPage();
    await page.setDefaultNavigationTimeout(0); 
    await page.goto(url_list[0]);
    const title = await page.title();
    console.log(`Title of the page "${url_list[0]}" is "${title}".`);

    const hrefs = await page.$$eval('a', as => as.map(a => a.href));    // Get all the hrefs with the links.
    const titles = await page.$$eval('a', as => as.map(a => a.title));  // Get the titles of all the links.
    const texts = await page.$$eval('a', as => as.map(a => a.text));    // Get the text content of all the a tags.
    
    // Create the list of tuples for this url.
    var tuple_list = [];
    // Set the title of the link to be the text content if the title is not present.
    for (let i = 0; i < hrefs.length; i++) {
        hrefLink = hrefs[i];
        if (titles[i].length === 0) {
            hrefTitle = texts[i].replace(/ +(?= )/g,'');
        } else {
            hrefTitle = titles[i];
        }
        // Add the tuple to the list.
        tuple_list.push([hrefLink, hrefTitle]);
    }

    // Add this list to the dict.
    output_dict[url_list[0]] = tuple_list;
    console.log(JSON.stringify(output_dict));
    
    await browser.close();
});
