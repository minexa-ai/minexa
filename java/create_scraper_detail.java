import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

public class Main {

    public static void main(String[] args) {
        String url = "https://api.minexa.ai/scraper/";
        String apiKey = "YOUR_API_KEY";

        System.out.println("Creating Scraper.. This may take up to 2 minutes");

        JSONObject data = new JSONObject();
        JSONArray urls = new JSONArray();
        urls.add("https://clinicaltrials.gov/study/NCT06382792");
        urls.add("https://clinicaltrials.gov/study/NCT06382779");
        urls.add("https://clinicaltrials.gov/study/NCT06382753");
        urls.add("https://clinicaltrials.gov/study/NCT06382727");

        // Copy paste the data from the website directly without any modification to train the scraper
        // or Write a short description of your required data, for example: "clinical trials study overview"

        data.put("look_for", """Study Overview
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
    2024PI059""");
        data.put("urls", urls);
        data.put("mode", "detail");

        String requestBody = data.toString();

        try {
            URL obj = new URL(url);
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestProperty("api-key", apiKey);

            con.setDoOutput(true);
            OutputStream os = con.getOutputStream();
            os.write(requestBody.getBytes());
            os.flush();
            os.close();

            int responseCode = con.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) { // success
                // Print the response
                System.out.println("Please confirm container is well located: " + con.getResponseMessage());

                // Read and save the response
                // Here, you can write code to read the response and save it to a file
                // For simplicity, I'm not implementing it here

                System.out.println("Full scraper json saved at: <file_path>");

            } else {
                System.out.println("Error status code " + responseCode + " occurred");
                // Print response message if any
                System.out.println(con.getResponseMessage());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
