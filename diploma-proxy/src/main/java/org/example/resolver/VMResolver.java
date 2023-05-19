package org.example.resolver;

import org.example.model.VM;

/**
 * @author Yaroslav Ilin
 */
public interface VMResolver {
    VM resolve(String id);

    VM current(String busy);
}
