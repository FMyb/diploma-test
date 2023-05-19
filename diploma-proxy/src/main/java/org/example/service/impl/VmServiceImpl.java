package org.example.service.impl;

import jakarta.transaction.Transactional;
import org.example.model.VM;
import org.example.repository.VMRepository;
import org.example.service.VmService;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Optional;

/**
 * @author Yaroslav Ilin
 */
@Service
public class VmServiceImpl implements VmService {
    private final VMRepository vmRepository;

    public VmServiceImpl(VMRepository vmRepository) {
        this.vmRepository = vmRepository;
    }

    @Override
    public List<VM> availableVm() {
        return vmRepository.findAllByBusyIsNull();
    }

    @Override
    @Transactional
    public VM allocateVm(String reserving) {
        Optional<VM> vmOptional = vmRepository.findByBusy(reserving);
        if (vmOptional.isPresent()) {
            return vmOptional.get();
        }
        VM vm = vmRepository.findFirstByBusyIsNull()
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "vm not found"));
        vm.setBusy(reserving);
        vmRepository.save(vm);
        return vm;
    }
}
