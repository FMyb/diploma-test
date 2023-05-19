package org.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;

import java.net.UnknownHostException;

/**
 * @author Yaroslav Ilin
 */
@SpringBootApplication(exclude = {SecurityAutoConfiguration.class})
@EnableWebSocket
public class ProxyApplication {
    public static void main(String[] args) {
        SpringApplication.run(ProxyApplication.class, args);
    }
}