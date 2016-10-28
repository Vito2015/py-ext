#!/usr/bin/env python
# coding: utf-8
"""
    multiprocessTask.py
    ~~~~~~~~~~~~~~~~~~~
    a multiprocess model of producer/consumer

    task = Task(work_func, 1, 3, counter=0, a='', callback=cb)
    results = task.run()
    for i in xrange(26):
        lines = ["%d" % i] * random.randint(10, 20)
        task.put(lines)

    task.finish()

"""
import os
import time
from multiprocessing import Pool as ProcessPool, Manager, cpu_count

__all__ = ['Producer', 'Consumer', 'Task']


class Callable(object):

    def __call__(self, *args, **kwargs):
        raise NotImplementedError('%s not callable' % self)

    def run(self, *args, **kwargs):
        raise NotImplementedError('%s.run() not implemented' % self)


class Producer(Callable):
    def __init__(self, todo_list=None, max_qsize=None):
        manager = Manager()
        self._q = manager.Queue()
        self._q_lock = manager.Lock()
        self._q_close_event = manager.Event()
        self._max_qsize = max_qsize or 0
        todo_list = todo_list or []
        if isinstance(todo_list, (list, tuple)) and len(todo_list) > 0:
            self.put(todo_list)
        super(Producer, self).__init__()

    @property
    def q_size(self):
        return self._q.qsize()

    def __call__(self, q, lock, close_event, *args, **kwargs):
        for i, data in enumerate(self.run()):
            with lock:
                q.put(data)
                print 'pid %s put %d: %s' % (os.getpid(), i, data)

    def run(self):
        while 1:
            with self._q_lock:
                if self._q.empty():
                    if self._q_close_event.is_set():
                        break
                    else:
                        time.sleep(0.01)
                        continue
                yield self._q.get()

    def put(self, *todos):
        for todo in todos:
            with self._q_lock:
                self._q.put(todo)

    def finish(self):
        try:
            self._q_close_event.set()
        except Exception as e:
            print e


class Consumer(Callable):
    def __init__(self, fn=None):
        self._fn = fn
        self.results = []
        super(Consumer, self).__init__()

    def __call__(self, q, lock, close_event, *args, **kwargs):
        while 1:
            with lock:
                if q.empty():
                    if close_event.is_set():
                        break
                    else:
                        time.sleep(0.01)
                        continue
                data = q.get()
            self.results.append(self.run(data, *args, **kwargs))
        return self.results

    def run(self, data, *args, **kwargs):
        if self._fn:
            return self._fn(data, *args, **kwargs)


class Task(object):
    """
    a multiprocess model of producer/consumer
    """

    def __init__(self, fn,
                 producer_count=None,
                 consumer_count=None,
                 callback=None,
                 batch=True,
                 counter=None,
                 **shared
                 ):
        """
        init producer/consumer task
        Args:
            fn: consumer called func(data, counter, q_size, *args, **shared_vars)
            producer_count: producer process count, default: 1
            consumer_count: consumer process count, default: cpu_count - 1
            callback: callback func after f calling completed
            batch: if True, `task.put(todo_list)` 'todo_list' will be do all at once in batches;
                    False, todo_list will be do one by one
            counter: process shared counter, need custom imp in <fn>
            **shared: process shared object data
        """
        cpus = cpu_count()
        if producer_count is None or producer_count < 1 or producer_count > cpu_count():
            producer_count = 1
        if consumer_count is None or consumer_count < 1 or consumer_count > cpu_count():
            consumer_count = cpus - 1

        print 'producer_count=%s consumer_count=%s' % (producer_count, consumer_count)

        self._callback = callback
        self.batch = batch
        manager = Manager()
        self.q = manager.Queue()
        self.lock = manager.Lock()
        self.event = manager.Event()
        self._counter = manager.Value('counter', counter or 0)
        self._shared = {var_name: manager.Value(var_name, var_value) for var_name, var_value in shared.iteritems()}
        self.producerProcessList = [Producer() for _ in xrange(producer_count)]
        self.consumerProcessList = [Consumer(fn=fn) for _ in xrange(consumer_count)]
        self.pool = ProcessPool(consumer_count + producer_count)

    @property
    def q_size(self):
        return self.q.qsize() + sum([x.q_size or 0 for x in self.producerProcessList])

    @property
    def counter(self):
        return self._counter.value

    @property
    def shared(self):
        return {var_name: var_value_proxy.value for var_name, var_value_proxy in self._shared.iteritems()}

    def put(self, todo_list):
        producer = self.producerProcessList.pop(0)
        if self.batch:
            producer.put(todo_list)
        else:
            producer.put(*todo_list)
        self.producerProcessList.append(producer)
        time.sleep(0.01)

    def run(self, *args, **kwargs):
        results = []
        arg = (self.q, self.lock, self.event, self._counter, self.q_size)
        kwargs.update(self._shared)
        for producer in self.producerProcessList:
            self.pool.apply_async(producer, arg + args, kwargs)
        for consumer in self.consumerProcessList:
            results.append(self.pool.apply_async(consumer, arg + args, kwargs, self._cb))
        return results

    def _cb(self, *args, **kwargs):
        if self._callback:
            self._callback(self.counter, self._shared)

    def finish(self):
        for producer in self.producerProcessList:
            producer.finish()

        self.pool.close()
        time.sleep(0.03)
        self.event.set()
        self.pool.join()


# def work(data, counter, *args, **kwargs):
#     pid = os.getpid()
#     print '%s doing %s' % (pid, data)
#     # counter = args[0] if len(args) > 0 else None
#     if counter:
#         counter.value += 1
#     kwargs['var_a'].value += chr(len(kwargs['var_a'].value) + 65)
#     return '%s result' % pid
#
#
# def cb(*args, **kwargs):
#     print 'callback', args, kwargs
#
#
# def test():
#     import random
#     n = 0
#     task = Task(work, 1, 3, counter=n, var_a='', callback=cb)
#     results = task.run()
#     for i in xrange(26):
#         lines = ["%d" % i] * random.randint(10, 20)
#         task.put(lines)
#
#     task.finish()
#
#     print 'end counter', task.counter
#     print 'shared.var_a', task.shared['var_a']
#     print 'results:\n' + '\n'.join([str(res.get()) for res in results])
#
# if __name__ == '__main__':
#     test()
