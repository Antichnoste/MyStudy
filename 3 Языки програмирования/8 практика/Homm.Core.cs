using System;
using System.Reflection;
using System.Linq;
using System.Collections.Generic;

namespace Homm.Core
{
    public class UnitStats { public int Hp { get; set; } }

    public class BattleContext
    {
        public int DamageDealt { get; set; }
        public UnitStats Attacker { get; set; } = new UnitStats();
        public UnitStats Defender { get; set; } = new UnitStats();
    }

    public enum TriggerType { OnAttack, OnDefense, PostBattle }

    [AttributeUsage(AttributeTargets.Method)]
    public class CombatSkillAttribute : Attribute
    {
        public string Name { get; }
        public TriggerType Trigger { get; }
        public int Priority { get; }
        public CombatSkillAttribute(string name, TriggerType trigger, int priority = 1)
        {
            Name = name; Trigger = trigger; Priority = priority;
        }
    }

    [AttributeUsage(AttributeTargets.Class)]
    public class GameAttribute : Attribute { }

    [GameAttribute]
    public class VampireMechanics
    {
        [CombatSkill("CriticalStrike", TriggerType.OnAttack, 100)]
        public void ExecuteCrit(BattleContext ctx)
        {
            ctx.DamageDealt *= 2;
            Console.WriteLine($"[Skill] Critical Hit! New Damage: {ctx.DamageDealt}");
        }

        [CombatSkill("Vampirism", TriggerType.OnAttack, 10)]
        public void ExecuteLifeDrain(BattleContext ctx)
        {
            int heal = ctx.DamageDealt / 2;
            ctx.Attacker.Hp += heal;
            Console.WriteLine($"[Skill] Vampirism: Healed {heal} HP.");
        }
    }

    public class SkillEngine
    {
        private Dictionary<TriggerType, List<(MethodInfo Method, object Instance, int Priority)>> _pipeline;

        public SkillEngine()
        {
            _pipeline = Enum.GetValues(typeof(TriggerType))
                .Cast<TriggerType>()
                .ToDictionary(t => t, _ => new List<(MethodInfo, object, int)>());
        }

        public void RegisterAssembly(Assembly assembly)
        {
            var types = assembly.GetTypes().Where(t => t.GetCustomAttribute<GameAttribute>() != null);
            foreach (var type in types)
            {
                object instance = Activator.CreateInstance(type)
                    ?? throw new InvalidOperationException($"Failed to create instance of {type.FullName}.");
                foreach (var method in type.GetMethods())
                {
                    var attr = method.GetCustomAttribute<CombatSkillAttribute>();
                    if (attr != null)
                    {
                        _pipeline[attr.Trigger].Add((method, instance, attr.Priority));
                        Console.WriteLine($"Registered: {attr.Name} (Priority: {attr.Priority})");
                    }
                }
            }
            foreach (var key in _pipeline.Keys.ToList())
                _pipeline[key] = _pipeline[key].OrderByDescending(x => x.Priority).ToList();
        }

        public void ExecutePipeline(TriggerType trigger, BattleContext context)
        {
            foreach (var skill in _pipeline[trigger])
                skill.Method.Invoke(skill.Instance, new object[] { context });
        }
    }
}