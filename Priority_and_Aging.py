from threading import Lock


class PriorityAgingSystem:
    def __init__(self, capacity=10, aging_interval_ticks=3):
        self.queue = [None] * capacity 
        self.capacity = capacity
        self.head = self.tail = self.size = 0
        self.aging_interval = aging_interval_ticks
        self.lock = Lock() 

    def add_job(self, job, current_tick):
     
        with self.lock:
            if self.is_full():
                return False  
            job.update({
                "submission_tick": current_tick,
                "original_priority": job["priority"]
            })
            self.queue[self.tail] = job
            self.tail = (self.tail + 1) % self.capacity
            self.size += 1
            self._sort_queue()
            return True

    def apply_priority_aging(self, current_tick):
      
        with self.lock:
            for i in range(self.size):
                job = self.queue[(self.head + i) % self.capacity]
                if not job: continue
                aging_intervals = (current_tick - job["submission_tick"]) // self.aging_interval
                job["priority"] = max(job["original_priority"] - aging_intervals, 0)
            self._sort_queue()

    def _sort_queue(self):
       
        jobs = [self.queue[(self.head + i) % self.capacity] for i in range(self.size)]
        jobs.sort(key=lambda x: (x["priority"], x["submission_tick"]))
        for i, job in enumerate(jobs):
            self.queue[(self.head + i) % self.capacity] = job

    def is_full(self):
        return self.size == self.capacity

    def get_queue_state(self):
    
        with self.lock:
            return [self.queue[(self.head + i) % self.capacity] for i in range(self.size)]