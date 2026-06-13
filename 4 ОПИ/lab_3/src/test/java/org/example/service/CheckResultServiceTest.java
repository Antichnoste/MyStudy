package org.example.service;

import org.junit.Assert;
import org.junit.Test;

import java.time.LocalTime;

public class CheckResultServiceTest {

	private class StubGeometry extends Geometry {
		private final boolean hitResult;

		private StubGeometry(boolean hitResult) {
			this.hitResult = hitResult;
		}

		@Override
		public boolean hit(double x, double y, int r) {
			return hitResult;
		}
	}

	private static class StubJpaService extends JpaService {
		private boolean called;
		private double x;
		private double y;
		private int r;
		private boolean hit;
		private LocalTime createdAt;

		@Override
		public void insertResult(double x, double y, int r, boolean hit, LocalTime createdAt) {
			this.called = true;
			this.x = x;
			this.y = y;
			this.r = r;
			this.hit = hit;
			this.createdAt = createdAt;
		}
	}

	@Test
	public void checkAndPersistUsesStubbedHit() {
		CheckResultService service = new CheckResultService();
		StubJpaService jpaService = new StubJpaService();
        StubGeometry geometryTrue = new StubGeometry(true);

		service.setJpaService(jpaService);
		service.setGeometry(geometryTrue);

		service.checkAndPersist(1.5, -2.0, 4);

		Assert.assertTrue(jpaService.called);
		Assert.assertEquals(1.5, jpaService.x, 0.0);
		Assert.assertEquals(-2.0, jpaService.y, 0.0);
		Assert.assertEquals(4, jpaService.r);
		Assert.assertTrue(jpaService.hit);
		Assert.assertNotNull(jpaService.createdAt);
	}
}
