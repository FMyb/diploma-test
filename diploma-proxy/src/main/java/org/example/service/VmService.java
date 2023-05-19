package org.example.service;

import org.example.model.VM;

import java.util.List;

/**
 * @author Yaroslav Ilin
 */
public interface VmService {
    List<VM> availableVm();

    VM allocateVm(String reserving);
}
