using CsvHelper.Configuration;

namespace Parser.Models
{
    public class MovieCreditsDto
    {
        public int Movie_Id { get; set; } 

        public string Title { get; set; }
        
        public string Cast { get; set; } 
        
        public string Crew { get; set; } 
    }

    public sealed class MovieCreditsDtoMap : ClassMap<MovieCreditsDto>
    {
        public MovieCreditsDtoMap()
        {
            Map(m => m.Movie_Id).Name("movie_id");
            Map(m => m.Title).Name("title");
            Map(m => m.Cast).Name("cast");
            Map(m => m.Crew).Name("crew");
        }
    }
}