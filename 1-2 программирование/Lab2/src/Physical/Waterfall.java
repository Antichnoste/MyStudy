package Physical;

import ru.ifmo.se.pokemon.*;

public class Waterfall extends PhysicalMove {
    public Waterfall() {
        super(Type.WATER, 80,100);
    }

    private boolean flag;
    @Override
    protected void applyOppEffects(Pokemon pokemon){
        if (Math.random() <= 0.2){
            flag = true;
            Effect.flinch(pokemon);
        }
    }


    @Override
    protected String describe() {
        return flag ? "ударил и испугал" : "ударил";
    }
}
