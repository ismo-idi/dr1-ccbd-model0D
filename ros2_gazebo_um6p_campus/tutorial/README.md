# Tutorial index

1. **01_UM6P_Campus_Environment_Setup_and_Coding.pdf** — beginner guide to the parked campus, assumptions, setup, assets, integration and paused checks. Exact source: source/campus_environment/.
2. **02_Two_UAV_Kinematic_Demos_Coding_and_Verification.pdf** — deterministic motion, yielding, static-sphere bypass, counter implementation, tests and manual recording. Exact source: source/kinematic_demos/.

Both appendices import the delivered source files directly. All required figures are under each source/assets directory. Build from the delivery root after installing the optional documented TeX tools:

```bash
bash scripts/build_tutorials.sh
```

Expected result: both named PDFs in this directory. `build_tutorial.sh` and `build_kinematic_tutorial.sh` remain aliases for one guide each. Tectonic may download TeX dependencies at documentation-build time; this is separate from scene runtime. Compilation alone is not visual verification; the delivered PDF QA record lists final page inspection. Do not distribute only a .tex file without the full delivery: its appendix imports project source by relative path.
