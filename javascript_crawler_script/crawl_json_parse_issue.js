/* crawl.js
   Author: Raiyan Rahman
   Date: March 1st, 2020
   Description: This script takes in one or more urls and then crawls those
   dynamically rendered webpages and returns the JSON file containing lists
   of tuples of links and titles for each url.
   Use: "node crawl.js -l <url1> ..."
   Output: link_title_list.json
*/
const Apify = require('apify');
const path = require('path');

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
       result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}
var rand = makeid(6)
var fs = require('fs');
var util = require('util');
var log_file = fs.createWriteStream(__dirname + '/debug-' + rand + '.log', {flags : 'w'});
var log_stdout = process.stdout;

console.log = function(d) {
  log_file.write(util.format(d) + '\n');
  log_stdout.write(util.format(d) + '\n');
};

Apify.main(async () => {

    try {
        // Get the urls from the command line arguments.
        var url_list = [];
        var is_url = false;
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
        console.log("HIIIIIIIIIIIIIIIIIIIIIIIIII");
        console.log(url_list);  // Ouput the links provided.
        console.log("printed url list")

        // Create the JSON object to store the tuples of links and titles for each url.
        var output_dict = {};
        const requestQueue = await Apify.openRequestQueue();


        // Add the links to the queue of websites to crawl.
        for (var i = 0; i < url_list.length; i++) {
            console.log("open requestQueue")
            console.log(url_list[i])

            // str = url_list[i].replace(/^\s+|\s+$/g, '');
            // console.log({ url: str })
            await requestQueue.addRequest({ url: url_list[i] });
            console.log("close requestQueue")

        }
        // Crawl the deeper URLs recursively.
        // const pseudoUrls = [new Apify.PseudoUrl('https://www.idf.il/en/[.*]')];

        // Initialize the crawler.
        const crawler = new Apify.PuppeteerCrawler({
            requestQueue,
            launchPuppeteerOptions: {
                headless: true,
                stealth: false,
                useChrome: false,
            },
            handlePageFunction: async ({ request, page }) => {
                const title = await page.title();   // Get the title of the page.
                console.log(`Title of "${request.url}" is "${title}"`);
                // let bodyHTML = await page.evaluate(() => document.body.innerHTML);   // Get the HTML content of the page.
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
                output_dict[request.url] = tuple_list;

                // Enqueue the deeper URLs to crawl.
                // await Apify.utils.enqueueLinks({ page, selector: 'a', pseudoUrls, requestQueue });
            },
            // The max concurrency and max requests to crawl through.
            maxRequestsPerCrawl: 100,
            maxConcurrency: 10,
            maxRequestRetries: 5,
            handlePageTimeoutSecs: 3000,
            gotoTimeoutSecs: 90000,
            timeout: 30000

        });
        // Run the crawler.
        await crawler.run();
        
        // Delete the apify storage.
        // Note: If the apify_storage file is not removed, it doesn't crawl
        // during subsequent runs.
        // Implementation of rmdir.
        console.log("BYEEEEEEEEEEEEEE");
        console.log(JSON.stringify(output_dict));
        const rmDir = function (dirPath, removeSelf) {
        if (removeSelf === undefined)
            removeSelf = true;
        try {
            var files = fs.readdirSync(dirPath);
        } catch (e) {
            // throw e
            return;
        }
        if (files.length > 0)
            for (let i = 0; i < files.length; i++) {
            const filePath = path.join(dirPath, files[i]);
            if (fs.statSync(filePath).isFile())
                fs.unlinkSync(filePath);
            else
                rmDir(filePath);
            }
        if (removeSelf)
            fs.rmdirSync(dirPath);
        };
        rmDir('./apify_storage/', true);

        // Create a JSON file from the tuples in the output list.
        // Overwrites if it already exists.
        fs.writeFileSync("link_title_list_json_issue.json", JSON.stringify(output_dict), function(err) {
            if (err) throw err;
            console.log('complete');
            });
    } catch(err) {
        // console.log("error occured, file created at "+ rand + ".log");
        console.log(err);
        return;
    }
    // remove log file if no error occured
    fs.unlink(__dirname + '/debug-' + rand + '.log', () => {
        console.log("success, so delete file "+ rand + ".log");
    });
});