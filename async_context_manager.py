import asyncio


class AsyncContextManager:

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def __enter__(self):
        return self.loop

    def __exit__(self, exception_type, exception_value, traceback):
        self.loop.close()
