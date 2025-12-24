package Special;

import ru.ifmo.se.pokemon.*;

public class ShadowBall extends SpecialMove {
    public ShadowBall() {
        super(Type.GHOST, 80, 100);
    }

    private boolean flag = false;

    @Override
    protected void applyOppEffects(Pokemon pokemon){
        if (Math.random() <= 0.2){
            flag = true;
            pokemon.setMod(Stat.SPECIAL_DEFENSE,-1);
        }
    }

    @Override
    protected String describe(){
        return flag ? "наносит урон и снижает специальную защиту" : "наносит урон";
    }
}
