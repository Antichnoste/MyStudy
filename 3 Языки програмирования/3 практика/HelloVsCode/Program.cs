using System;
using System.Collections.Generic;
using System.Linq;

namespace BattleManager
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("МЕНЕДЖЕР БАТАЛЬОНОВ\n");

            var redBattalion = new Battalion("Красная Армия");
            redBattalion.AddWarrior(new Knight("Сэр Роланд"));
            redBattalion.AddWarrior(new Archer("Леголас"));
            redBattalion.AddWarrior(new Mage("Гэндальф"));
            redBattalion.AddWarrior(new Healer("Жрица Элина"));

            var blueBattalion = new Battalion("Синяя Армия");
            blueBattalion.AddWarrior(new Knight("Черный Рыцарь"));
            blueBattalion.AddWarrior(new Archer("Хоторн"));
            blueBattalion.AddWarrior(new Mage("Мерлин"));
            blueBattalion.AddWarrior(new Healer("Шаман Зорг"));

            redBattalion.PrintBattalionStatus();
            blueBattalion.PrintBattalionStatus();

            var battle = new Battle(redBattalion, blueBattalion);
            battle.StartBattle();
        }
    }
}