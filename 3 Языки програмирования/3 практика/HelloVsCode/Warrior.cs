    public abstract class Warrior
    {
        public string Name { get; set; }
        public int Health { get; set; }
        public int MaxHealth { get; set; }
        public int Damage { get; set; }
        public int Armor { get; set; }
        public int Speed { get; set; }

        public Warrior(string name, int health, int damage, int armor, int speed)
        {
            Name = name;
            Health = health;
            MaxHealth = health;
            Damage = damage;
            Armor = armor;
            Speed = speed;
        }

        public virtual void Attack(Warrior target)
        {
            int actualDamage = Math.Max(Damage - target.Armor, 1);
            target.Health = Math.Max(0, target.Health - actualDamage);
            Console.WriteLine($"{Name} атакует {target.Name} и наносит {actualDamage} урона!");
        }

        public virtual void SpecialAbility(List<Warrior> allies, List<Warrior> enemies)
        {
            var target = GetRandomAliveTarget(enemies);
            if (target != null) Attack(target);
        }

        public bool IsAlive => Health > 0;

        public virtual void PrintStatus()
        {
            string healthBar = GetHealthBar();
            Console.WriteLine($"{Name}: {healthBar} {Health}/{MaxHealth} HP | Броня: {Armor} | Урон: {Damage} | Скорость: {Speed}");
        }

        protected string GetHealthBar()
        {
            int currentHealth = Math.Max(Health, 0);
            int bars = (int)((double)currentHealth / MaxHealth * 10);
            bars = Math.Max(0, Math.Min(10, bars));
            return new string('█', bars) + new string('_', 10 - bars);
        }

        public  Warrior GetRandomAliveTarget(List<Warrior> warriors)
        {
            var alive = warriors.FindAll(w => w.IsAlive);
            if (alive.Count == 0) return null;
            var random = new Random();
            return alive[random.Next(alive.Count)];
        }
    }
