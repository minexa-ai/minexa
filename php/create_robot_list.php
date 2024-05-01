<?php
$url = "https://api.minexa.ai/robot/";
$api_key = "JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP";

// Your JSON data for the request body
$data = array(

    // what part of the page you want to extract - free form - write a descriptive text so that we can better locate the right part of the page
    "look_for" => "Features",

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
    // No need to use for creating robot for a particular page for the first time
    // "xpath" => "/html/body/div/div/div[3]/div[1]/div[2]",

    // if you want to extract detail data, we advise not to use a simple domain name but try to find pages that are different
    // Use detail if the data is mixed and in a less structured format.
    "mode" => "detail",
);

$headers = array(
    "Content-Type: application/json",
    "api-key: $api_key"
);

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
    $robot_id = $response_data["response"]["id"];
    $file_path = dirname(__FILE__) . "/robot_id_" . $robot_id . ".json";

    // Save the robot.json
    file_put_contents($file_path, json_encode($response_data, JSON_PRETTY_PRINT));
    echo "Full robot json saved at: $file_path\n";
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
