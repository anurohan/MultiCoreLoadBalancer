# Multi-Core Load Balancer

A small Python desktop simulator that demonstrates how generated processes can be distributed across CPU cores. The Tkinter interface displays per-core load while the simulation runs and reports throughput, average waiting time, and average turnaround time.

## What it demonstrates

- Generation of sample processes with arrival times, burst durations, and priorities.
- Assignment of work to the currently least-loaded core.
- Step-by-step simulation with start and stop controls.
- Per-core activity/load display and summary scheduling metrics.
- A simple desktop GUI built with Python's Tkinter toolkit.

This is an educational simulator; it models scheduling behavior and is not a control plane for real CPU cores or operating-system processes.

## Requirements

- Python 3 with Tkinter available.
- No third-party Python packages are imported by `multi_core_scheduler.py`.

On Windows, install Python with its Tcl/Tk support enabled. On Linux, install the distribution's Tkinter package if it is not already present.

## Run

From the repository root:

```sh
python multi_core_scheduler.py
```

A desktop window should open. Use **Generate & Start Simulation** to create sample work and start the animation, and **Stop Simulation** to halt it.

## Project files

- `multi_core_scheduler.py` — process model, scheduling loop, metrics, and Tkinter interface.
- `MultiCoreLoadBalancer_Report.pdf` — accompanying project report.

## Limitations

Processes and their timings are generated in memory for demonstration. The program does not schedule real system processes, persist runs, or compare against a production operating-system scheduler.