package org.example;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

@Component
public class ProxyWebSocketConfigurer implements WebSocketConfigurer {
    private final String host;

    private final String port;

    public ProxyWebSocketConfigurer(
            @Value("${proxy.host}") String host,
            @Value("${proxy.port}") String port
    ) {
        this.host = host;
        this.port = port;
    }

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(new ProxyServerHandler(host, port), "/*");
    }

}