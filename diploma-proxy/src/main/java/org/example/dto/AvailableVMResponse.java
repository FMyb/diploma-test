package org.example.dto;

import java.util.List;

/**
 * @author Yaroslav Ilin
 */
public class AvailableVMResponse {
    private List<VMDto> data;

    public AvailableVMResponse(List<VMDto> data) {
        this.data = data;
    }

    public List<VMDto> getData() {
        return data;
    }

    public void setData(List<VMDto> data) {
        this.data = data;
    }
}
