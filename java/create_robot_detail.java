import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

public class Main {

    public static void main(String[] args) {
        String url = "https://api.minexa.ai/robot/";
        String apiKey = "YOUR_API_KEY";

        System.out.println("Creating Robot.. This may take up to 2 minutes");

        JSONObject data = new JSONObject();
        JSONArray urls = new JSONArray();
        urls.add("https://clinicaltrials.gov/study/NCT06382792");
        urls.add("https://clinicaltrials.gov/study/NCT06382779");
        urls.add("https://clinicaltrials.gov/study/NCT06382753");
        urls.add("https://clinicaltrials.gov/study/NCT06382727");
        data.put("look_for", "Features");
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

                System.out.println("Full robot json saved at: <file_path>");

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
