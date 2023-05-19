package org.example.controller;

import jakarta.servlet.http.HttpServletRequest;
import org.example.dto.AvailableVMResponse;
import org.example.dto.VMDto;
import org.example.service.CheckpointService;
import org.example.service.VmService;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;

import java.net.URISyntaxException;
import java.util.List;
import java.util.stream.Collectors;

/**
 * @author Yaroslav Ilin
 */
@RestController
@RequestMapping("/api")
@CrossOrigin
public class CheckpointController {
    private final CheckpointService checkpointService;

    private final VmService vmService;

    public CheckpointController(CheckpointService checkpointService, VmService vmService) {
        this.checkpointService = checkpointService;
        this.vmService = vmService;
    }

    @GetMapping(value = "/available_vm", produces = MediaType.APPLICATION_JSON_VALUE)
    public AvailableVMResponse availableVM() {
        return new AvailableVMResponse(vmService.availableVm().stream()
                .map(it -> new VMDto(it.getVmId(), it.getName()))
                .collect(Collectors.toList())
        );
    }

    @PostMapping(value = "/switch_vm", consumes = MediaType.APPLICATION_JSON_VALUE)
    public String switchVm(@RequestBody VMDto vm, HttpServletRequest request) throws URISyntaxException {
        return checkpointService.switchVm(request.getRemoteAddr(), vm);
    }
}
