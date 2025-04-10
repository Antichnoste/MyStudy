package common.command;

import java.io.Serializable;

public enum CommandTypes implements Serializable {

    Add("add"),
    Average_of_oscars_count("average_of_oscars_count"),
    Clear("clear"),
    Execute_script("execute_script"),
    Exit("exit"),
    Filter_contains_name("filter_contains_name"),
    Filter_starts_with_tagline("filter_starts_with_tagline"),
    Help("help"),
    History("history"),
    Info("info"),
    Remove_by_id("remove_by_id"),
    Remove_first("remove_first"),
    Remove_greater("remove_greater"),
    Save("save"),
    Show("show"),
    Update("update"),
    Add_to_history("add_to_history");

    private String type;

    private CommandTypes(String type) {
        this.type = type;
    }

    public String Type() {
        return type;
    }

    private static final long serialVersionUID = 14L;

    public static CommandTypes getByString(String string) {
        try {

            return CommandTypes.valueOf(string.toUpperCase().charAt(0) + string.substring(1).toLowerCase());
        } catch (NullPointerException | IllegalArgumentException e) {
        }
        return null;
    }

}
