package Pokemons;

import ru.ifmo.se.pokemon.*;
import Physical.*;
import Status.*;
import Special.*;

public final class Clefable extends Clefairy {
    public Clefable(String name, int lvl) {
        super(name, lvl);
        setType(Type.FAIRY);
        setStats(90,70,73,95,90,60);
        setMove(new Facade(), new ShadowBall(), new Growl(), new FireBlast());
    }
}
