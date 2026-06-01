package dev.gerard.signalharbor;

import dev.gerard.signalharbor.config.SignalHarborProperties;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.cache.annotation.EnableCaching;

@EnableCaching
@SpringBootApplication
@EnableConfigurationProperties(SignalHarborProperties.class)
public class SignalHarborApplication {

	public static void main(String[] args) {
		SpringApplication.run(SignalHarborApplication.class, args);
	}

}
