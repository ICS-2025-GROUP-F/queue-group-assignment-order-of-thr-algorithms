# =================================================================
# MODULE 5: EVENT SIMULATION & TIME MANAGEMENT
# Student: [Tracyy Ohowa]
# =================================================================

def tick(self):
    
    self.current_time += 1
    
    print(f"\n--- TICK {self.current_time} ---")
    
    # Update waiting times for all jobs
    self._update_waiting_times()
    
    # Apply time-based updates (aging and expiry)
    self._apply_time_based_updates()
    
    # Show status after tick
    self.show_status()

def _update_waiting_times(self):
    
    if self.size == 0:
        return
        
    current_index = self.front
    for i in range(self.size):
        job = self.queue[current_index]
        if job is not None:
            job['waiting_time'] += 1
        current_index = (current_index + 1) % self.capacity

def _apply_time_based_updates(self):
    """
    Apply time-based updates including:
    1. Priority aging
    2. Job expiry
    """
    # Apply priority aging
    self._apply_priority_aging()
    
    # Remove expired jobs
    self._remove_expired_jobs()

def _apply_priority_aging(self):
    
    if self.size == 0:
        return
        
    aging_interval = getattr(self, 'aging_interval', 5)  # Default 5 ticks
    aged_jobs = []
    current_index = self.front
    
    for i in range(self.size):
        job = self.queue[current_index]
        if job is not None:
            # Check if job should age (every aging_interval ticks)
            if job['waiting_time'] > 0 and job['waiting_time'] % aging_interval == 0:
                if job['priority'] < 10:  # Max priority is 10
                    job['priority'] += 1
                    aged_jobs.append(job['job_id'])
                    print(f"🔄 Job {job['job_id']} priority increased to {job['priority']} (aged)")
        
        current_index = (current_index + 1) % self.capacity
    
    # Re-sort queue if any jobs were aged
    if aged_jobs:
        self._reorder_queue_by_priority()

def _remove_expired_jobs(self):
    """
    Remove jobs that have exceeded the expiry time.
    Default expiry_time = 30 ticks.
    """
    if self.size == 0:
        return
        
    expiry_time = getattr(self, 'expiry_time', 30)  # Default 30 ticks
    expired_jobs = []
    current_index = self.front
    
    # Find expired jobs
    for i in range(self.size):
        job = self.queue[current_index]
        if job is not None and job['waiting_time'] >= expiry_time:
            expired_jobs.append(job)
        current_index = (current_index + 1) % self.capacity
    
    # Remove expired jobs
    for job in expired_jobs:
        self._remove_job_by_id(job['job_id'])
        print(f"⚠️  Job {job['job_id']} from user {job['user_id']} EXPIRED after {job['waiting_time']} ticks")

def get_current_time(self):
    """
    Get the current system time.
    
    Returns:
        int: Current system time in ticks
    """
    return getattr(self, 'current_time', 0)

def get_system_stats(self):
    """
    Get system statistics related to time management.
    
    Returns:
        dict: Time-related system statistics
    """
    if not hasattr(self, 'current_time'):
        self.current_time = 0
        
    stats = {
        'current_time': self.current_time,
        'queue_size': self.size,
        'average_wait_time': self._calculate_average_wait_time()
    }
    return stats

# =================================================================
# HELPER METHODS FOR MODULE 5
# =================================================================

def _calculate_average_wait_time(self):
    """
    Calculate average waiting time of jobs currently in queue.
    
    Returns:
        float: Average waiting time
    """
    if self.size == 0:
        return 0.0
        
    total_wait = 0
    current_index = self.front
    
    for i in range(self.size):
        job = self.queue[current_index]
        if job is not None:
            total_wait += job['waiting_time']
        current_index = (current_index + 1) % self.capacity
    
    return total_wait / self.size

def _reorder_queue_by_priority(self):
    """
    Reorder the queue based on priority after aging.
    Higher priority jobs move to front.
    """
    if self.size <= 1:
        return
        
    # Extract all jobs
    jobs = []
    current_index = self.front
    for i in range(self.size):
        if self.queue[current_index] is not None:
            jobs.append(self.queue[current_index])
        current_index = (current_index + 1) % self.capacity
    
    # Sort by priority (descending) then by waiting time (ascending)
    jobs.sort(key=lambda x: (-x['priority'], x['waiting_time']))
    
    # Clear queue and re-add sorted jobs
    self._clear_queue_and_rebuild(jobs)

def _remove_job_by_id(self, job_id):
    """
    Remove a specific job from the queue by job ID.
    
    Args:
        job_id (str): ID of job to remove
    """
    if self.size == 0:
        return False
        
    current_index = self.front
    for i in range(self.size):
        job = self.queue[current_index]
        if job is not None and job['job_id'] == job_id:
            # Shift all subsequent jobs forward
            for j in range(i, self.size - 1):
                next_index = (self.front + j + 1) % self.capacity
                current_pos = (self.front + j) % self.capacity
                self.queue[current_pos] = self.queue[next_index]
            
            # Clear the last position
            last_pos = (self.front + self.size - 1) % self.capacity
            self.queue[last_pos] = None
            self.size -= 1
            self.rear = (self.rear - 1) % self.capacity
            return True
            
        current_index = (current_index + 1) % self.capacity
    
    return False

def _clear_queue_and_rebuild(self, jobs):
    
    # Clear the queue
    for i in range(self.capacity):
        self.queue[i] = None
    
    self.front = 0
    self.rear = 0
    self.size = 0
    
    # Add jobs back
    for job in jobs:
        if self.size < self.capacity:
            self.queue[self.rear] = job
            self.rear = (self.rear + 1) % self.capacity
            self.size += 1