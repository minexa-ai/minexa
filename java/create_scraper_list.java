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
        urls.add("https://clinicaltrials.gov/search?page=1");

        // Copy paste the data from the website directly without any modification to train the scraper
        // or Write a short description of your required data, for example: "clinical trials results"
        data.put("look_for", """
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
        Hualien, Taiwan""");
        data.put("urls", urls);
        data.put("mode", "list");

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
