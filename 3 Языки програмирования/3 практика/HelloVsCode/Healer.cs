    public class Healer : Warrior
    {
        public Healer(string name) : base(name, 70, 10, 4, 6) { }

        public override void SpecialAbility(List<Warrior> allies, List<Warrior> enemies)
        {
            var woundedAlly = allies.Where(a => a.IsAlive && a.Health < a.MaxHealth)
                                .OrderBy(a => a.Health)
                                .FirstOrDefault();

            if (woundedAlly != null)
            {
                int healAmount = 25;
                woundedAlly.Health = Math.Min(woundedAlly.Health + healAmount, woundedAlly.MaxHealth);
                Console.WriteLine($"{Name} лечит {woundedAlly.Name} на {healAmount} HP!");
            }
            else
            {
                base.SpecialAbility(allies, enemies);
            }
        }
    }
