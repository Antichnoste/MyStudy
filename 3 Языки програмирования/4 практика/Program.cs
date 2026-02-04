using Parser.Models;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Text;
using System.Globalization;

class Program
{
    private const string RESULTS_DIR = "results";

    static void Main(string[] args)
    {
        string fileName = "tmdb_5000_credits.csv";
        string filePath = Path.Combine(Directory.GetCurrentDirectory(), fileName);

        List<MovieCredits> movies = TmdbCreditsParser.ParseFile(filePath); // тут происхрдит сам парсинг, дальше только обработка задач
        
        // Создание каталога results
        Directory.CreateDirectory(RESULTS_DIR);

        var analysisTasks = new List<(string Title, string FileName, Func<string> Action)>
        {
            ("Найти все фильмы, снятые режиссером 'Steven Spielberg'.", "1_Spielberg_Films.txt", 
                () => FormatResults(MovieAnalyzer.FindFilmsByDirector(movies, "Steven Spielberg"))),

            ("Получить список всех персонажей, которых сыграл актер 'Tom Hanks'.", "2_TomHanks_Characters.txt",
                () => FormatResults(MovieAnalyzer.FindCharactersByActor(movies, "Tom Hanks"))),

            ("Найти 5 фильмов с самым большим количеством актеров в составе.", "3_Top5_CastSize.txt",
                () => FormatResults(MovieAnalyzer.FindTop5FilmsByCastSize(movies))),

            ("Найти топ-10 самых востребованных актеров (по количеству фильмов).", "4_Top10_BusiestActors.txt",
                () => FormatResults(MovieAnalyzer.FindTop10BusiestActors(movies), item => $"{item.ActorName}: {item.MovieCount} фильмов")),

            ("Получить список всех уникальных департаментов (department) съемочной группы.", "5_Unique_Departments.txt",
                () => FormatResults(MovieAnalyzer.FindUniqueDepartments(movies))),

            ("Найти все фильмы, где 'Hans Zimmer' был композитором (Original Music Composer).", "6_HansZimmer_Films.txt",
                () => FormatResults(MovieAnalyzer.FindFilmsByComposer(movies, "Hans Zimmer"))),

            ("Создать словарь, где ключ — ID фильма, а значение — имя режиссера.", "7_Movie_Director_Map.txt",
                () => FormatResults(MovieAnalyzer.GetMovieDirectorMap(movies), item => $"ID {item.Key}: {item.Value}")),

            ("Найти фильмы, где в актерском составе есть и 'Brad Pitt', и 'George Clooney'.", "8_Pitt_Clooney_Films.txt",
                () => FormatResults(MovieAnalyzer.FindFilmsWithDuo(movies, "Brad Pitt", "George Clooney"))),

            ("Посчитать, сколько всего человек работает в департаменте 'Camera' по всем фильмам.", "9_Camera_Department_Count.txt",
                () => MovieAnalyzer.CountUniquePeopleInDepartment(movies, "Camera").ToString() + " уникальных человек"),

            ("Найти всех людей, которые в фильме 'Titanic' были одновременно и в съемочной группе, и в списке актеров.", "10_Titanic_Crossover.txt",
                () => FormatResults(MovieAnalyzer.FindCrossoverPeopleInMovie(movies, "Titanic"))),

            ("Найти 'внутренний круг' режиссера: Для 'Quentin Tarantino' найти топ-5 членов съемочной группы.", "11_Tarantino_InnerCircle.txt",
                () => FormatResults(MovieAnalyzer.FindDirectorsInnerCircle(movies, "Quentin Tarantino", 5), item => $"{item.CrewName}: {item.FilmsTogether} фильмов")),

            ("Определить экранные 'дуэты': Найти 10 пар актеров, которые чаще всего снимались вместе.", "12_Top10_Duos.txt",
                () => FormatResults(MovieAnalyzer.FindTopDuos(movies, 10), item => $"{item.Actor1} & {item.Actor2}: {item.FilmsTogether} фильмов")),

            ("Вычислить 'индекс разнообразия': Найти 5 членов съемочной группы, работавших в наибольшем числе департаментов.", "13_Top5_VersatileCrew.txt",
                () => FormatResults(MovieAnalyzer.FindTopVersatileCrew(movies, 5), item => $"{item.CrewName}: {item.DepartmentCount} департаментов")),

            ("Найти 'творческие трио': фильмы, где один человек был режиссером, сценаристом и продюсером.", "14_Creative_Trios.txt",
                () => FormatResults(MovieAnalyzer.FindCreativeTrios(movies), item => $"{item.MovieTitle} ({item.UniversalPerson})")),

            ("Два шага до Кевина Бейкона.", "15_Two_Steps_To_Bacon.txt",
                () => FormatResults(MovieAnalyzer.FindTwoStepsToKevinBacon(movies, "Kevin Bacon"))),

            ("Проанализировать 'командную работу': Средний размер Cast/Crew по режиссеру.", "16_Director_Team_Stats.txt",
                () => FormatResults(MovieAnalyzer.AnalyzeTeamwork(movies), item => $"{item.DirectorName}: Cast={item.AvgCastSize:F2}, Crew={item.AvgCrewSize:F2}")),

            ("Определить карьерный путь 'универсалов'.", "17_Universal_Career_Path.txt",
                () => FormatResults(MovieAnalyzer.FindCareerPath(movies), item => $"{item.Name}: {item.MostFrequentDepartment} ({item.Count} раз)")),

            ("Найти пересечение 'элитных клубов': Работавшие с Мартином Скорсезе и Кристофером Ноланом.", "18_Scorsese_Nolan_Intersection.txt",
                () => FormatResults(MovieAnalyzer.FindEliteIntersection(movies, "Martin Scorsese", "Christopher Nolan"))),

            ("Выявить 'скрытое влияние': Ранжировать департаменты по среднему Cast Size.", "19_Department_Influence.txt",
                () => FormatResults(MovieAnalyzer.AnalyzeDepartmentInfluence(movies), item => $"{item.Department}: {item.AvgCastSize:F2} (Avg Cast)")),

            ("Проанализировать 'архетипы' персонажей: Роли Джонни Деппа.", "20_JohnnyDepp_Archetypes.txt",
                () => FormatResults(MovieAnalyzer.AnalyzeActorArchetypes(movies, "Johnny Depp"), item => $"{item.Archetype}: {item.Count} раз"))
        };

        int counter = 0;
        foreach (var task in analysisTasks)
        {
            counter++;
            RunAnalysisTask(counter, task.Title, task.FileName, task.Action);
        }
    }

