import sched
import time
from transitions import Machine, State




class MyTimer(object):
    states = [State(name='idle'),        
              State(name='waiting', on_enter=[
                    'action_start_timer', 'action_do_task'], on_exit=['action_stop_timer'])
            ]
    transitions = [
        {'trigger': 'event_begin_task_in_time',
            'source': 'idle', 'dest': 'waiting'},
        {'trigger': 'event_receive_res', 'source': 'waiting', 'dest': 'idle'},
        {'trigger': 'event_time_up', 'source': 'waiting', 'dest': 'idle','after':['action_remove_all_tasks']},
    ]

    def __init__(self,wait_seconds=2):
        self.machine = Machine(
            model=self, states=MyTimer.states, transitions=MyTimer.transitions, initial='idle', send_event=True, ignore_invalid_triggers=True)
        self.wait_seconds=wait_seconds
        self.task_need_to_waited = None
        self.scheduler = sched.scheduler(time.time, time.sleep)
    

    def action_start_timer(self, event):
        print('启动定时器.')
        self.scheduler.enter(self.wait_seconds, 1, self.event_time_up)
        self.scheduler.run()
        
    def action_stop_timer(self,event):
        print('停止定时器.')
    
    def action_do_task(self, event):
        self.task_need_to_waited = event.kwargs.get('task', 0)
        print(type(self.task_need_to_waited))
        print('执行任务.')
        self.task_need_to_waited()
    
    def action_remove_all_tasks(self,event):
        print('清除剩余task.')
    


def create_task(para):
    def task():
        print(f'任务 {para} 开始.')
        #print(f'任务 {para} 结束.')
    return task


def main():
    print("hello world")
    mytimer = MyTimer()

    #创建任务
    task1 = create_task(1)
    mytimer.event_begin_task_in_time(task=task1)
    #任务结束
    mytimer.event_receive_res()
    print(mytimer)



if __name__ == "__main__":
    main()
