package Pokemons;

import ru.ifmo.se.pokemon.*;
import Physical.*;
import Status.*;
import Special.*;

public class Clefairy extends Cleffa {
    public Clefairy(String name, int lvl) {
        super(name, lvl);
        setType(Type.FAIRY);
        setStats(70,45,48,60,65,35);
        setMove(new Facade(), new ShadowBall(), new Growl());
    }
}
