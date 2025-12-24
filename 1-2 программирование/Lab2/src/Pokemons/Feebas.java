package Pokemons;

import ru.ifmo.se.pokemon.*;
import Physical.*;
import Status.*;
import Special.*;

public class Feebas extends Pokemon{
    public Feebas(String name, int lvl){
        super(name, lvl);
        setType(Type.WATER);
        setStats(20,15,20,10,55,80);
        setMove(new Waterfall(), new IceBeam(), new Rest());
    }
}
