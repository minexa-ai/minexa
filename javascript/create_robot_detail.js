import fetch from "node-fetch";
import fs from "fs";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const url = "https://api.minexa.ai/robot/";
const api_key = "JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP";

const data = {
  look_for: "Features",
  urls: [
    "https://clinicaltrials.gov/study/NCT06382792",
    "https://clinicaltrials.gov/study/NCT06382779",
    "https://clinicaltrials.gov/study/NCT06382753",
    "https://clinicaltrials.gov/study/NCT06382727",
  ],
  mode: "detail",
};

const headers = {
  "Content-Type": "application/json",
  "api-key": api_key,
};

fetch(url, {
  method: "POST",
  headers: headers,
  body: JSON.stringify(data),
})
  .then((response) => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error(`Error status code ${response.status} occurred`);
    }
  })
  .then((data) => {
    console.log(
      "Please confirm container is well located:",
      data.response.web_app
    );

    const robot_id = data.response.id;
    const file_path = `${__dirname}/robot_id_${robot_id}.json`;

    fs.writeFile(file_path, JSON.stringify(data, null, 4), (err) => {
      if (err) throw err;
      console.log(`Full robot json saved at: ${file_path}`);
    });
  })
  .catch((error) => {
    console.error(error);
  });
