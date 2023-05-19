package org.example.service.impl;

import org.apache.hc.core5.net.URIBuilder;
import org.example.client.RestVMClient;
import org.example.dto.VMDto;
import org.example.model.Checkpoint;
import org.example.model.VM;
import org.example.repository.CheckpointRepository;
import org.example.repository.VMRepository;
import org.example.resolver.VMResolver;
import org.example.service.CheckpointService;
import org.springframework.stereotype.Service;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.UUID;

/**
 * @author Yaroslav Ilin
 */
@Service
public class CheckpointServiceImpl implements CheckpointService {
    private final CheckpointRepository checkpointRepository;
    private final RestVMClient vmClient;

    private final VMResolver vmResolver;

    private final VMRepository vmRepository;

    public CheckpointServiceImpl(
            CheckpointRepository checkpointRepository,
            RestVMClient vmClient,
            VMResolver vmResolver,
            VMRepository vmRepository
    ) {
        this.checkpointRepository = checkpointRepository;
        this.vmClient = vmClient;
        this.vmResolver = vmResolver;
        this.vmRepository = vmRepository;
    }


    @Override
    public String switchVm(String from, VMDto to) throws URISyntaxException {
        VM currentVm = vmResolver.current(from);
        URI fromAddress = new URIBuilder().setScheme("http").setHost(currentVm.getHost()).setPort(8080).setPath("/save_state").build();
        Checkpoint checkpoint = new Checkpoint(UUID.randomUUID().toString(), "");
        vmClient.saveState(fromAddress, checkpoint.getCheckpointId());
        checkpointRepository.save(checkpoint);
        VM toVm = vmResolver.resolve(to.getId());
        URI toAddress = new URIBuilder().setScheme("http").setHost(toVm.getHost()).setPort(8080).setPath("/load_state").build();
        vmClient.loadState(toAddress, checkpoint.getCheckpointId());
        toVm.setBusy(currentVm.getBusy());
        vmRepository.save(toVm);
        return "http://" + toVm.getHost() + ":8888/?token=" + currentVm.getToken();
    }
}
