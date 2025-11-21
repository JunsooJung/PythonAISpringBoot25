package org.mbc.controller.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;


@Configuration
public class WebClientConfig {
    @Bean
    WebClient webclient(){
        return WebClient.builder().exchangeStrategies(ExchangeStrategies.builder()
                        .codecs(configurer
                                    -> configurer.defaultCodecs().maxInMemorySize(-1)) // -1 메모리 지정으로 무제한 인풋 가능
                        .build())
                .baseUrl("http://localhost:8000")
                .build(); // https://blog.naver.com/seek316/223337685249
    }
}
