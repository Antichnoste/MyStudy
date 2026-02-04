using CsvHelper;
using CsvHelper.Configuration;
using System.Globalization;
using System.Text.Json;
using System.IO;
using System.Collections.Generic;
using System.Linq;

namespace Parser.Models
{
    public static class TmdbCreditsParser
    {
        public static List<MovieCredits> ParseFile(string filePath)
        {
            var config = new CsvConfiguration(CultureInfo.InvariantCulture)
            {
                HasHeaderRecord = true,
                Delimiter = ",",
            };

            var parsedCredits = new List<MovieCredits>();

            using (var reader = File.OpenText(filePath))
            using (var csv = new CsvReader(reader, config))
            {
                csv.Context.RegisterClassMap<MovieCreditsDtoMap>();
                
                var records = csv.GetRecords<MovieCreditsDto>().ToList();

                var jsonOptions = new JsonSerializerOptions 
                {
                    PropertyNameCaseInsensitive = true 
                };

                foreach (var dto in records)
                {
                    var credits = new MovieCredits
                    {
                        MovieId = dto.Movie_Id,
                        Title = dto.Title
                    };

                    if (!string.IsNullOrWhiteSpace(dto.Cast))
                    {
                        try
                        {
                            credits.Cast = JsonSerializer.Deserialize<List<CastMember>>(dto.Cast, jsonOptions) ?? new List<CastMember>();
                        }
                        catch (JsonException ex)
                        {
                            System.Console.WriteLine($"Ошибка десериализации Cast для фильма '{dto.Title}' (ID {dto.Movie_Id}): {ex.Message}");
                        }
                    }
                    
                    if (!string.IsNullOrWhiteSpace(dto.Crew))
                    {
                        try
                        {
                            credits.Crew = JsonSerializer.Deserialize<List<CrewMember>>(dto.Crew, jsonOptions) ?? new List<CrewMember>();
                        }
                        catch (JsonException ex)
                        {
                            System.Console.WriteLine($"Ошибка десериализации Crew для фильма '{dto.Title}' (ID {dto.Movie_Id}): {ex.Message}");
                        }
                    }

                    parsedCredits.Add(credits);
                }
            }
            
            return parsedCredits;
        }
    }
}