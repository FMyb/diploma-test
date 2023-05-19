package org.example.service;

import org.example.dto.VMDto;

import java.net.URISyntaxException;

/**
 * @author Yaroslav Ilin
 */
public interface CheckpointService {
    String switchVm(String from, VMDto to) throws URISyntaxException;
}
