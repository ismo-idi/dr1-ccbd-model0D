# User target and execution measurements

User supplied on 14 September 2026: Dell Latitude 5430; i5-1245U (10 physical cores / 12 threads), 16 GiB DDR4, roughly 4 GiB swap, Samsung PM9A1 512 GB NVMe; Ubuntu 24.04.4 Noble amd64; kernel 7.0.0-31; Wayland with XWayland; Iris Xe 8086:46a8 / i915 / Mesa25.2.8 / OpenGL4.6. Earlier ROS/Gazebo observations: Jazzy desktop via apt, Gazebo8.11.0, ros_gz1.0.22-1noble.20260412.072535. May31 Ogre log is historical, not a live measurement.

Current task tool execution observed Ubuntu24.04.5 x86_64; same kernel family; Gazebo8.15.0; ros_gz1.0.24; live GLX probe outside sandbox: IrisXe ADL GT2, Mesa25.2.8, direct rendering, OpenGL4.6. About125GiB free at initial check. The session used the existing installation and did not upgrade it. Do not infer a new installation date or a user-performed upgrade from this discrepancy.

Sandbox could not resolve GitHub or access display/network interfaces. Authorized read-only/network/rendering operations outside it succeeded; private Git clone still lacked terminal authentication. The connected GitHub tool supplied pinned repository text instead. No host graphics settings, container privileges, apt sources or security settings were modified.

Local future verification: run the delivered environment check, then bounded headless and GUI tests. A future terminal session or a different machine may report different packages. Interactive VS Code task UI, the older package pair, and clean-OS provisioning were not executed.
