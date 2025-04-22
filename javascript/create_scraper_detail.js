import fetch from "node-fetch";
import fs from "fs";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const url = "https://api.minexa.ai/scraper/";
const api_key = "YOUR_API_KEY";

const data = {
    // Copy paste the data from the website directly without any modification to train the scraper
    // or Write a short description of your required data, for example: "clinical trials study overview"
    "look_for": `Study Overview
    Brief Summary
    The gold standard after shoulder resection for tumors is reconstruction by reverse prosthesis and allograft. This is an intervention also performed for more frequent etiologies (revisions of prosthesis, non cancerous humeral bone loss ...).

    The results in these etiologies are good, and do not find any particular mechanical complications (including no osteolysis of the graft). In the case of reconstruction for cancer, the numbers of patients are lower (rare pathologies) and some studies on small numbers found osteolysis of the allograft. The aim of this study is to analyze the presence or not osteolysis in these patients, and to quantify it precisely by scanner measurement (no data yet in the literature).

    Detailed Description
    quantify bone stock of the allograft by scanner measurement in post operative and in 6 month to 1 years after surgery.

    This is a retrospective study, and the scanner was performed routinely every 3 to 6 month, during 2 years, for oncological follow up.

    Official Title
    Results of Proximal Humeral Reconstruction With Allograft Prosthetic Composite After Resection for Tumors
    Conditions
    Shoulder Disease
    Intervention / Treatment
    Procedure: proximal humeral resection for tumor and allograft prosthetic composite reconstruction
    Other Study ID Numbers
    2024PI059`,
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

console.log("Creating scraper.. This may take up to 2 minutes");

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

    const scraper_id = data.response.id;
    const file_path = `${__dirname}/scraper_id_${scraper_id}.json`;

    fs.writeFile(file_path, JSON.stringify(data, null, 4), (err) => {
      if (err) throw err;
      console.log(`Full scraper json saved at: ${file_path}`);
    });
  })
  .catch((error) => {
    console.error(error);
  });
