using System.Collections.Generic;
using System.Linq;

namespace Parser.Models
{
    public record DirectorTeamStats(string DirectorName, double AvgCastSize, double AvgCrewSize);

    public record UniversalCareer(string Name, string MostFrequentDepartment, int Count);

    public record DepartmentCastCorrelation(string Department, double AvgCastSize);

    public static class MovieAnalyzer
    {
        // 1. Найти все фильмы, снятые режиссером "Steven Spielberg".
        public static List<string> FindFilmsByDirector(List<MovieCredits> movies, string directorName)
        {
            return movies
                .Where(m => m.Crew.Any(c => c.Job == "Director" && c.Name == directorName))
                .Select(m => m.Title)
                .ToList();
        }

        // 2. Получить список всех персонажей, которых сыграл актер "Tom Hanks".
        public static List<string> FindCharactersByActor(List<MovieCredits> movies, string actorName)
        {
            return movies
                .SelectMany(m => m.Cast)
                .Where(c => c.Name == actorName)
                .Select(c => c.Character)
                .Distinct()
                .ToList();
        }

        // 3. Найти 5 фильмов с самым большим количеством актеров в составе.
        public static List<string> FindTop5FilmsByCastSize(List<MovieCredits> movies)
        {
            return movies
                .OrderByDescending(m => m.Cast.Count)
                .Take(5)
                .Select(m => $"{m.Title} ({m.Cast.Count} актеров)")
                .ToList();
        }

        // 4. Найти топ-10 самых востребованных актеров (по количеству фильмов).
        public static List<(string ActorName, int MovieCount)> FindTop10BusiestActors(List<MovieCredits> movies)
        {
            return movies
                .SelectMany(m => m.Cast)
                .GroupBy(c => c.Name)
                .Select(g => (ActorName: g.Key, MovieCount: g.Count()))
                .OrderByDescending(x => x.MovieCount)
                .Take(10)
                .ToList();
        }

        // 5. Получить список всех уникальных департаментов (department) съемочной группы.
        public static List<string> FindUniqueDepartments(List<MovieCredits> movies)
        {
            return movies
                .SelectMany(m => m.Crew)
                .Select(c => c.Department)
                .Distinct()
                .OrderBy(d => d)
                .ToList();
        }

        // 6. Найти все фильмы, где "Hans Zimmer" был композитором (Original Music Composer).
        public static List<string> FindFilmsByComposer(List<MovieCredits> movies, string composerName)
        {
            return movies
                .Where(m => m.Crew.Any(c => c.Job == "Original Music Composer" && c.Name == composerName))
                .Select(m => m.Title)
                .ToList();
        }

        // 7. Создать словарь, где ключ — ID фильма, а значение — имя режиссера.
        public static Dictionary<int, string> GetMovieDirectorMap(List<MovieCredits> movies)
        {
            return movies
                .ToDictionary(
                    m => m.MovieId,
                    m => m.Crew.FirstOrDefault(c => c.Job == "Director")?.Name ?? "Неизвестен"
                );
        }
        
        // 8. Найти фильмы, где в актерском составе есть и "Brad Pitt", и "George Clooney".
        public static List<string> FindFilmsWithDuo(List<MovieCredits> movies, string actor1, string actor2)
        {
            return movies
                .Where(m => m.Cast.Any(c => c.Name == actor1) && m.Cast.Any(c => c.Name == actor2))
                .Select(m => m.Title)
                .ToList();
        }
        
        // 9. Посчитать, сколько всего человек работает в департаменте "Camera" по всем фильмам.
        public static int CountUniquePeopleInDepartment(List<MovieCredits> movies, string departmentName)
        {
            return movies
                .SelectMany(m => m.Crew)
                .Where(c => c.Department == departmentName)
                .GroupBy(c => c.Id) 
                .Count();
        }
        
        // 10. Найти всех людей, которые в фильме "Titanic" были одновременно и в съемочной группе, и в списке актеров.
        public static List<string> FindCrossoverPeopleInMovie(List<MovieCredits> movies, string movieTitle)
        {
            var movie = movies.FirstOrDefault(m => m.Title == movieTitle);
            
            if (movie == null) return new List<string>();

            var castIds = movie.Cast.Select(c => c.Id).ToHashSet();

            return movie.Crew
                .Where(c => castIds.Contains(c.Id))
                .Select(c => c.Name)
                .Distinct()
                .ToList();
        }
        
