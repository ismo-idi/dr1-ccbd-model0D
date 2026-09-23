# Constrained Consensus-Based Dynamics for Decentralized Path Planning in UAV Swarms

Supporting material for **Directed Research 1**, UM6P Vanguard Center.

**ASSOUMANE IDI Ismaël**, University Mohammed VI Polytechnic (UM6P), Vanguard Center, Morocco.
Supervisors: HABBAL Abderrahmane (Université Côte d'Azur), HARMEN Yasser (UM6P), RATNANI Ahmed (UM6P).

---

## The report

[`Report-DR_ASSOUMANE-IDI.pdf`](Report-DR_ASSOUMANE-IDI.pdf) is the complete Directed Research
report. It is self-contained: every result, derivation, numerical value and limitation is
stated in the report itself. This repository exists so that the computations and the
simulation environment behind it can be inspected and re-run.

## The presentation

[`Presentation-DR_ASSOUMANE-IDI.pdf`](Presentation-DR_ASSOUMANE-IDI.pdf) is the slide deck of the
Predoc Research Project Defense of 25 September 2026. Its two embedded demonstration videos play
in Adobe Acrobat Reader; other PDF viewers show a still frame. The same videos are available as
MP4 files under `ros2_gazebo_um6p_campus/demo/*/media/videos/`.

## What is here

### `model0d_alg2_numerics/` — the numerical study

The two-vehicle crossing instance reported in Section 10 of the report: the distributed
two-level solver, the recorded solve, the exact-rational safety certificate, the independent
centralized reference solve and the objective-weight sensitivity sweep.

- `validation/centralized_reference/` — the independent centralized solve used as an external
  validation oracle, with its environment record and checksums.
- `attempts/` — the recorded solver campaigns, each with its configuration, console output,
  diagnostics, plots and provenance.
- `requirements/` — the dependency manifests, one per campaign.
- `FINAL_SIMULATION_CAMPAIGN_REPORT_18_SEP_2026.md` — the campaign record from which the
  numbers in Section 10 of the report are taken.

### `ros2_gazebo_um6p_campus/` — the physics-based simulation environment

The UM6P-inspired campus scene and the two kinematic demonstrations shown in Section 11 of
the report, built on **ROS 2 Jazzy** and **Gazebo Sim** under Ubuntu 24.04.

- `campus_environment/` — the scene description, generated from a written specification by a
  deterministic script, and its bring-up packages.
- `demo/demo_1_no_obstacle/` and `demo/demo_2_static_sphere/` — the two demonstrations,
  including the **recorded videos** under `media/videos/`.
- `evidence/` — recorded verification runs, screenshots and results.
- `tutorial/` — the environment and demonstration build tutorials.
- `SHA256SUMS` — integrity manifest; see *Integrity* below.

### `exploration/` — the two scoping studies

- `model-0U/` — the uncertainty extension scoped in Section 12 of the report.
- `splines/` — the higher-order trajectory study scoped in Section 13.

## Reproducing

Each study carries its own instructions. In short:

- Numerical study: create the environment from the matching file in
  `model0d_alg2_numerics/requirements/`, then follow the reproduction notes in the campaign
  directory. Runs are single-threaded with a fixed hash seed and a fixed reduction order, and
  two independent executions produce bit-identical saved state.
- Simulation environment: see `ros2_gazebo_um6p_campus/README.md` and
  `ros2_gazebo_um6p_campus/docs/REPRODUCIBILITY.md`.

Reproducibility of this kind establishes that a computation is deterministic, not that it is
correct. That is why the numerical results are additionally accompanied by an
exact-arithmetic certificate, an independent recomputation of the constraint values, and the
external centralized comparison — none of which an implementation could pass merely by
repeating itself.

## Integrity

`ros2_gazebo_um6p_campus/SHA256SUMS` verifies the simulation tree, and
`model0d_alg2_numerics/validation/centralized_reference/SHA256SUMS` verifies the centralized
reference. Verify with:

    cd ros2_gazebo_um6p_campus && sha256sum -c SHA256SUMS

Two files listed in that manifest are deliberately **not** published here, and will therefore
be reported as missing:

- `references/repository-source-manifest.json`
- `references/phase2-repository.json`

Both are snapshots of the private working repository's file listing. They record nothing
about the scientific work and are omitted so that this public repository does not carry a
directory listing of a private one. Every other entry in the manifest verifies.

## Note for Windows users

A small number of recorded screenshots under `ros2_gazebo_um6p_campus/evidence/` are named
with ISO-8601 timestamps containing colons, which Windows filesystems do not accept. Git for
Windows will report an error for those files during checkout while cloning the rest normally;
they can be viewed directly on GitHub. The names are left unchanged so that the SHA-256
manifest above still verifies byte-for-byte.

## Original assignment

The original Directed Research assignment document is not published here. It can be shared on
request.
