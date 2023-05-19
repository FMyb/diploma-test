package org.example.dto;

/**
 * @author Yaroslav Ilin
 */
public class LoadStateRequest {
    private String checkpointName;

    public LoadStateRequest(String checkpointName) {
        this.checkpointName = checkpointName;
    }

    public String getCheckpointName() {
        return checkpointName;
    }

    public void setCheckpointName(String checkpointName) {
        this.checkpointName = checkpointName;
    }
}
