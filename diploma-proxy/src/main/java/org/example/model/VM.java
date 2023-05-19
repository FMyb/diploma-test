package org.example.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

/**
 * @author Yaroslav Ilin
 */
@Entity(name = "vm")
@Table(name = "vms")
public class VM {
    @Id
    private String vmId;

    @Column
    private String host;

    @Column
    private String name;

    @Column
    private String busy;

    @Column
    private String token;

    public VM(String vmId, String host, String name, String busy, String token) {
        this.vmId = vmId;
        this.host = host;
        this.name = name;
        this.busy = busy;
        this.token = token;
    }

    public VM() {

    }

    public String getVmId() {
        return vmId;
    }

    public void setVmId(String vmId) {
        this.vmId = vmId;
    }

    public String getHost() {
        return host;
    }

    public void setHost(String host) {
        this.host = host;
    }

    public String getName() {
        return name;
    }

    public String getBusy() {
        return busy;
    }

    public void setBusy(String busy) {
        this.busy = busy;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }
}
