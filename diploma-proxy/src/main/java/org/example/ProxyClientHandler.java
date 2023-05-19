package org.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.socket.WebSocketMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.AbstractWebSocketHandler;

/**
 * @author Yaroslav Ilin
 */
public class ProxyClientHandler extends AbstractWebSocketHandler {
       private final Logger logger = LoggerFactory.getLogger(ProxyClientHandler.class);

       private final WebSocketSession webSocketServerSession;

       public ProxyClientHandler(WebSocketSession webSocketServerSession) {
              this.webSocketServerSession = webSocketServerSession;
       }

       @Override
       public void handleMessage(WebSocketSession session, WebSocketMessage<?> webSocketMessage) throws Exception {
              webSocketServerSession.sendMessage(webSocketMessage);
       }

       @Override
       public void afterConnectionEstablished(WebSocketSession session) throws Exception {
              super.afterConnectionEstablished(session);
              logger.info("connection established {}", session);
       }
}
