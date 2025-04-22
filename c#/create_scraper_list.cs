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
    // or Write a short description of your required data, for example: ""clinical trials results""

    ""look_for"": """"
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
    Hualien, Taiwan
    """",
        ""urls"": [""https://clinicaltrials.gov/search?page=1""],
        ""mode"": ""list""
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
