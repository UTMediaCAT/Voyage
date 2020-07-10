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
var log_file = fs.createWriteStream(__dirname + '/js_log/debug-' + rand + '.log', {flags : 'w'});
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

    try {
        var is_url = false;
        var is_file = false;
        var url_list = [];
        var result_file_name = "";
        process.argv.forEach(function (val, index, array) {
            // Add the links.
            if(is_url) {
                url_list.push(val);
                is_url = false;
            }
            if (is_file) {
                result_file_name = val;
            }
            // If it is a flag for the link.
            if (val === "-l") {
                is_url = true;
            }
            if (val === "-f") {
                is_file = true;
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
        await page.setDefaultNavigationTimeout(600000); 
        await page.goto(url_list[0]);
        const title = await page.title();
        console.log(`Title of the page "${url_list[0]}" is "${title}".`);

        const hrefs = await page.$$eval('a', as => as.map(a => a.href));    // Get all the hrefs with the links.
        const titles = await page.$$eval('a', as => as.map(a => a.title));  // Get the titles of all the links.
        const texts = await page.$$eval('a', as => as.map(a => a.text));    // Get the text content of all the a tags.
        if (url_list[0].includes("idf.il")) {
            console.log(titles);
            console.log(hrefs);
            console.log("hi");
            // console.log(texts);
        }
        // Create the list of tuples for this url.
        var tuple_list = [];
        // Set the title of the link to be the text content if the title is not present.
        for (let i = 0; i < hrefs.length; i++) {
            hrefLink = hrefs[i];
            if (titles[i] == undefined || titles[i] == null) {
                titles[i] = "";
            }
            if (titles[i] && titles[i].length === 0) {
                hrefTitle = texts[i];//.replace(/ +(?= )/g,'');
            } else {
                hrefTitle = titles[i];
            }
            // Add the tuple to the list.
            tuple_list.push([hrefLink, hrefTitle]);
        }

        // Add this list to the dict.
        output_dict[url_list[0]] = tuple_list;
        // console.log(JSON.stringify(output_dict));
        
        await browser.close();
        
        
        // write result to file
        var dirPath = __dirname + '/result_file/';
        // console.log(dirPath)
        // rmDir(dirPath, false);
        console.log(dirPath + result_file_name);

        // Create a JSON file from the tuples in the output list.
        // Overwrites if it already exists.
        fs.writeFileSync(dirPath + result_file_name, JSON.stringify(output_dict));
        //  function(err) {
        //     if (err) {
        //         console.log("error occured");
        //         console.log(err);
        //         throw err;
        //     }
        // });

    } catch(err) {
        // console.log("error occured, file created at "+ rand + ".log");
        console.log(err);
        return;
    }

    // remove log file if no error occured
    fs.unlink(__dirname + '/js_log/debug-' + rand + '.log', () => {
        console.log("success, so delete file "+ rand + ".log");
    });
});


// draft:

// var result_file = fs.createWriteStream(__dirname + '/result_file/' + result_file_name, {flags : 'w'});
// fs.writeFileSync("link_title_list.json", JSON.stringify(output_dict), function(err) {
//     if (err) throw err;
//     console.log('complete');
//     });

// const rmDir = function (dirPath, removeSelf) {
//     if (removeSelf === undefined)
//         removeSelf = true;
//     try {
//         var files = fs.readdirSync(dirPath);
//     } catch (e) {
//         // throw e
//         return;
//     }
//     if (files.length > 0)
//         for (let i = 0; i < files.length; i++) {
//         const filePath = path.join(dirPath, files[i]);
//         if (fs.statSync(filePath).isFile())
//             fs.unlinkSync(filePath);
//         else
//             rmDir(filePath);
//         }
//     if (removeSelf)
//         fs.rmdirSync(dirPath);
// };