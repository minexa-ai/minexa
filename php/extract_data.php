<?php

$url = "https://api.minexa.ai/data/";
$apiKey = 'YOUR_API_KEY';  // free key.

// Your JSON data for the request body
$outputFormat = "json"; // json/csv

$data = [
    "batches" => [
        [
            "robot_id" => 103,
            "columns" => [
                "col_1",
                "col_3"
            ],
            "urls" => [
                "https://clinicaltrials.gov/search"
            ]
        ]
    ]
];

$headers = [
    "Content-Type: application/json",
    "api-key: $apiKey"
];

$nextSet = null;
$started = 0;
$iteratedData = [];
$extractedData = [];

$formattedDatetime = date("Y_m_d_H_i");

while ($nextSet || $started == 0) {
    // Send a POST request with headers
    $data['next'] = $nextSet;
    $options = [
        "http" => [
            "method" => "POST",
            "header" => implode("\r\n", $headers),
            "content" => json_encode($data)
        ]
    ];
    $context = stream_context_create($options);
    $response = file_get_contents($url, false, $context);

    // Check if the request was successful (status code 2xx)
    if ($response) {
        $jsonContent = json_decode($response, true);

        foreach ($jsonContent["response"] as $extractions) {
            foreach ($extractions["results"] as $rows) {
                if (isset($rows["error"]) && $rows["error"]) {
                    continue;
                }
                $row = [];
                foreach ($rows as $col => $value) {
                    if (is_string($value)) {
                        $row[$col] = $value;
                    } elseif (is_array($value)) {
                        $row[$col] = array_column($value, "value");
                    }
                }
                $iteratedData[] = $row;
            }
        }

        $extractedData = array_merge($extractedData, $jsonContent["response"]);
        try {
            // Create and save the file
            $filePath = dirname(__FILE__) . "/exctraction_$formattedDatetime";

            // Saving in json format
            file_put_contents("$filePath.json", json_encode($extractedData, JSON_PRETTY_PRINT));

            // Saving in csv format
            $fp = fopen("$filePath.csv", 'w');
            fputcsv($fp, array_keys($iteratedData[0]));
            foreach ($iteratedData as $row) {
                fputcsv($fp, $row);
            }
            fclose($fp);

            // Saving in Excel format (if PHPExcel library is installed)
            // require_once 'PHPExcel/Classes/PHPExcel.php';
            // $excel = new PHPExcel();
            // $excel->getActiveSheet()->fromArray($iteratedData, null, 'A1');
            // $writer = PHPExcel_IOFactory::createWriter($excel, 'Excel2007');
            // $writer->save("$filePath.xlsx");

            echo "res nbr " . count($jsonContent['response']) . PHP_EOL;
            if (isset($jsonContent['meta']['next'])) {
                $nextSet = $jsonContent['meta']['next'];
                echo "run " . $nextSet . PHP_EOL;
                $started += 1;
            } else {
                echo "finished" . PHP_EOL;
                break;
            }
        } catch (Exception $e) {
            echo "Error: " . $e->getMessage() . PHP_EOL;
        }
    } else {
        // Handle the case where the request was not successful
        echo "Request failed" . PHP_EOL;
    }
}
?>
