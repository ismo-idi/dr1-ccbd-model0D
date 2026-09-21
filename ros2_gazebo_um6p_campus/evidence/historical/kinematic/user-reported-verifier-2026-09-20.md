# User-reported verifier failure — 20 September 2026

Source: user-supplied terminal screenshot, preserved as user-reported-verifier-2026-09-20.png. This is diagnostic evidence, not presentation media or a new task-executed test.

Observed: `bash scripts/verify_demo.sh 2 gui` terminated with AssertionError at the midflight pause assertion requiring subsequent poses and simulation time to equal the captured hold sample. The screenshot also shows the same assertion for a Wave1 headless verification attempt. It shows failed manual attempts without the `scripts/` path. The user separately reports that manually launched Demo1 runs successfully.

The verifier owns its launch and cleans it up in a finally block. Therefore its test failure explains the test scene closing. It does not establish a clearance violation or a broken manual Wave2 launcher. The root cause of the pause assertion is NOT DIAGNOSED: queued telemetry and other concurrent activity require examination of the actual run data before assigning a cause. The screenshot alone is insufficient.

Immediate user workflow: stop the owning manual launch in Terminal A; from the delivery root run `bash scripts/launch_demo.sh 2 gui` in Terminal A; after loading run `bash scripts/demo_control.sh start` in Terminal B. Do not use verify_demo.sh for manual recording. No rebuild is needed solely to change wave after a successful build.

Changes in this follow-up: README now provides explicit separate commands for both demos, preparation, pause/resume, owner-terminal shutdown, and the distinction between manual launch and automated tests. No code, route, package layout, or original test evidence changed. No simulation or new test executed. No commit or publication performed.

Pending before future publication: diagnose and resolve this user-reported verification failure with retained local trace/result/log evidence. The earlier four successful final tests remain historical observations; they do not invalidate this newer report.
