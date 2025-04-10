package Special;

import ru.ifmo.se.pokemon.*;

public class FireBlast extends SpecialMove {
    public FireBlast() {
        super(Type.FIRE, 110,85);
    }

    private boolean flag = false;

    @Override
    protected void applyOppEffects(Pokemon pokemon){
        if (Math.random() <= 0.1){
            flag = true;
            Effect.burn(pokemon);
        }
    }

    @Override
    protected String describe(){
        return flag ? "поджигает и наносит урон" : "наносит урон";
    }
}
