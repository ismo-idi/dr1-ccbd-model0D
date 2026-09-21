"""Frozen N=2 Trajectory-Copy Consensus assembly for the approved baseline.

Guardian({1,2}) = 1. Source 2 is copied at UAV 1, and the unique equality
edge links UAV 1's source-2 copy to UAV 2's source block.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .config import ModelConfig


@dataclass(frozen=True)
class TCCOperators:
    Q: int
    d1: int
    d2: int
    M_eq: int
    m: int
    S_1_from_1: np.ndarray
    S_1_from_2: np.ndarray
    S_2_from_2: np.ndarray
    A: np.ndarray
    B: np.ndarray

    def stack_Z(self, z1: np.ndarray, z2: np.ndarray) -> np.ndarray:
        return np.concatenate([np.asarray(z1, float).reshape(-1), np.asarray(z2, float).reshape(-1)])

    def split_Z(self, Z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        Z = np.asarray(Z, float).reshape(-1)
        if Z.size != self.d1 + self.d2:
            raise ValueError(f"Z has size {Z.size}, expected {self.d1+self.d2}")
        return Z[: self.d1].copy(), Z[self.d1 :].copy()

    def source1_from_z1(self, z1: np.ndarray) -> np.ndarray:
        return self.S_1_from_1 @ np.asarray(z1, float).reshape(-1)

    def copy2_from_z1(self, z1: np.ndarray) -> np.ndarray:
        return self.S_1_from_2 @ np.asarray(z1, float).reshape(-1)

    def source2_from_z2(self, z2: np.ndarray) -> np.ndarray:
        return self.S_2_from_2 @ np.asarray(z2, float).reshape(-1)

    def target_rows(self, z1: np.ndarray, z2: np.ndarray, u: np.ndarray) -> np.ndarray:
        Z = self.stack_Z(z1, z2)
        return self.A @ Z + self.B @ np.asarray(u, float).reshape(-1)

    def direct_tcc_difference(self, z1: np.ndarray, z2: np.ndarray) -> np.ndarray:
        return self.copy2_from_z1(z1) - self.source2_from_z2(z2)


def assemble_tcc(cfg: ModelConfig) -> TCCOperators:
    Q = cfg.Q
    d1 = 2 * Q
    d2 = Q
    M_eq = 1
    m = 2 * Q

    S11 = np.zeros((Q, d1))
    S11[:, :Q] = np.eye(Q)
    S12 = np.zeros((Q, d1))
    S12[:, Q:] = np.eye(Q)
    S22 = np.eye(Q)

    # Global Z = [z1; z2]. Two half-row blocks:
    # S_{1<-2} z1 - u = 0 ; S_{2<-2} z2 - u = 0.
    A = np.zeros((m, d1 + d2))
    A[:Q, :d1] = S12
    A[Q:, d1:] = S22
    B = np.vstack([-np.eye(Q), -np.eye(Q)])

    return TCCOperators(
        Q=Q, d1=d1, d2=d2, M_eq=M_eq, m=m,
        S_1_from_1=S11, S_1_from_2=S12, S_2_from_2=S22,
        A=A, B=B,
    )


def project_a1(cfg: ModelConfig, u: np.ndarray) -> np.ndarray:
    """Projection onto B_K = B^K for the axis-aligned approved A1 box."""
    arr = np.asarray(u, dtype=float).reshape(cfg.K, cfg.q)
    return np.clip(arr, cfg.a1_lower, cfg.a1_upper).reshape(-1)


def stationary_exact_tcc_initialization(cfg: ModelConfig, ops: TCCOperators):
    """Accepted Gate-3 exact-TCC stationary initialization."""
    x1 = np.tile(cfg.starts[0], cfg.K)
    x2 = np.tile(cfg.starts[1], cfg.K)
    z1 = np.concatenate([x1, x2.copy()])
    z2 = x2.copy()
    u = x2.copy()
    return z1, z2, u
