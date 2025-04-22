using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Data;
using System.Linq;

class Program
{
    static async Task Main(string[] args)
    {
        string url = "https://api.minexa.ai/data/";
        string apiKey = "YOUR_API_KEY";
        string outputFormat = "json"; // json/csv

        // Your JSON data for the request body
        JObject data = JObject.FromObject(new
        {
            batches = new[]
            {
                new
                {
                    scraper_id = 103,
                    columns = new[] { "col_1", "col_3" },
                    urls = new[] { "https://clinicaltrials.gov/search" }
                }
            }
        });

        HttpClient client = new HttpClient();
        client.DefaultRequestHeaders.Add("api-key", apiKey);

        string nextSet = null;
        int started = 0;
        List<JObject> extractedData = new List<JObject>();
        List<Dictionary<string, object>> iteratedData = new List<Dictionary<string, object>>();

        string formattedDateTime = DateTime.Now.ToString("yyyy_MM_dd_HH_mm");

        while (nextSet != null || started == 0)
        {
            // Send a POST request with headers
            data["next"] = nextSet;
            var content = new StringContent(data.ToString(), Encoding.UTF8, "application/json");
            HttpResponseMessage response = await client.PostAsync(url, content);

            // Check if the request was successful (status code 2xx)
            if (response.IsSuccessStatusCode)
            {
                string responseContent = await response.Content.ReadAsStringAsync();
                JObject jsonContent = JObject.Parse(responseContent);

                foreach (JObject extraction in jsonContent["response"])
                {
                    foreach (JObject row in extraction["results"])
                    {
                        if (row["error"] != null)
                            continue;

                        Dictionary<string, object> rowData = new Dictionary<string, object>();
                        foreach (var item in row)
                        {
                            if (item.Value.Type == JTokenType.String)
                                rowData[item.Key] = item.Value.ToString();
                            else if (item.Value.Type == JTokenType.Array)
                                rowData[item.Key] = item.Value.Select(x => x["value"].ToString()).ToList();
                        }
                        iteratedData.Add(rowData);
                    }
                }

                extractedData.AddRange(jsonContent["response"].ToObject<List<JObject>>());
                try
                {
                    string filePath = Path.Combine(Directory.GetCurrentDirectory(), $"exctraction_{formattedDateTime}");

                    // Saving in json format
                    File.WriteAllText($"{filePath}.json", JsonConvert.SerializeObject(extractedData, Formatting.Indented));

                    DataTable dt = ToDataTable(iteratedData);
                    Console.WriteLine(dt.Rows.Count + " rows retrieved.");

                    // Saving the csv
                    SaveDataTableToCSV(dt, $"{filePath}.csv");

                    // Saving the Excel file
                    SaveDataTableToExcel(dt, $"{filePath}.xlsx");

                }
                catch (JsonReaderException)
                {
                    Console.WriteLine(responseContent);
                }

                Console.WriteLine($"res nbr {jsonContent["response"].Count()}");
                if (jsonContent["meta"]["next"] != null)
                {
                    nextSet = jsonContent["meta"]["next"].ToString();
                    Console.WriteLine("run " + nextSet);
                    started++;
                }
                else
                {
                    Console.WriteLine("finished");
                    break;
                }
            }
            else
            {
                // Handle the case where the request was not successful
                Console.WriteLine($"Request failed with status code: {response.StatusCode}");
                Console.WriteLine(await response.Content.ReadAsStringAsync());
            }
        }
    }

    static DataTable ToDataTable(List<Dictionary<string, object>> list)
    {
        DataTable table = new DataTable();
        foreach (var pair in list.First())
        {
            table.Columns.Add(pair.Key, typeof(string));
        }
        foreach (Dictionary<string, object> dict in list)
        {
            DataRow row = table.NewRow();
            foreach (var pair in dict)
            {
                row[pair.Key] = pair.Value;
            }
            table.Rows.Add(row);
        }
        return table;
    }

    static void SaveDataTableToCSV(DataTable dt, string filePath)
    {
        StringBuilder sb = new StringBuilder();
        IEnumerable<string> columnNames = dt.Columns.Cast<DataColumn>().Select(column => column.ColumnName);
        sb.AppendLine(string.Join(",", columnNames));

        foreach (DataRow row in dt.Rows)
        {
            IEnumerable<string> fields = row.ItemArray.Select(field => field.ToString());
            sb.AppendLine(string.Join(",", fields));
        }

        File.WriteAllText(filePath, sb.ToString());
    }

    static void SaveDataTableToExcel(DataTable dt, string filePath)
    {
        using (var excel = new OfficeOpenXml.ExcelPackage())
        {
            var ws = excel.Workbook.Worksheets.Add("Sheet1");

            for (int i = 0; i < dt.Columns.Count; i++)
            {
                ws.Cells[1, i + 1].Value = dt.Columns[i].ColumnName;
            }

            for (int i = 0; i < dt.Rows.Count; i++)
            {
                for (int j = 0; j < dt.Columns.Count; j++)
                {
                    ws.Cells[i + 2, j + 1].Value = dt.Rows[i][j];
                }
            }

            FileInfo excelFile = new FileInfo(filePath);
            excel.SaveAs(excelFile);
        }
    }
}
