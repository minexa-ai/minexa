<?php
$url = "https://api.minexa.ai/scraper/";
$api_key = "YOUR_API_KEY";

// Your JSON data for the request body
$data = array(

    // Copy paste the data from the website directly without any modification to train the scraper
    // or Write a short description of your required data, for example: "clinical trials study overview"
    "look_for" => <<<EOD
    Study Overview
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
    2024PI059,
    EOD,
    // Provide 4 urls corresponding to a similarly structured page but with different data
    "urls" => array(
        "https://clinicaltrials.gov/study/NCT06382792",
        "https://clinicaltrials.gov/study/NCT06382779",
        "https://clinicaltrials.gov/study/NCT06382753",
        "https://clinicaltrials.gov/study/NCT06382727"
    ),

    // uncomment if you need to recrawl the HTML again from scratch by ignoring cached data (like its the first time you scrape it)
    //"reset" => true,

    // Unocomment and set it when manaully detecting your container after first try
    // No need to use for creating scraper for a particular page for the first time
    // "xpath" => "/html/body/div/div/div[3]/div[1]/div[2]",

    // if you want to extract detail data, we advise not to use a simple domain name but try to find pages that are different
    // Use detail if the data is mixed and in a less structured format.
    "mode" => "detail",
);

$headers = array(
    "Content-Type: application/json",
    "api-key: $api_key"
);

echo "Creating scraper.. This may take up to 2 minutes"

// Make the POST request
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
$response = curl_exec($ch);
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

// Print the response
if ($status_code == 200) {
    $response_data = json_decode($response, true);
    echo "Please confirm container is well located: " . $response_data['response']['web_app'] . "\n";

    // Create and save the file
    $scraper_id = $response_data["response"]["id"];
    $file_path = dirname(__FILE__) . "/scraper_id_" . $scraper_id . ".json";

    // Save the scraper.json
    file_put_contents($file_path, json_encode($response_data, JSON_PRETTY_PRINT));
    echo "Full scraper json saved at: $file_path\n";
} else {
    echo "Error status code $status_code occurred \n";
    try {
        $error_data = json_decode($response, true);
        echo json_encode($error_data, JSON_PRETTY_PRINT) . "\n";
    } catch (Exception $e) {
        echo $e->getMessage() . " in showing error\n";
    }
}
?>
