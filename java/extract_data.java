import org.json.JSONArray;
import org.json.JSONObject;

import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        String url = "https://api.minexa.ai/data/";
        String apiKey = "JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP";
        String outputFormat = "json"; // or "csv"

        // Your JSON data for the request body
        JSONObject data = new JSONObject();
        JSONArray batches = new JSONArray();

        JSONObject batch = new JSONObject();
        batch.put("robot_id", 103);

        JSONArray columns = new JSONArray();
        columns.put("col_1");
        columns.put("col_3");
        batch.put("columns", columns);

        JSONArray urls = new JSONArray();
        urls.put("https://www.britannica.com/topic/list-of-herbs-and-spices-2024392");
        batch.put("urls", urls);

        batches.put(batch);
        data.put("batches", batches);

        JSONObject headers = new JSONObject();
        headers.put("Content-Type", "application/json");
        headers.put("api-key", apiKey);

        String nextSet = null;
        int started = 0;
        List<JSONObject> iteratedData = new ArrayList<>();
        List<JSONObject> extractedData = new ArrayList<>();

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy_MM_dd_HH_mm");
        LocalDateTime now = LocalDateTime.now();
        String formattedDateTime = now.format(formatter);

        while (nextSet != null || started == 0) {
            try {
                // Send a POST request with headers
                data.put("next", nextSet);
                URL obj = new URL(url);
                HttpURLConnection con = (HttpURLConnection) obj.openConnection();
                con.setRequestMethod("POST");
                con.setRequestProperty("Content-Type", "application/json");
                con.setRequestProperty("api-key", apiKey);

                con.setDoOutput(true);
                OutputStream os = con.getOutputStream();
                os.write(data.toString().getBytes());
                os.flush();
                os.close();

                int responseCode = con.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_OK) { // success
                    // Read and process the response
                    JSONObject jsonResponse = new JSONObject(new String(con.getInputStream().readAllBytes()));
                    JSONArray responseArray = jsonResponse.getJSONArray("response");

                    for (int i = 0; i < responseArray.length(); i++) {
                        JSONObject extraction = responseArray.getJSONObject(i);
                        JSONArray results = extraction.getJSONArray("results");

                        for (int j = 0; j < results.length(); j++) {
                            JSONObject row = results.getJSONObject(j);
                            if (!row.has("error")) {
                                JSONObject newRow = new JSONObject();
                                row.keySet().forEach(col -> newRow.put(col, row.get(col)));
                                iteratedData.add(newRow);
                            }
                        }
                        extractedData.add(extraction);
                    }

                    // Create and save the file
                    String filePath = "extraction_" + formattedDateTime;
                    FileWriter fileWriter = new FileWriter(filePath + ".json");
                    fileWriter.write(extractedData.toString());
                    fileWriter.close();

                    // Convert iteratedData to DataFrame and save as CSV or Excel
                    // This part is dependent on the specific DataFrame library being used in Java

                    // Print number of responses
                    System.out.println("Number of responses: " + responseArray.length());

                    if (jsonResponse.getJSONObject("meta").has("next")) {
                        nextSet = jsonResponse.getJSONObject("meta").getString("next");
                        System.out.println("Run " + nextSet);
                        started++;
                    } else {
                        System.out.println("Finished");
                        break;
                    }

                } else {
                    // Handle the case where the request was not successful
                    System.out.println("Request failed with status code: " + responseCode);
                    System.out.println(con.getResponseMessage());
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
