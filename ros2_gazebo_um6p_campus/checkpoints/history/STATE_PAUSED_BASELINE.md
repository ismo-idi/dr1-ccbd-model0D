# Final handoff checkpoint

14 September 2026. Environment preparation is complete to the verified scope below. No pending implementation or environment test remains for this delivery. No remote commit, push, merge or publication occurred.

## Starting reference and preservation

Repository: ismo-idi/CCBO_Model1, branch Model-0_24-Aug-2026. Starting commit and resume-checked head: e3a8af05cbb40793f6b48f26ffe042dc51f0ddca. A pinned connector snapshot was inspected because terminal cloning could not authenticate. This is a dedicated delivery directory, not a claimed Git checkout. Source identities are in references/repository-source-manifest.json and references/inspected-snapshot-sha256.txt. Synced sources, scientific documents, historical archives, presentations and other project files were preserved.

## Completed checklist

- [x] Execution capabilities, user laptop details, official compatible stack and repository context inspected.
- [x] Two installed ament packages, local procedural assets, paused launch, bounded tests and terminal/VS Code tasks delivered.
- [x] User feedback: U/6 +12 degrees, M/P -12 degrees; building +12m Y translation gives 13.8m gap; UAV/pad centers x +/-3.6, y -8.2, origins z .12, yaw +/-.3. Exactly two static UAVs remain.
- [x] Unmarked clear 18x18m forecourt at x[-9,9], y[-22,-4] documented for separately reviewed future staging. No flight capacity/safety claim.
- [x] Other approved model meshes preserved byte-for-byte; deterministic regeneration PASS.
- [x] Final installed SDF/resources validated; actual GUI rendered and screenshot inspected.
- [x] Final GUI launch/relaunch PASS: exact entities/poses, received ROS bridge strings, paused/zero iterations/zero simulation time, clean child exits.
- [x] Final clean directory with spaces: new build/install and two paused headless runs PASS. Tested source identity saved.
- [x] Exact LaTeX, complete imported scripts/configuration listings and 34-page PDF compiled. All final pages visually inspected; PDF_QA.md records results.
- [x] Provenance, observed package versions, mutable dependency limitations, command ledger and PASS/FAIL/NOT VERIFIED record saved.

## Exact next action

Review README.md, tutorial/tutorial.pdf and evidence/VERIFICATION.md. To open locally, use the README's setup-plan, build, headless verification and GUI launch commands from the extracted delivery folder. Stop with Ctrl+C once in the owning terminal. Run only one campus launcher/test at a time.

The final archive is ../ros2_gazebo_um6p_campus_2026-09-14.zip, with adjacent .zip.sha256 and .zip.verification.json. Its top-level folder contains the maintained source, assets, documentation, PDF and evidence. SHA256SUMS inside the folder identifies delivered bytes, excluding itself and disposable generated outputs. The earlier ../campus-preparation-checkpoint.tar.gz is pre-feedback and superseded; do not use it as the final delivery.

## Evidence and dependency state

Native Ubuntu 24.04.5 amd64, ROS 2 Jazzy, Gazebo Sim 8.15.0, ros_gz 1.0.24, Intel Iris Xe / Mesa 25.2.8 / OpenGL 4.6. Existing installation reused; no package installation, host upgrade, graphics-driver or security change. Docker/Podman absent; native route selected. Exact revisions: references/observed-direct-package-pins.txt and evidence/installed-packages.tsv. This is not an immutable binary lock.

Authoritative final results: evidence/gui/results.json and screenshot 2026-09-14T14:14:41.229415443.png; evidence/clean-reproduction/local-headless/results.json; evidence/assets.json; evidence/clean-source-identity.json; evidence/feedback-change-scope.json; evidence/deterministic-generation.json; evidence/PDF_QA.md. Earlier diagnostic failures are retained and explicitly superseded in evidence/VERIFICATION.md. Final camera reset and screenshot use successful bounded Gazebo CLI services; no world-control service was called.

Maintained files: src/, scripts/, tests/, .vscode/, docs/, references/, decisions/, tutorial/{tutorial.tex,chapters.tex,listings.tex,assets/campus-gazebo.png,tutorial.pdf}. Build/install/log/.runtime and tutorial/qa* are disposable and excluded from the archive. The available session Tectonic executable/cache is not required at runtime; documentation rebuild supports a normal installed LaTeX toolchain.

## Processes and approvals

No task-owned Gazebo, ROS bridge, launcher or verifier remains running; final-process-check.json confirms the host check. No cleanup command is needed at handoff.

NOT VERIFIED: fresh operating-system provisioning, older user-reported Gazebo 8.11.0 / ros_gz 1.0.22, container deployment, interactive VS Code UI, final alternative overview rendering, software-only/EGL rendering. Exact local procedures are documented. These limits do not invalidate the tested native hardware-rendered delivery.

Further physics, UAV dynamics, flight, algorithms, trajectories, safety certification and numerical campaigns require separate authorization. GitHub publication also requires explicit user approval. Do not alter the scientific baseline. On future resume, read this checkpoint first, verify archive/source hashes and preserve intervening edits; rebuild only components actually missing or changed. No automatic continuation or persistent cache is promised.
