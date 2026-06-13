package org.example.web4;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.example.web4.support.PostgresIntegrationTest;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest
@ActiveProfiles("test")
class Web4ApplicationTests extends PostgresIntegrationTest {

	@Test
	void contextLoads() {
	}

}
