package org.example.repository;

import org.example.model.Checkpoint;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

/**
 * @author Yaroslav Ilin
 */
@Repository
public interface CheckpointRepository extends CrudRepository<Checkpoint, String> {
}
