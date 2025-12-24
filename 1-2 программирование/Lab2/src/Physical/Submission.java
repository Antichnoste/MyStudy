package Physical;

import ru.ifmo.se.pokemon.*;

public class Submission extends PhysicalMove {
    public Submission() {
        super(Type.FIGHTING, 80, 80);
    }

    @Override
    protected void applySelfDamage(Pokemon pokemon, double damage) {
        pokemon.setMod(Stat.HP, (int) Math.round(damage / 4));
    }

    @Override
    protected String describe() {
        return "подичиняет";
    }
}
