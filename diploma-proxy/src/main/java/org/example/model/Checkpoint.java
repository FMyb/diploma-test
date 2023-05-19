package org.example.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

/**
 * @author Yaroslav Ilin
 */
@Table(name = "checkpoints")
@Entity(name = "checkpoint")
public class Checkpoint {
    @Id
    private String checkpointId;

    @Column
    private String name;

    public Checkpoint(String checkpointId, String name) {
        this.checkpointId = checkpointId;
        this.name = name;
    }

    public Checkpoint() {

    }

    public String getCheckpointId() {
        return checkpointId;
    }

    public void setCheckpointId(String checkpointId) {
        this.checkpointId = checkpointId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
