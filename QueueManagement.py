class PrintQueueManager:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue=[None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def is_full(self):
        return self.size==self.capacity
    
    def is_empty(self):
        return self.size == 0
    
    def enqueue_job(self,user_id,job_id,priority):
        if self.is_full():
            print("Queue is full. Cannot enqueue job.")
            return
        
        self.rear = (self.rear + 1) % self.capacity

        job ={
            "user_id": user_id,
            "job_id": job_id,
            "priority": priority,
            "waiting_time": 0
        }

        self.queue[self.rear] = job 
        self.size += 1
        print(f"Job {job_id} from user {user_id} with priority {priority} added to the queue.")

    def dequeue_job(self):

        if self.is_empty():

            print("Queue is empty. No job to dequeue.")
            return None
        
        job=self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1

        print(f"Job{job['job_id']} dequeued for printing")
        return job
    

    def show_status(self):
        print("Current Queue Status:")
        if self.is_empty():
            print("Queue is empty.")
            return
        
        index= self.front
        count = 0

        while count < self.size:

            job=self.queue[index]
            print(f"[JobID: {job['job_id']} | User: {job['user_id']} | Priority: {job['priority']} | Waiting Time: {job['waiting_time']}]")
            index = (index + 1) % self.capacity
            count += 1
    
    print("------------------------\n")

    def increment_waiting_time(self):
        index=self.front
        count = 0

        while count < self.size:
            if self.queue[index]:
                self.queue[index]['waiting_time'] += 1
            index = (index + 1) % self.capacity
            count += 1


             

          
            

        