    private static void RunAnalysisTask(int number, string title, string fileName, Func<string> analysisAction)
    {
        string separator = new string('-', 100);
        System.Console.ForegroundColor = System.ConsoleColor.Cyan;
        System.Console.WriteLine($"\n{number}. {title}");
        System.Console.WriteLine(separator);
        System.Console.ResetColor();

        string results = string.Empty;
        try
        {
            results = analysisAction();
            
            // Вывод в консоль
            System.Console.WriteLine(results);

            // Запись в файл
            string fullPath = Path.Combine(RESULTS_DIR, fileName);
            string fileContent = $"{number}. {title}\n{separator}\n{results}";
            File.WriteAllText(fullPath, fileContent, Encoding.UTF8);
        }
        catch (System.Exception ex)
        {
            System.Console.ForegroundColor = System.ConsoleColor.Red;
            System.Console.WriteLine($"Ошибка при выполнении задачи: {ex.Message}");
            System.Console.ResetColor();
            results = $"Ошибка: {ex.Message}";
        }
        
        System.Console.WriteLine(separator);
    }

    private static string FormatResults<T>(IEnumerable<T> items, Func<T, string> formatter = null)
    {
        if (items == null || !items.Any())
        {
            return "Результатов не найдено.";
        }
        
        if (formatter == null)
        {
            formatter = item => item.ToString();
        }

        var sb = new StringBuilder();
        foreach (var item in items)
        {
            sb.AppendLine(formatter(item));
        }
        return sb.ToString().TrimEnd();
    }
}