    public class Battalion
    {
        public string Name { get; set; }
        public List<Warrior> Warriors { get; set; }

        public Battalion(string name)
        {
            Name = name;
            Warriors = new List<Warrior>();
        }

        public void AddWarrior(Warrior warrior)
        {
            Warriors.Add(warrior);
        }

        public void RemoveWarrior(Warrior warrior)
        {
            Warriors.Remove(warrior);
        }

        public bool HasAliveWarriors()
        {
            return Warriors.Any(w => w.IsAlive);
        }

        public List<Warrior> GetAliveWarriors()
        {
            return Warriors.Where(w => w.IsAlive).ToList();
        }

        public void PrintBattalionStatus()
        {
            Console.WriteLine($"\n=== {Name} ===");
            var aliveWarriors = Warriors.Where(w => w.IsAlive).ToList();
            var deadWarriors = Warriors.Where(w => !w.IsAlive).ToList();
            
            Console.WriteLine("Живые:");
            foreach (var warrior in aliveWarriors)
            {
                warrior.PrintStatus();
            }
            
            if (deadWarriors.Any())
            {
                Console.WriteLine("Мертвые:");
                foreach (var warrior in deadWarriors)
                {
                    Console.WriteLine($"{warrior.Name} (убит)");
                }
            }
        }

        public int GetTotalHealth()
        {
            return Warriors.Where(w => w.IsAlive).Sum(w => w.Health);
        }
    }
