    public class Mage : Warrior
    {
        private int _mana = 100;

        public Mage(string name) : base(name, 60, 15, 2, 5) { }

        public override void SpecialAbility(List<Warrior> allies, List<Warrior> enemies)
        {
            if (_mana >= 30)
            {
                _mana -= 30;
                Console.WriteLine($"{Name} использует ОГНЕННЫЙ ШАР!");
                
                foreach (var enemy in enemies.Where(e => e.IsAlive))
                {
                    int damage = 20;
                    enemy.Health = Math.Max(0, enemy.Health - damage);
                    Console.WriteLine($"   {enemy.Name} получает {damage} магического урона!");
                }
            }
            else
            {
                base.SpecialAbility(allies, enemies);
            }
}

        public override void PrintStatus()
        {
            base.PrintStatus();
            Console.WriteLine($"   Mana: {_mana}/100");
        }
    }
