using System.Reflection;

public class Program
{
    public static void Main()
    {
        Console.WriteLine("=== PART 1: SKILL ENGINE ===");
        var engine = new Homm.Core.SkillEngine();
        engine.RegisterAssembly(Assembly.GetExecutingAssembly());

        var ctx = new Homm.Core.BattleContext { 
            DamageDealt = 100, 
            Attacker = new Homm.Core.UnitStats { Hp = 50 } 
        };

        engine.ExecutePipeline(Homm.Core.TriggerType.OnAttack, ctx);
        Console.WriteLine($"Final Attacker HP: {ctx.Attacker.Hp}");

        Console.WriteLine("\n=== PART 2: PERFORMANCE TEST (Emit) ===");
        EmitDemo.RunPerformanceTest();
    }
}