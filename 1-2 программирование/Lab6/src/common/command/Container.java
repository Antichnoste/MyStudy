package common.command;

import common.utillity.ExecutionResponse;

import java.io.Serializable;

public class Container implements Serializable {
    private static final long serialVersionUID = 15L;

    private final ExecutionResponse executionResponse;
    private final Object obj;
    private CommandTypes commandTypes;

    public Container(CommandTypes commandTypes, ExecutionResponse executionResponse, Object obj) {
        this.executionResponse = executionResponse;
        this.obj = obj;
        this.commandTypes = commandTypes;
    }

    public Container(CommandTypes commandTypes, Object obj) {
        this.executionResponse = null;
        this.obj = obj;
        this.commandTypes = commandTypes;
    }

    public Container(CommandTypes commandTypes, ExecutionResponse executionResponse) {
        this.executionResponse = executionResponse;
        this.obj = null;
        this.commandTypes = commandTypes;
    }

    public Container(ExecutionResponse executionResponse) {
        this.executionResponse = executionResponse;
        this.obj = null;
        this.commandTypes = null;
    }

    public Container(CommandTypes commandTypes) {
        this.executionResponse = null;
        this.obj = null;
        this.commandTypes = commandTypes;
    }

    public CommandTypes getCommandType() {
        return commandTypes;
    }

    public ExecutionResponse getExecutionResponse() {
        return executionResponse;
    }

    public Object getObj() {
        return obj;
    }
}
