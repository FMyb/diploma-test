package org.example.controller;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.apache.hc.core5.net.URIBuilder;
import org.example.ProxyService;
import org.example.model.VM;
import org.example.service.VmService;
import org.springframework.http.HttpMethod;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.view.RedirectView;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.UUID;

@RestController
@CrossOrigin
public class ProxyController {
    private final ProxyService service;

    private final VmService vmService;

    public ProxyController(ProxyService service, VmService vmService) {
        this.service = service;
        this.vmService = vmService;
    }

    @GetMapping(value = "/")
    public RedirectView doorman(HttpServletRequest request) throws URISyntaxException {
        VM vm = vmService.allocateVm(request.getRemoteAddr());
        URI address = new URIBuilder()
                .setScheme("http")
                .setHost(vm.getHost())
                .setPort(8888)
                .setParameter("token", vm.getToken())
                .build();
        RedirectView redirectView = new RedirectView(address.toString());
        return redirectView;
    }

    @RequestMapping(value = "/**", headers = "Connection!=Upgrade")
    public Object sendRequestToSPM(@RequestBody(required = false) byte[] body,
                                   HttpMethod method, HttpServletRequest request, HttpServletResponse response)
            throws URISyntaxException {
        return service.processProxyRequest(body, method, request, response, UUID.randomUUID().toString());
    }
}