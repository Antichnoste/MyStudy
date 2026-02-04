using System.Collections.Generic;

namespace Parser.Models
{
    public class MovieCredits
    {
        public int MovieId { get; set; }
        public string Title { get; set; }
        public List<CastMember> Cast { get; set; } = new List<CastMember>();
        public List<CrewMember> Crew { get; set; } = new List<CrewMember>();
    }
}