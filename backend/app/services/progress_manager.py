

# # ================================
# # backend/app/services/progress_manager.py
# # ================================
# import asyncio
# from collections import defaultdict




# class ProgressManager:
#     """In-memory pub/sub for SSE"""


#     def __init__(self):
#         self.subscribers = defaultdict(list)


#     async def publish(self, project_id: int, data: dict):
#         for queue in self.subscribers[project_id]:
#             await queue.put(data)


#     async def subscribe(self, project_id: int):
#         queue = asyncio.Queue()
#         self.subscribers[project_id].append(queue)
#         return queue




# progress_manager = ProgressManager()

# backend/app/services/progress_manager.py

import asyncio
from typing import Dict, List

class ProgressManager:
    def __init__(self):
        self.subscribers: Dict[int, List[asyncio.Queue]] = {}

    async def subscribe(self, project_id: int):
        queue = asyncio.Queue()
        self.subscribers.setdefault(project_id, []).append(queue)
        return queue

    async def publish(self, project_id: int, message: dict):
        for q in self.subscribers.get(project_id, []):
            await q.put(message)

progress_manager = ProgressManager()
