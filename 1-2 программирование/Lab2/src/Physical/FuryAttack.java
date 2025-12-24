package Physical;

import ru.ifmo.se.pokemon.*;

public class FuryAttack extends PhysicalMove {
    public FuryAttack() {
        super(Type.NORMAL, 15,85);
    }

    @Override
    protected String describe() {
        return "яростно атакует";
    }

    @Override
    protected void applyOppEffects(Pokemon pokemon){
        double probability = Math.random();
        int hits;

        if (probability < 0.375){
            hits = 2;
        } else if (probability < 0.75){
            hits = 3;
        } else if (probability < 0.875){
            hits = 4;
        } else{
            hits = 5;
        }

        pokemon.setMod(Stat.HP, (int) (this.power * hits));
    }

}
