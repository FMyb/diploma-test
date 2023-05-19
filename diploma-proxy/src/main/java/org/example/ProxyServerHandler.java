package org.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.socket.WebSocketMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.AbstractWebSocketHandler;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * @author Yaroslav Ilin
 */
public class ProxyServerHandler extends AbstractWebSocketHandler {
    private final Map<String, NextHop> nextHops = new ConcurrentHashMap<>();
    private final Logger logger = LoggerFactory.getLogger(ProxyServerHandler.class);

    private final String host;

    private final String port;

    public ProxyServerHandler(String host, String port) {
        this.host = host;
        this.port = port;
    }

    @Override
    public void handleMessage(WebSocketSession webSocketSession, WebSocketMessage<?> webSocketMessage) throws Exception {
        getNextHop(webSocketSession).sendMessageToNextHop(webSocketMessage);
    }

    private NextHop getNextHop(WebSocketSession webSocketSession) {
        NextHop nextHop = nextHops.get(webSocketSession.getId());
        if (nextHop == null) {
            nextHop = new NextHop(webSocketSession, host, port);
            nextHops.put(webSocketSession.getId(), nextHop);
        }
        return nextHop;
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        super.afterConnectionEstablished(session);
        getNextHop(session);
        logger.info("connection established {}", session);
    }
}
