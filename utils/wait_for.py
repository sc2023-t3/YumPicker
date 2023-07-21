import asyncio


class KeyNotExistsError(Exception):
    pass


class Key:
    def __init__(self, identifier: str):
        self.identifier: str = identifier
        self.released: bool = False

    def release(self) -> None:
        self.released = True


class Waiter:
    def __init__(self):
        self.keys: dict[str, Key] = {}

    async def wait_for(self, key_name: str) -> None:
        key = Key(key_name)

        self.keys[key_name] = key

        while True:
            await asyncio.sleep(0.01)

            if not key.released:
                continue

            del self.keys[key_name]
            break

    async def release(self, key_name: str, raise_if_not_exists: bool = False) -> None:
        try:
            self.keys[key_name].release()
        except KeyError as error:
            if not raise_if_not_exists:
                return

            raise KeyNotExistsError(f"Key {key_name} does not exist.") from error
