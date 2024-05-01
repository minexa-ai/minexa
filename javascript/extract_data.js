import fs from "fs";
import path from "path";
import fetch from "node-fetch";
import { DateTime } from "luxon";
import _ from "lodash";
import { Parser } from "json2csv";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const url = "https://api.minexa.ai/data/";
const api_key = "JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP"; // free key.

// Your JSON data for the request body
const output_format = "json"; //json/csv

const data = {
  batches: [
    {
      robot_id: 103,
      columns: ["col_1", "col_3"],
      urls: [
        "https://www.britannica.com/topic/list-of-herbs-and-spices-2024392",
      ],
    },
  ],
};

const headers = {
  "Content-Type": "application/json",
  "api-key": api_key,
};

let next_set = null;
let started = 0;
const iterated_data = [];
const extracted_data = [];

const formatted_datetime = DateTime.now().toFormat("yyyy_MM_dd_HH_mm");

(async () => {
  while (next_set || started === 0) {
    // Send a POST request with headers
    data.next = next_set;
    const response = await fetch(url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(data),
    });

    // Check if the request was successful (status code 2xx)
    if (response.ok) {
      const jsonContent = await response.json();

      for (const extractions of jsonContent.response) {
        for (const rows of extractions.results) {
          if (rows.error) {
            continue;
          }
          const row = {};
          for (const [col, value] of Object.entries(rows)) {
            if (typeof value === "string") {
              row[col] = value;
            } else if (Array.isArray(value)) {
              row[col] = value.map((x) => x.value);
            }
          }
          iterated_data.push(row);
        }
      }
      extracted_data.push(...jsonContent.response);

      try {
        // Create and save the file
        const file_path = `${__dirname}/exctraction_${formatted_datetime}.json`;

        // Saving in json format
        fs.writeFileSync(
          `${file_path}.json`,
          JSON.stringify(extracted_data, null, 4)
        );

        const fields = _.uniq(
          _.flatten(iterated_data.map((row) => Object.keys(row)))
        );
        const opts = { fields };
        const parser = new Parser(opts);
        const csv = parser.parse(iterated_data);

        // Print the CSV
        console.log(csv);

        // Saving the csv
        fs.writeFileSync(`${file_path}.csv`, csv);
      } catch (err) {
        console.error(err);
      }

      console.log(`res nbr ${jsonContent.response.length}`);
      if (jsonContent.meta.next) {
        next_set = jsonContent.meta.next;
        console.log("run " + next_set);
        started++;
      } else {
        console.log("finished");
        break;
      }
    } else {
      // Handle the case where the request was not successful
      console.error(`Request failed with status code: ${response.status}`);
      console.error(await response.text());
      break;
    }
  }
})();
