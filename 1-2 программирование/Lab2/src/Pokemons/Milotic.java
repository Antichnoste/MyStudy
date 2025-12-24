package Pokemons;

import ru.ifmo.se.pokemon.*;
import Physical.*;
import Status.*;
import Special.*;

import javax.swing.plaf.basic.BasicRadioButtonUI;

public final class Milotic extends Feebas {
    public Milotic(String name, int lvl) {
        super(name, lvl);
        setType(Type.WATER);
        setStats(95,60,79,100,125,81);
        setMove(new Waterfall(), new IceBeam(), new Rest(), new BrutalSwing());
    }
}
