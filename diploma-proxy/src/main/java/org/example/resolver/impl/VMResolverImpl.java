package org.example.resolver.impl;

import org.example.model.VM;
import org.example.repository.VMRepository;
import org.example.resolver.VMResolver;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ResponseStatusException;

/**
 * @author Yaroslav Ilin
 */
@Component
public class VMResolverImpl implements VMResolver {
    private final VMRepository vmRepository;

    public VMResolverImpl(VMRepository vmRepository) {
        this.vmRepository = vmRepository;
    }

    @Override
    public VM resolve(String id) {
        return vmRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "vm not found"));
    }

    @Override
    public VM current(String busy) {
        return vmRepository.findByBusy(busy)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "current vm not found for: " + busy));
    }
}
