import fetch from "node-fetch";
import fs from "fs";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const url = "https://api.minexa.ai/scraper/";
const api_key = "YOUR_API_KEY";

// Your JSON data for the request body
const data = {
    // Copy paste the data from the website directly without any modification to train the scraper
    // or Write a short description of your required data, for example: "clinical trials results"
    "look_for": `
    NCT06939504
    Not yet recruiting
    New
    A Trial of HRS-9813 Capsule and Tablet in Healthy Subjects
    Conditions
    Pulmonary Fibrosis
    Locations
    Shanghai, Shanghai, China


    NCT06939491
    Recruiting
    New
    Comparison of Ultrasound-guided Electrolysis Therapy vs. Sham Electrolysis in Patients With Patellar Tendinopathy: A Prospective Randomized Study Including MRI and Shear-wave Ultrasound Elastography Imaging
    Conditions
    Patellar Tendinopathy / Jumpers Knee
    Locations
    Bremen, Germany


    NCT06939478
    Not yet recruiting
    New
    AI Powered Mapping Technology for Identifying Arrhythmias
    Conditions
    Arrhythmias, Cardiac
    Locations
    Location not provided


    NCT06939465
    Recruiting
    New
    Esophageal Visceral Hypersensitivity and Hypervigilance in Disorders of Gut-brain Interaction: the Roles of Cognitive-behavioral Therapy
    Conditions
    GERD Without Erosive Esophagitis
    Gut-Brain Disorders
    Locations
    Hualien, Taiwan`,
  urls: ["https://clinicaltrials.gov/search?page=1"],
  mode: "list",
};

const headers = {
  "Content-Type": "application/json",
  "api-key": api_key,
};

console.log("Creating scraper.. This may take up to 2 minutes");

// Make the POST request
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

    // Save the scraper.json
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
