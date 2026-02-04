using System.Text.Json.Serialization;

namespace Parser.Models
{
    /// <summary>
    /// Представляет одного участника актерского состава.
    /// </summary>
    public class CastMember
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }

        [JsonPropertyName("name")]
        public string Name { get; set; }

        [JsonPropertyName("character")]
        public string Character { get; set; }

        [JsonPropertyName("gender")]
        public int Gender { get; set; } 

        [JsonPropertyName("order")]
        public int Order { get; set; }

        [JsonPropertyName("cast_id")]
        public int CastId { get; set; }

        [JsonPropertyName("credit_id")]
        public string CreditId { get; set; }
    }
}