        // 11. Найти "внутренний круг" режиссера.
        public static List<(string CrewName, int FilmsTogether)> FindDirectorsInnerCircle(List<MovieCredits> movies, string directorName, int topN = 5)
        {
            var directorFilms = movies
                .Where(m => m.Crew.Any(c => c.Job == "Director" && c.Name == directorName))
                .ToList();

            return directorFilms
                .SelectMany(m => m.Crew)
                .Where(c => c.Job != "Director" && c.Name != directorName)
                .GroupBy(c => c.Name)
                .Select(g => (CrewName: g.Key, FilmsTogether: g.Count()))
                .OrderByDescending(x => x.FilmsTogether)
                .Take(topN)
                .ToList();
        }

        // 12. Определить экранные "дуэты".
        public static List<(string Actor1, string Actor2, int FilmsTogether)> FindTopDuos(List<MovieCredits> movies, int topN = 10)
        {
            var duos = movies
                .SelectMany(m =>
                {
                    var actors = m.Cast.Select(c => c.Name).Distinct().OrderBy(n => n).ToList();
                    var filmDuos = new List<(string Actor1, string Actor2)>();

                    for (int i = 0; i < actors.Count; i++)
                    {
                        for (int j = i + 1; j < actors.Count; j++)
                        {
                            filmDuos.Add((actors[i], actors[j]));
                        }
                    }
                    return filmDuos;
                })
                .GroupBy(duo => duo)
                .Select(g => (g.Key.Actor1, g.Key.Actor2, FilmsTogether: g.Count()))
                .OrderByDescending(x => x.FilmsTogether)
                .Take(topN)
                .ToList();
            
            return duos;
        }

        // 13. Вычислить "индекс разнообразия" для карьеры.
        public static List<(string CrewName, int DepartmentCount)> FindTopVersatileCrew(List<MovieCredits> movies, int topN = 5)
        {
            return movies
                .SelectMany(m => m.Crew)
                .GroupBy(c => c.Name)
                .Select(g => 
                (
                    CrewName: g.Key, 
                    DepartmentCount: g.Select(c => c.Department).Distinct().Count()
                ))
                .OrderByDescending(x => x.DepartmentCount)
                .Take(topN)
                .ToList();
        }

        // 14. Найти "творческие трио".
        public static List<(string MovieTitle, string UniversalPerson)> FindCreativeTrios(List<MovieCredits> movies)
        {
            var trios = new List<(string MovieTitle, string UniversalPerson)>();

            foreach (var movie in movies)
            {
                var people = movie.Crew.GroupBy(c => c.Id);

                foreach (var personGroup in people)
                {
                    // Проверяем, есть ли у человека все три роли
                    bool isDirector = personGroup.Any(c => c.Job == "Director");
                    bool isWriter = personGroup.Any(c => c.Job.Contains("Writer")); 
                    bool isProducer = personGroup.Any(c => c.Job.Contains("Producer"));

                    if (isDirector && isWriter && isProducer)
                    {
                        trios.Add((movie.Title, personGroup.First().Name));
                        break; 
                    }
                }
            }
            return trios;
        }

        // 15. Два шага до Кевина Бейкона.
        public static List<string> FindTwoStepsToKevinBacon(List<MovieCredits> movies, string targetActor = "Kevin Bacon")
        {
            var filmsWithTarget = movies
                .Where(m => m.Cast.Any(c => c.Name == targetActor))
                .ToList();
            
            var actorsStep1 = filmsWithTarget
                .SelectMany(m => m.Cast)
                .Where(c => c.Name != targetActor)
                .Select(c => c.Name)
                .ToHashSet();

            var filmsWithStep1Actors = movies
                .Where(m => m.Cast.Any(c => actorsStep1.Contains(c.Name)))
                .ToList();

            var actorsStep2 = filmsWithStep1Actors
                .SelectMany(m => m.Cast)
                .Select(c => c.Name)
                .Distinct()
                .Where(name => name != targetActor && !actorsStep1.Contains(name))
                .ToList();

            return actorsStep2;
        }

