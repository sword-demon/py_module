from concurrent.futures import ThreadPoolExecutor


class MyThreadPool:

    def __init__(self, max_thread_num):
        self.max_thread_num = max_thread_num
        self.pool = None
        self.create_pool()

    def create_pool(self):
        """
        创建一个线程池
        :param i: 线程数
        :return:
        """
        print("创建了一个有{}条线程的线程池!".format(self.max_thread_num))
        self.pool = ThreadPoolExecutor(self.max_thread_num)

    def close_pool(self):
        """
        关闭线程池
        :param pool: 线程池对象
        :return:
        """
        self.pool.shutdown()
        print("线程池已释放!")

    def task_callback(self, result_response):
        """
        执行回调
        :param result_response:
        :return:
        """
        ret_dic = result_response.result()

    def create_task(self, task, *args, **kwargs):
        self.pool.submit(task, *args, **kwargs)
