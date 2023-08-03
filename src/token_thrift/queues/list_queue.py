from .abstract_queue import AbstractQueue, PendingRequest

class ListQueue(AbstractQueue):
    def __init__(self):
        self.queue = []

    def enqueue(self, pending_request):
        pending_request.id = len(self.queue)
        self.queue.append(pending_request)

    def dequeue(self) -> PendingRequest:
        return self.queue.pop(0)
    
    def is_empty(self) -> bool:
        return self.queue == []
