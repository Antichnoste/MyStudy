package Pokemons;

import ru.ifmo.se.pokemon.*;
import Physical.*;
import Status.*;
import Special.*;

public class Cleffa extends Pokemon {
    public Cleffa(String name, int lvl) {
        super(name, lvl);
        setType(Type.FAIRY);
        setStats(50, 25, 28, 45, 55, 15);
        setMove(new Facade(), new ShadowBall());
    }
}
