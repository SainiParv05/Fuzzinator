"""
mutator.py
Fuzzinator — Input Mutation Engine

Implements 4 mutation strategies for fuzzing:
  0: bit_flip   — flip a random bit
  1: byte_flip  — flip a random byte (XOR 0xFF)
  2: byte_insert — insert a random byte at a random position
  3: havoc      — apply multiple random mutations

All mutations operate on bytearray inputs.
"""

import random
import copy


# Number of available mutation strategies
NUM_ACTIONS = 4


def bit_flip(data: bytearray) -> bytearray:
    """Flip a single random bit in the input."""
    if len(data) == 0:
        return bytearray([random.randint(0, 255)])
    result = bytearray(data)
    byte_idx = random.randint(0, len(result) - 1)
    bit_idx = random.randint(0, 7)
    result[byte_idx] ^= (1 << bit_idx)
    return result


def byte_flip(data: bytearray) -> bytearray:
    """Flip (XOR 0xFF) a random byte in the input."""
    if len(data) == 0:
        return bytearray([random.randint(0, 255)])
    result = bytearray(data)
    idx = random.randint(0, len(result) - 1)
    result[idx] ^= 0xFF
    return result


def byte_insert(data: bytearray) -> bytearray:
    """Insert a random byte at a random position."""
    result = bytearray(data)
    pos = random.randint(0, len(result))
    value = random.randint(0, 255)
    result.insert(pos, value)
    # Cap max size to prevent runaway growth
    if len(result) > 1024:
        result = result[:1024]
    return result


def havoc(data: bytearray) -> bytearray:
    """Apply 2–6 random mutations (havoc mode)."""
    result = bytearray(data)
    num_mutations = random.randint(2, 6)
    simple_mutations = [bit_flip, byte_flip, byte_insert]

    for _ in range(num_mutations):
        mutation = random.choice(simple_mutations)
        result = mutation(result)

    # Occasionally overwrite a chunk with random bytes
    if len(result) > 4 and random.random() < 0.3:
        start = random.randint(0, len(result) - 2)
        length = random.randint(1, min(4, len(result) - start))
        for i in range(length):
            result[start + i] = random.randint(0, 255)

    return result


# Strategy lookup table
STRATEGIES = {
    0: bit_flip,
    1: byte_flip,
    2: byte_insert,
    3: havoc,
}

STRATEGY_NAMES = {
    0: "bit_flip",
    1: "byte_flip",
    2: "byte_insert",
    3: "havoc",
}


def mutate(data: bytearray, action: int) -> bytearray:
    """
    Apply a mutation strategy to the input data.

    Args:
        data: Input bytes to mutate
        action: Strategy index (0-3)

    Returns:
        Mutated bytearray
    """
    action = max(0, min(action, NUM_ACTIONS - 1))
    strategy = STRATEGIES[action]
    return strategy(copy.deepcopy(data))
