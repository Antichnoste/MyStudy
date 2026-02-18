package Physical;

import ru.ifmo.se.pokemon.*;

public class Facade extends PhysicalMove {
    public Facade(){
        super(Type.NORMAL, 70,100);
    }

    private boolean flag = false;

    @Override
    protected void applyOppDamage(Pokemon pokemon, double damage) {
        Status condition = pokemon.getCondition();

        if (condition.equals(Status.BURN) || condition.equals(Status.POISON) || condition.equals(Status.PARALYZE)) {
            flag = true;
            pokemon.setMod(Stat.HP, 2 * (int) Math.round(damage));
        } else{
            pokemon.setMod(Stat.HP, (int) Math.round(damage));
        }
    }

    @Override
    protected String describe() {
        return flag ? "сильно бьёт" : "бьёт" ;
    }

    @Override
    protected String describe(int a) {
        return flag ? "сильно бьёт" : "бьёт" ;
    }
}