        // 16. Проанализировать "командную работу".
        public static List<DirectorTeamStats> AnalyzeTeamwork(List<MovieCredits> movies)
        {
            return movies
                .SelectMany(m => m.Crew.Where(c => c.Job == "Director").Select(d => (DirectorName: d.Name, Movie: m)))
                .GroupBy(x => x.DirectorName)
                .Select(g => new DirectorTeamStats(
                    DirectorName: g.Key,
                    AvgCastSize: g.Average(x => x.Movie.Cast.Count),
                    AvgCrewSize: g.Average(x => x.Movie.Crew.Count)
                ))
                .OrderByDescending(s => s.AvgCastSize + s.AvgCrewSize)
                .ToList();
        }

        // 17. Определить карьерный путь "универсалов".
        public static List<UniversalCareer> FindCareerPath(List<MovieCredits> movies)
        {
            var allCastIds = movies.SelectMany(m => m.Cast).Select(c => c.Id).ToHashSet();
            var allCrewIds = movies.SelectMany(m => m.Crew).Select(c => c.Id).ToHashSet();
            
            var crossoverIds = allCastIds.Intersect(allCrewIds);

            var allCrewRecords = movies
                .SelectMany(m => m.Crew)
                .Where(c => crossoverIds.Contains(c.Id))
                .ToList();
            
            return allCrewRecords
                .GroupBy(c => c.Id)
                .Select(personGroup =>
                {
                    var topDepartment = personGroup
                        .GroupBy(c => c.Department)
                        .Select(d => new { Department = d.Key, Count = d.Count() })
                        .OrderByDescending(x => x.Count)
                        .FirstOrDefault();

                    return new UniversalCareer(
                        Name: personGroup.First().Name,
                        MostFrequentDepartment: topDepartment?.Department ?? "N/A",
                        Count: topDepartment?.Count ?? 0
                    );
                })
                .OrderByDescending(u => u.Count)
                .ToList();
        }

        // 18. Найти пересечение "элитных клубов".
        public static List<string> FindEliteIntersection(List<MovieCredits> movies, string director1, string director2)
        {
            var getCrewIds = (string dName) => movies
                .Where(m => m.Crew.Any(c => c.Job == "Director" && c.Name == dName))
                .SelectMany(m => m.Crew.Select(c => c.Id))
                .ToHashSet();

            var ids1 = getCrewIds(director1);
            var ids2 = getCrewIds(director2);

            var intersectionIds = ids1.Intersect(ids2).ToHashSet();
            
            return movies
                .SelectMany(m => m.Crew)
                .Where(c => intersectionIds.Contains(c.Id))
                .Select(c => c.Name)
                .Distinct()
                .OrderBy(n => n)
                .ToList();
        }

        // 19. Выявить "скрытое влияние".
        public static List<DepartmentCastCorrelation> AnalyzeDepartmentInfluence(List<MovieCredits> movies)
        {
            return movies
                .SelectMany(m => m.Crew.Select(c => (Department: c.Department, CastCount: m.Cast.Count)))
                .GroupBy(x => x.Department)
                .Select(g => new DepartmentCastCorrelation(
                    Department: g.Key,
                    AvgCastSize: g.Average(x => x.CastCount)
                ))
                .OrderByDescending(d => d.AvgCastSize)
                .ToList();
        }

        // 20. Проанализировать "архетипы" персонажей.
        public static List<(string Archetype, int Count)> AnalyzeActorArchetypes(List<MovieCredits> movies, string actorName)
        {
            return movies
                .SelectMany(m => m.Cast)
                .Where(c => c.Name == actorName)
                .Select(c => c.Character.Split(' ', 2)[0].Trim())
                .Where(word => !string.IsNullOrEmpty(word))
                .GroupBy(archetype => archetype)
                .Select(g => (Archetype: g.Key, Count: g.Count()))
                .OrderByDescending(x => x.Count)
                .ToList();
        }
    }
}