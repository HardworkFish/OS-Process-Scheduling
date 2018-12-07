"""
Author: TRsky
Time: 2018-11-07
Title: Operation System Process Scheduling Simulation
File: algorithm implement
"""

import copy


# 调度算法
class AlgoClass(object):
    """
    :param name:调度算法名称
    :param proc_list:进程列表
    :param rtime:运行时间
    """
    def __init__(self, name, proc_list, rtime):
        self.name = name
        self.pre_procs = copy.deepcopy(proc_list)  # 进程队列
        self.rtime = rtime  # 时间片
        self.in_mem_procs = []  # 就绪队列
        self.current_proc = None
        self.end_pros = []  # 结束队列
        self.flag = False

    # 对进入 CPU 内的队列进行排序处理
    def organize_procs(self):
        if self.name == "SRT" or self.name == "SPN":
            # 最短剩余时间优先(抢占式）| 最短作业优先(非抢占式)
            self.in_mem_procs = sorted(self.in_mem_procs, key=lambda process: process.req_time - process.run_time)
        elif self.name == "PRI":
            # 优先数调用(抢占式)
            self.in_mem_procs = sorted(self.in_mem_procs, key=lambda process: (process.priority, process.start_time))
            self.in_mem_procs[0].priority += 1  # 进程被调度， 优先数 +1
        elif self.name == "RR":
            # 时间片轮转，按进入就绪队列的到达顺序
            return

    def context_switch(self, next_proc):
        if self.current_proc.is_done():
            self.output(["finished", self.current_proc])
            self.current_proc.end_time = self.rtime
            self.current_proc.status = 'Terminated'  # 进程处在终止状态
            self.end_pros.append(self.current_proc)
        # 进程切换
        self.output(["cs", self.current_proc, next_proc])
        self.current_proc.status = 'Waiting'  # 当前进程处在等待状态
        self.current_proc = next_proc
        self.current_proc.status = 'Running'  # 进程处在运行状态

    def check_switch(self):
        if len(self.in_mem_procs) > 0:
            if self.current_proc.is_done():
                if len(self.in_mem_procs) > 1:
                    self.in_mem_procs.remove(self.current_proc)
                    self.context_switch(self.in_mem_procs[0])
                else:
                    self.output(["finished", self.current_proc])
                    self.in_mem_procs[0].status = 'Terminated'  # 进程处在终止状态
                    self.in_mem_procs[0].end_time = self.rtime
                    self.end_pros.append(self.in_mem_procs[0])
                    self.in_mem_procs.remove(self.in_mem_procs[0])
            # 最短剩余时间优先，抢占， 任务未完成切换
            elif self.name == "SRT" or self.name == "PRI":
                if self.current_proc != self.in_mem_procs[0]:
                    self.context_switch(self.in_mem_procs[0])
            # 最短作业优先， 非抢占，任务未完成不切换
            elif self.name == "SPN":
                return
            # 轮转调度(抢占式)
            elif self.name == "RR":
                if len(self.in_mem_procs) > 1:
                    self.context_switch(self.in_mem_procs[1])
                    # 进行轮转
                    temp_proc = self.in_mem_procs[0]
                    self.in_mem_procs.remove(self.in_mem_procs[0])
                    self.in_mem_procs.append(temp_proc)
            else:
                print("Error! Invalid algorithm\n choices are SRT SPN PRI RR\n")

    def output(self, args):
        if args[0] == 'created':
            proc = args[1]
            print("[time: %dms] Process %d created (requiring %dms CPU time))"
                  % (self.rtime, proc.pid, proc.req_time))
        elif args[0] == "started":
            proc = args[1]
            print("[time: %dms] Process %d accessed CPU for the first time (initial wait time %dms)"
                  % (self.rtime, proc.pid, (self.rtime - proc.arrive_time)))
        # 进程切换
        elif args[0] == "cs":
            proc1 = args[1]
            proc2 = args[2]
            print("[time: %dms] Context switch (swapped out process %d for process %d)"
                  % (self.rtime, proc1.pid, proc2.pid))
        # 进程调度完成
        elif args[0] == "finished":
            proc = args[1]
            print("[time: %dms] Process %d terminated (turnaround time %dms, total wait time %dms)"
                  % (self.rtime, proc.pid, (self.rtime - proc.arrive_time),
                     (self.rtime - proc.arrive_time - proc.req_time)))
            # 计算等待时间
            self.current_proc.total_wait = self.rtime - self.current_proc.arrive_time - self.current_proc.req_time
            # 计算周转时间
            self.current_proc.turnaround = self.rtime - self.current_proc.arrive_time
        elif args[0] == "running":
            proc = args[1]
            print("[time: %dms] Process %d is running now.Current process's priority is %d and "
                  "still remains %d ms time)"
                  % (self.rtime, proc.pid, proc.priority, proc.req_time - proc.run_time))

    # 进行进程调度
    def run(self):
        if len(self.in_mem_procs) > 0:
            if self.current_proc.run_time == 0:
                self.output(["started", self.current_proc])  # 进程开始运行
                self.current_proc.start_time = self.rtime
            if not self.current_proc.is_done():
                self.output(["running", self.current_proc])
                self.current_proc.run(1)

    def all_done(self):
        max_end_time = max([(x.start_time + x.req_time) for x in self.pre_procs])
        return self.rtime >= max_end_time and len(self.in_mem_procs) == 0

    def output_end_proc(self):
        print("          %5s    %5s     %5s      %5s    %5s    %5s      %5s     %5s      %5s " %
              ("Process",  "Arrived Time", "Run Time", "Priority", "Started Time", "End Time", "Waited Time",
               "Turnaround", "Turnaround & Weight"))
        for proc in self.end_pros:
            print("Process:     %2d      %5.1f ms       %5.1f ms       %2d           %5.1f ms       %5.1f ms "
                  "     %5.1f ms       %5.1f ms         %5.1f ms"
                  % (proc.pid, proc.arrive_time, proc.req_time, proc.priority, proc.start_time, proc.end_time,
                     proc.total_wait, proc.turnaround, proc.turnaround/proc.req_time))

    # 进程调度
    def schedule(self):
        for proc in self.pre_procs:
            if proc.arrive_time == self.rtime:
                self.output(["created", proc])
                proc.statue = 'Reading'  # 进入就绪队列
                self.in_mem_procs.append(proc)
        if len(self.in_mem_procs) > 0:
            if not self.flag:
                self.current_proc = self.in_mem_procs[0]  # 当前进程为进入内存的首个进程
                self.flag = True
        if self.flag and not self.all_done():
            self.organize_procs()
            self.check_switch()
            self.run()
        self.rtime += 1
