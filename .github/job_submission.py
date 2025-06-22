import threading
import time
from collections import deque


class PrintQueueManager:
    def __init__(self, max_capacity=10):
        self.queue = deque(maxlen=max_capacity)
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.job_id_counter = 0
        self.max_capacity = max_capacity

    def enqueue_job(self, user_id, priority):
        with self.lock:
            while len(self.queue) >= self.max_capacity:
                self.condition.wait()

            self.job_id_counter += 1
            job_id = self.job_id_counter

            job = {
                'user_id': user_id,
                'job_id': job_id,
                'priority': priority,
                'waiting_time': 0,
                'submission_time': time.time()
            }

            self.queue.append(job)
            print(f"Job {job_id} from user {user_id} enqueued with priority {priority}")
            self.condition.notify_all()
            return job_id

    def handle_simultaneous_submissions(self, jobs_list):
        results = []
        threads = []

        for user_id, priority in jobs_list:
            thread = threading.Thread(
                target=lambda u, p: results.append(self.enqueue_job(u, p)),
                args=(user_id, priority)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results