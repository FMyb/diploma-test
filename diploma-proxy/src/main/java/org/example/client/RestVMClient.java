package org.example.client;

import org.example.dto.LoadStateRequest;
import org.example.dto.SaveStateRequest;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.net.URI;

/**
 * @author Yaroslav Ilin
 */
@Component
public class RestVMClient {
    private final RestTemplate restTemplate = new RestTemplate(new HttpComponentsClientHttpRequestFactory());

    public void saveState(URI address, String checkpointId) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<SaveStateRequest> body = new HttpEntity<>(new SaveStateRequest(checkpointId), headers);
        restTemplate.exchange(address, HttpMethod.POST, body, Void.class);
    }

    public void loadState(URI address, String checkpointId) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<LoadStateRequest> body = new HttpEntity<>(new LoadStateRequest(checkpointId), headers);
        restTemplate.exchange(address, HttpMethod.POST, body, Void.class);
    }
}
