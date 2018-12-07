"""
Author: TRsky
Time: 2018-11-07
Title: Operation System Process Scheduling Simulation
File: Main Control
"""
from process import Process
from algo import AlgoClass
import random

procs = []  # 进程队列
time = 0  # 时间片


# 初始化进程队列
def make_procs():
    global procs
    # 测试数据
    # proc1 = Process(1, 0, 3, random.randint(2, 9))
    # proc2 = Process(2, 2, 6, random.randint(2, 9))
    # proc3 = Process(3, 4, 4, random.randint(2, 9))
    # proc4 = Process(4, 6, 5, random.randint(2, 9))
    # proc5 = Process(5, 8, 2, random.randint(2, 9))
    # procs.append(proc1)
    # procs.append(proc2)
    # procs.append(proc3)
    # procs.append(proc4)
    # procs.append(proc5)
    # pid, at, pt, pri
    procs = [Process(i, random.randint(0, 15), random.randint(3, 15), random.randint(1, 15)) for i in range(10)]


# 调用调度算法
def run_algo(algo):
    global time   # 0 时间刻
    print("Beginning a run of %s" % algo.name)  # 输出调度算法名称
    while not algo.all_done():  # 进程未全部调度未完成，则继续执行进程
        algo.schedule()
    time = 0  # 初始化时间点

if __name__ == '__main__':
    make_procs()
    # 启动进程
    # 最短剩余时间优先(抢占式)
    algo_srt = AlgoClass("SRT", procs, time)
    # 最短任务优先(不可抢占)
    algo_spn = AlgoClass("SPN", procs, time)
    # 优先级调度(抢占式)， 优先数小，优先级高
    algo_pri = AlgoClass("PRI", procs, time)
    # 时间片为 1 的轮转调度
    algo_rr = AlgoClass("RR", procs, time)

    # 执行调度算法
    run_algo(algo_srt)
    run_algo(algo_spn)
    run_algo(algo_pri)
    run_algo(algo_rr)

    print("\nOverall Stats:\n")
    print("\nShortest Remaining Time First(SRT):")
    algo_srt.output_end_proc()
    print("\nShortest Process Next(SPN):")
    algo_spn.output_end_proc()
    print("\nPriority Scheduling(PRI):")
    algo_pri.output_end_proc()
    print("\nRound Robin(RR):")
    algo_rr.output_end_proc()


