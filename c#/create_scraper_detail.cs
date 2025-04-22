using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        string url = "https://api.minexa.ai/scraper/";
        string apiKey = "YOUR_API_KEY";

        // Your JSON data for the request body
        string jsonBody = @"
        {
            // Copy paste the data from the website directly without any modification to train the scraper
            // or Write a short description of your required data, for example: ""clinical trials study overview""
            ""look_for"": """"Study Overview
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
            2024PI059
            """",
            ""urls"": [
                ""https://clinicaltrials.gov/study/NCT06382792"",
                ""https://clinicaltrials.gov/study/NCT06382779"",
                ""https://clinicaltrials.gov/study/NCT06382753"",
                ""https://clinicaltrials.gov/study/NCT06382727""
            ],
            ""mode"": ""detail""
        }";

        Console.WriteLine("Creating scraper.. This may take up to 2 minutes");

        HttpClient client = new HttpClient();
        client.DefaultRequestHeaders.Add("api-key", apiKey);
        StringContent content = new StringContent(jsonBody, Encoding.UTF8, "application/json");

        HttpResponseMessage response = await client.PostAsync(url, content);

        if (response.IsSuccessStatusCode)
        {
            string responseContent = await response.Content.ReadAsStringAsync();
            Console.WriteLine("Please confirm container is well located: " + responseContent);

            // Create and save the file
            dynamic jsonResponse = Newtonsoft.Json.JsonConvert.DeserializeObject(responseContent);
            string scraperId = jsonResponse.response.id;
            string filePath = Path.Combine(Directory.GetCurrentDirectory(), $"scraper_id_{scraperId}.json");

            // Save the scraper.json
            using (StreamWriter file = File.CreateText(filePath))
            {
                Newtonsoft.Json.JsonSerializer serializer = new Newtonsoft.Json.JsonSerializer();
                serializer.Serialize(file, jsonResponse);
            }
            Console.WriteLine("Full scraper json saved at: " + filePath);
        }
        else
        {
            Console.WriteLine("Error status code " + response.StatusCode + " occurred ");
            string responseContent = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseContent);
        }
    }
}
