package Special;

import ru.ifmo.se.pokemon.*;

public class IceBeam extends SpecialMove {
    public IceBeam() {
        super(Type.ICE, 90, 100);
    }

    private boolean flag;
    @Override
    protected void applyOppEffects(Pokemon pokemon){
        if (Math.random() <= 0.1){
            flag = true;
            Effect.freeze(pokemon);
        }
    }

    @Override
    protected String describe(){
        return flag ? "замораживает и наносит урон" : "наносит урон";
    }

}
