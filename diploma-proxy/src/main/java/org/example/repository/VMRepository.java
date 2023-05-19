package org.example.repository;

import org.example.model.VM;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * @author Yaroslav Ilin
 */
@Repository
public interface VMRepository extends JpaRepository<VM, String> {
    List<VM> findAllByBusyIsNull();

    Optional<VM> findFirstByBusyIsNull();

    Optional<VM> findByBusy(String busy);
}
