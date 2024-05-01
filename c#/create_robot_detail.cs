using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        string url = "https://api.minexa.ai/robot/";
        string apiKey = "JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP";

        // Your JSON data for the request body
        string jsonBody = @"
        {
            ""look_for"": ""Features"",
            ""urls"": [
                ""https://clinicaltrials.gov/study/NCT06382792"",
                ""https://clinicaltrials.gov/study/NCT06382779"",
                ""https://clinicaltrials.gov/study/NCT06382753"",
                ""https://clinicaltrials.gov/study/NCT06382727""
            ],
            ""mode"": ""detail""
        }";

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
            string robotId = jsonResponse.response.id;
            string filePath = Path.Combine(Directory.GetCurrentDirectory(), $"robot_id_{robotId}.json");

            // Save the robot.json
            using (StreamWriter file = File.CreateText(filePath))
            {
                Newtonsoft.Json.JsonSerializer serializer = new Newtonsoft.Json.JsonSerializer();
                serializer.Serialize(file, jsonResponse);
            }
            Console.WriteLine("Full robot json saved at: " + filePath);
        }
        else
        {
            Console.WriteLine("Error status code " + response.StatusCode + " occurred ");
            string responseContent = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseContent);
        }
    }
}
