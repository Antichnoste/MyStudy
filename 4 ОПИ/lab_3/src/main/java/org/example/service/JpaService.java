package org.example.service;

import org.example.model.HitEntity;

import javax.persistence.*;
import java.time.LocalTime;
import java.util.List;

public class JpaService {

    private static class EmfHolder {
        static final EntityManagerFactory EMF = Persistence.createEntityManagerFactory("default");;
    }

    public void insertResult(double x, double y, int r, boolean hit, LocalTime createdAt) {
        EntityManager em = EmfHolder.EMF.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        try {
            tx.begin();
            HitEntity e = new HitEntity();
            e.setX(x); e.setY(y); e.setR(r);
            e.setHit(hit);
            e.setCreatedAt(createdAt);
            em.persist(e);
            tx.commit();
        } catch (RuntimeException ex) {
            if (tx.isActive()) tx.rollback();
            throw ex;
        } finally {
            em.close();
        }
    }

    public List<HitEntity> listLatest(int maxRows) {
        EntityManager em = EmfHolder.EMF.createEntityManager();
        try {
            return em.createQuery(
                            "SELECT h FROM HitEntity h ORDER BY h.createdAt DESC", HitEntity.class)
                    .setMaxResults(maxRows)
                    .getResultList();
        } finally {
            em.close();
        }
    }
}

