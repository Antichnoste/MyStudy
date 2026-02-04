    public class Battle
    {
        private readonly Battalion _battalionA;
        private readonly Battalion _battalionB;

        public Battle(Battalion battalionA, Battalion battalionB)
        {
            _battalionA = battalionA;
            _battalionB = battalionB;
        }

        public void StartBattle()
        {
            Console.WriteLine($"БИТВА НАЧИНАЕТСЯ: {_battalionA.Name} vs {_battalionB.Name}!\n");
            int round = 1;

            while (_battalionA.HasAliveWarriors() && _battalionB.HasAliveWarriors())
            {
                Console.WriteLine($"\n === РАУНД {round} ===");
                ExecuteRound();
                round++;
                
                if (round > 100)
                {
                    Console.WriteLine("Битва зашла в тупик!");
                    break;
                }
            }

            AnnounceWinner();
        }

        private void ExecuteRound()
        {
            var allFighters = GetAllFightersBySpeed();
            
            foreach (var fighter in allFighters)
            {
                if (!fighter.IsAlive) continue;

                if (fighter is Knight || fighter is Healer || fighter is Mage)
                {
                    var allies = _battalionA.Warriors.Contains(fighter) ? 
                                _battalionA.GetAliveWarriors() : 
                                _battalionB.GetAliveWarriors();
                    var enemies = _battalionA.Warriors.Contains(fighter) ? 
                                _battalionB.GetAliveWarriors() : 
                                _battalionA.GetAliveWarriors();
                    
                    fighter.SpecialAbility(allies, enemies);
                }
                else
                {
                    var target = fighter.GetRandomAliveTarget(
                        _battalionA.Warriors.Contains(fighter) ? 
                        _battalionB.Warriors : 
                        _battalionA.Warriors
                    );
                    if (target != null) fighter.Attack(target);
                }
            }

            PrintBattleStatus();
        }

        private List<Warrior> GetAllFightersBySpeed()
        {
            var allFighters = new List<Warrior>();
            allFighters.AddRange(_battalionA.Warriors);
            allFighters.AddRange(_battalionB.Warriors);
            return allFighters.OrderByDescending(f => f.Speed).ToList();
        }

        private void PrintBattleStatus()
        {
            _battalionA.PrintBattalionStatus();
            _battalionB.PrintBattalionStatus();
            
            Console.WriteLine($"\nИтог раунда: {_battalionA.Name} - {_battalionA.GetTotalHealth()} HP | " +
                            $"{_battalionB.Name} - {_battalionB.GetTotalHealth()} HP");
        }

        private void AnnounceWinner()
        {
            bool battalionAAlive = _battalionA.HasAliveWarriors();
            bool battalionBAlive = _battalionB.HasAliveWarriors();

            Console.WriteLine("\n === РЕЗУЛЬТАТ БИТВЫ ===");

            if (battalionAAlive && !battalionBAlive)
            {
                Console.WriteLine($"ПОБЕДИЛ {_battalionA.Name}!");
                Console.WriteLine($"Выжившие бойцы:");
                _battalionA.GetAliveWarriors().ForEach(w => Console.WriteLine($"{w.Name}"));
            }
            else if (!battalionAAlive && battalionBAlive)
            {
                Console.WriteLine($"ПОБЕДИЛ {_battalionB.Name}!");
                Console.WriteLine($"Выжившие бойцы:");
                _battalionB.GetAliveWarriors().ForEach(w => Console.WriteLine($"{w.Name}"));
            }
            else
            {
                Console.WriteLine("НИЧЬЯ! Обе армии уничтожены!");
            }
        }
    }
