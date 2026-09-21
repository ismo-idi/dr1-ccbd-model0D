# Demo 2 — static sphere bypass and crossing

Work from the **delivery root**, not this subfolder. Build once with `bash scripts/build.sh`.

Terminal A:

```bash
bash scripts/launch_demo.sh 2 gui
```

Wait until Gazebo has loaded; keep Terminal A running. Then, in Terminal B at the same root:

```bash
bash scripts/demo_control.sh start
```

Stop with Ctrl+C in Terminal A. See the root README for pause, replay and troubleshooting. `verify_demo.sh` is an automated test that closes its own scene.

`src/um6p_demo_2/config/routes.txt` owns the two waypoint sequences. `common/scripts/generate_demo_worlds.py` regenerates the installed world input. `tests/expected.json` records expected deterministic milestones. Shared motion and panel code live in `common/`. No physical flight dynamics are modeled.

Your original recording is under `media/videos/`; actual Gazebo screenshots are under `media/screenshots/`. See the media provenance and the scenario verification record.
