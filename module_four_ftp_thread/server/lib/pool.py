from threading import Thread
import queue


class MyThreadPool:

    def __init__(self, max_thread_num):
        self.max_thread_num = max_thread_num
        self.pool = None
        self.q = queue.Queue(self.max_thread_num)
        self.create_pool()

    def create_pool(self):
        """
        创建一个线程池
        :param i: 线程数
        :return:
        """
        print("创建了一个有{}条线程的线程池!".format(self.max_thread_num))
        # 在队列中存放max_thread_num个对象，起到线程池的作用
        for i in range(self.max_thread_num):
            self.q.put(Thread)

    def get_thread(self):
        """取出一条线程"""
        return self.q.get()

    def is_empty(self):
        """队列是否为空"""
        if not self.q.empty():
            return True
