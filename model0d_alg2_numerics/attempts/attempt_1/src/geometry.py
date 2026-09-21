"""Exact Model 0-D piecewise-linear segment geometry.

The functions here implement the frozen guarded piecewise squared-distance
representation from Decision 10. Numerical diagnostic thresholds are never
used to alter the mathematical value function; they are applied separately
by diagnostics.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import casadi as ca
import numpy as np

Regime = Literal["degenerate", "endpoint0", "interior", "endpoint1"]


@dataclass(frozen=True)
class SegmentDistanceResult:
    min_squared_distance: float
    lambda_star_clipped: float
    s: float
    dot: float
    regime: Regime


def _as_np(v) -> np.ndarray:
    return np.asarray(v, dtype=float).reshape(-1)


def segment_min_squared_numeric(a, d) -> SegmentDistanceResult:
    """Exact guarded minimum of ||a + lambda d||^2 for lambda in [0,1]."""
    a = _as_np(a)
    d = _as_np(d)
    s = float(np.dot(d, d))
    dot = float(np.dot(a, d))
    if s == 0.0:
        return SegmentDistanceResult(float(np.dot(a, a)), 0.0, s, dot, "degenerate")
    if dot >= 0.0:
        return SegmentDistanceResult(float(np.dot(a, a)), 0.0, s, dot, "endpoint0")
    if dot <= -s:
        apd = a + d
        return SegmentDistanceResult(float(np.dot(apd, apd)), 1.0, s, dot, "endpoint1")
    lam = -dot / s
    value = float(np.dot(a, a) - dot * dot / s)
    # Clamp only roundoff of the analytically interior parameter.
    lam = float(np.clip(lam, 0.0, 1.0))
    return SegmentDistanceResult(value, lam, s, dot, "interior")


def segment_min_squared_symbolic(a, d):
    """CasADi exact-value branch representation.

    The inactive denominator is guarded by an exact s>0 condition rather than
    an epsilon replacement. Therefore for every s>0 the analytical value uses
    the exact denominator s; at s=0 the degenerate endpoint value is selected.
    """
    s = ca.dot(d, d)
    dot = ca.dot(a, d)
    a2 = ca.dot(a, a)
    apd = a + d
    end1 = ca.dot(apd, apd)
    safe_s = ca.if_else(s > 0, s, 1.0)
    interior = a2 - (dot * dot) / safe_s
    nondeg = ca.if_else(dot >= 0, a2, ca.if_else(dot <= -s, end1, interior))
    return ca.if_else(s > 0, nondeg, a2)


def obstacle_segment_constraint_numeric(p0, p1, center, clearance: float) -> tuple[float, SegmentDistanceResult]:
    a = _as_np(p0) - _as_np(center)
    d = _as_np(p1) - _as_np(p0)
    res = segment_min_squared_numeric(a, d)
    return float(clearance * clearance - res.min_squared_distance), res


def obstacle_segment_constraint_symbolic(p0, p1, center, clearance: float):
    c = ca.DM(np.asarray(center, dtype=float).reshape(-1, 1))
    a = p0 - c
    d = p1 - p0
    m = segment_min_squared_symbolic(a, d)
    return clearance * clearance - m


def uav_segment_constraint_numeric(pi0, pi1, pj0, pj1, clearance: float) -> tuple[float, SegmentDistanceResult]:
    a = _as_np(pi0) - _as_np(pj0)
    d = (_as_np(pi1) - _as_np(pj1)) - a
    res = segment_min_squared_numeric(a, d)
    return float(clearance * clearance - res.min_squared_distance), res


def uav_segment_constraint_symbolic(pi0, pi1, pj0, pj1, clearance: float):
    a = pi0 - pj0
    d = (pi1 - pj1) - a
    m = segment_min_squared_symbolic(a, d)
    return clearance * clearance - m


def unsquared_margin_from_squared_min(min_squared_distance: float, clearance: float) -> float:
    if not np.isfinite(min_squared_distance):
        return float("nan")
    # Negative values below zero can arise only from roundoff in the interior formula.
    return float(np.sqrt(max(0.0, min_squared_distance)) - clearance)


def dense_sample_min_squared(a, d, samples: int = 10001) -> float:
    """Independent diagnostic helper used only by component tests."""
    a = _as_np(a)
    d = _as_np(d)
    lam = np.linspace(0.0, 1.0, int(samples), dtype=float)
    pts = a[None, :] + lam[:, None] * d[None, :]
    return float(np.min(np.sum(pts * pts, axis=1)))
