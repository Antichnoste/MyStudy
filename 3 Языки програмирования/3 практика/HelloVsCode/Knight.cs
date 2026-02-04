    public class Knight : Warrior
    {
        public Knight(string name) : base(name, 120, 18, 8, 3) { }

        public override void SpecialAbility(List<Warrior> allies, List<Warrior> enemies)
        {
            var weakAlly = allies.Where(a => a.IsAlive && a != this)
                            .OrderBy(a => a.Health)
                            .FirstOrDefault();
            
            if (weakAlly != null)
            {
                weakAlly.Armor += 3;
                Console.WriteLine($"{Name} защищает {weakAlly.Name}! Броня увеличена до {weakAlly.Armor}");
            }
            else
            {
                base.SpecialAbility(allies, enemies);
            }
        }
    }
