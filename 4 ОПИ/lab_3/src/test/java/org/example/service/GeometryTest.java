package org.example.service;

import org.junit.*;

public class GeometryTest {

    private Geometry geometry;

    @BeforeClass
    public static void hello(){
        System.out.println("Выполняется 1 раз перед запуском всего файла");
    }

    @Before
    public void hello_every_time(){
        System.out.println("Выполняется каждый раз перед запуском любого метода с @Test");
    }


    @Test(expected = RuntimeException.class, timeout = 1000)
    @Ignore
    public void hitShouldReturnTrueForPointInsideRectangle() {
        Assert.assertTrue(geometry.hit(-1.0, -1.0, 2));
    }

    @Test
    @Ignore
    public void hitShouldReturnFalseForInvalidRadius() {
        Assert.assertFalse(geometry.hit(0.0, 0.0, 0));
    }
}
