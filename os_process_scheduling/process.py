"""
Author: TRsky
Time: 2018-11-07
Title: Operation System Process Scheduling Simulation
File: Process Class
"""


# 进程类
class Process(object):
    """
    :param pid: 进程标志符
    :param at: 进程到达时间
    :param pt: 进程需求时间
    :param pri: 进程优先级
    """
    def __init__(self, pid, at, pt, pri):
        self.pid = pid  # 进程标志符
        self.start_time = 0  # 进程开始时间
        self.arrive_time = at  # 进程到达时间
        self.req_time = pt  # 进程运行时间
        self.priority = pri  # 进程优先级
        self.end_time = 0  # 进程结束时间
        self.run_time = 0  # 进程总运行时间
        self.total_wait = 0  # 总等待时间
        self.turnaround = 0  # 周转时间
        self.status = 'Terminated'  # 进程状态

    def __str__(self):
        return self.pid

    # 判断进程是否结束
    def is_done(self):
        # 程序执行时间大于需求时间
        return self.run_time >= self.req_time

    # 进程调度时间
    def run(self, runtime):
        self.run_time += runtime
