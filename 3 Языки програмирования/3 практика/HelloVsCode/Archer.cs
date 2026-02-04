    public class Archer : Warrior
    {
        private int _criticalChance = 25;

        public Archer(string name) : base(name, 80, 25, 3, 8) { }

        public override void Attack(Warrior target)
        {
            var random = new Random();
            bool isCritical = random.Next(100) < _criticalChance;
            int damage = isCritical ? Damage * 2 : Damage;
            int actualDamage = Math.Max(damage - target.Armor, 1);

            target.Health = Math.Max(0, target.Health - actualDamage);

            if (isCritical)
            {
                Console.WriteLine($"{Name} совершает КРИТИЧЕСКИЙ выстрел в {target.Name} и наносит {actualDamage} урона!");
            }
            else
            {
                Console.WriteLine($"{Name} стреляет в {target.Name} и наносит {actualDamage} урона!");
            }
        }
    }
