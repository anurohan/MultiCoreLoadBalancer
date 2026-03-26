import tkinter as tk
from tkinter import ttk
import random
import time
import threading
from collections import deque

# Process Class
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.start_time = -1
        self.completion_time = -1

# Scheduler Class
class MultiCoreScheduler:
    def __init__(self, num_cores=4):
        self.num_cores = num_cores
        self.cores = [None] * num_cores          # Current process on each core
        self.core_load = [0] * num_cores         # Load percentage (0-100)
        self.processes = []                      # All processes
        self.completed = []                      # Completed processes
        self.time = 0
        self.process_queue = deque()

    def generate_processes(self, num=60):
        """Generate random processes"""
        for i in range(num):
            arrival = random.randint(0, 25)
            burst = random.randint(4, 18)
            priority = random.randint(1, 5)
            p = Process(i + 1, arrival, burst, priority)
            self.processes.append(p)
        self.processes.sort(key=lambda x: x.arrival_time)

    def get_least_loaded_core(self):
        """Dynamic Load Balancing - assign to least loaded core"""
        min_load = min(self.core_load)
        return self.core_load.index(min_load)

    def simulate_step(self):
        # Add new arrived processes to ready queue
        for p in self.processes[:]:
            if p.arrival_time <= self.time:
                self.process_queue.append(p)
                self.processes.remove(p)

        # Assign processes to cores using load balancing
        for i in range(self.num_cores):
            if self.cores[i] is None and self.process_queue:
                core_idx = self.get_least_loaded_core()
                p = self.process_queue.popleft()
                self.cores[core_idx] = p
                p.start_time = self.time
                self.core_load[core_idx] = random.randint(65, 95)   # Simulate load

        # Run 1 time unit on each core
        for i in range(self.num_cores):
            if self.cores[i]:
                self.cores[i].remaining_time -= 1
                # If process finished
                if self.cores[i].remaining_time <= 0:
                    self.cores[i].completion_time = self.time + 1
                    self.completed.append(self.cores[i])
                    self.cores[i] = None
                    self.core_load[i] = 0

        self.time += 1

    def calculate_metrics(self):
        if not self.completed:
            return 0.0, 0.0, 0.0
        total_completed = len(self.completed)
        avg_waiting = sum((p.completion_time - p.arrival_time - p.burst_time) 
                         for p in self.completed) / total_completed
        avg_turnaround = sum((p.completion_time - p.arrival_time) 
                            for p in self.completed) / total_completed
        throughput = total_completed / self.time if self.time > 0 else 0
        return round(throughput, 2), round(avg_waiting, 2), round(avg_turnaround, 2)

# GUI Class
class SchedulerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Multi-Core Load Balancing Scheduler")
        self.root.geometry("900x700")
        self.scheduler = MultiCoreScheduler(num_cores=4)
        self.running = False
        self.thread = None
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="Multi-Core Load Balancing Scheduler", 
                 font=("Arial", 18, "bold")).pack(pady=10)

        # Core Status
        self.core_frame = tk.Frame(self.root)
        self.core_frame.pack(pady=10)
        self.core_labels = []
        for i in range(4):
            lbl = tk.Label(self.core_frame, text=f"Core {i+1}: Idle (0%)", 
                           font=("Arial", 12), width=35, height=2, 
                           relief="ridge", bg="#f0f0f0")
            lbl.grid(row=i//2, column=i%2, padx=15, pady=8)
            self.core_labels.append(lbl)

        # Metrics
        self.metrics_frame = tk.Frame(self.root)
        self.metrics_frame.pack(pady=15)
        self.tp_label = tk.Label(self.metrics_frame, text="Throughput: 0.00", 
                                 font=("Arial", 13))
        self.tp_label.pack()
        self.wait_label = tk.Label(self.metrics_frame, text="Avg Waiting Time: 0.00", 
                                   font=("Arial", 13))
        self.wait_label.pack()
        self.turn_label = tk.Label(self.metrics_frame, text="Avg Turnaround Time: 0.00", 
                                   font=("Arial", 13))
        self.turn_label.pack()

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="🚀 Generate & Start Simulation", 
                  command=self.start_simulation, bg="#28a745", fg="white", 
                  font=("Arial", 12, "bold"), width=25).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="⛔ Stop Simulation", 
                  command=self.stop_simulation, bg="#dc3545", fg="white", 
                  font=("Arial", 12, "bold"), width=20).pack(side=tk.LEFT, padx=10)

        self.status = tk.Label(self.root, text="Ready - Press Start", fg="blue", 
                               font=("Arial", 12))
        self.status.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_gui(self):
        while self.running:
            self.scheduler.simulate_step()
            
            # Update core status
            for i in range(self.scheduler.num_cores):
                if self.scheduler.cores[i]:
                    p = self.scheduler.cores[i]
                    text = f"Core {i+1}: P{p.pid} ({p.remaining_time}s) - {self.scheduler.core_load[i]}%"
                    color = "#ffeb3b"
                else:
                    text = f"Core {i+1}: Idle (0%)"
                    color = "#f0f0f0"
                self.core_labels[i].config(text=text, bg=color)

            # Update metrics
            tp, aw, at = self.scheduler.calculate_metrics()
            self.tp_label.config(text=f"Throughput: {tp} processes/unit time")
            self.wait_label.config(text=f"Avg Waiting Time: {aw}")
            self.turn_label.config(text=f"Avg Turnaround Time: {at}")

            self.root.update()
            time.sleep(0.6)   # Live feel

    def start_simulation(self):
        if not self.running:
            self.scheduler = MultiCoreScheduler(num_cores=4)
            self.scheduler.generate_processes(60)
            self.running = True
            self.status.config(text="Simulation Running...", fg="green")
            self.thread = threading.Thread(target=self.update_gui, daemon=True)
            self.thread.start()

    def stop_simulation(self):
        self.running = False
        self.status.config(text="Simulation Stopped", fg="red")

    def on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    app = SchedulerGUI()
    app.root.mainloop()