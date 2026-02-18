package Pokemons;

import ru.ifmo.se.pokemon.*;
import Physical.*;
import Status.*;
import Special.*;

public final class Pinsir extends Pokemon {
    public Pinsir(String name, int lvl){
        super(name, lvl);
        setType(Type.BUG);
        setStats(65,125,100,55,70,85);
        setMove(new Submission(), new Facade(), new DoubleTeam(), new FuryAttack());
    }
}
