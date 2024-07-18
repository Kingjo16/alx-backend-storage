#!/usr/bin/env python3
"""
A module for using the Redis NoSQL data storage.
"""
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    """
    Tracks the number of calls made to a method in a Cache class.

    Args:
        method (Callable): The method to be tracked.

    Returns:
        Callable: The wrapped method with call count tracking.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Invokes the given method after incrementing its call counter.

        Args:
            self: The instance of the Cache class.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            Any: The result of the method call.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Tracks the call details of a method in a Cache class.

    Args:
        method (Callable): The method to be tracked.

    Returns:
        Callable: The wrapped method with call detail tracking.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Returns the method's output after storing its inputs and output.

        Args:
            self: The instance of the Cache class.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            Any: The result of the method call.
        """
        input_key = f'{method.__qualname__}:inputs'
        output_key = f'{method.__qualname__}:outputs'
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """
    Displays the call history of a Cache class' method.

    Args:
        method (Callable): The method whose history is to be displayed.
    """
    if method is None or not hasattr(method, '__self__'):
        return
    redis_store = getattr(method.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    method_name = method.__qualname__
    input_key = f'{method_name}:inputs'
    output_key = f'{method_name}:outputs'
    call_count = 0
    if redis_store.exists(method_name) != 0:
        call_count = int(redis_store.get(method_name))
    print(f'{method_name} was called {call_count} times:')
    inputs = redis_store.lrange(input_key, 0, -1)
    outputs = redis_store.lrange(output_key, 0, -1)
    for input_data, output_data in zip(inputs, outputs):
        print(f'{method_name}(*{input_data.decode("utf-8")}) -> {output_data}')


class Cache:
    """
    Represents an object for storing data in a Redis data storage.
    """
    def __init__(self) -> None:
        """
        Initializes a Cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a value in a Redis data storage and returns the key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The key associated with the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, converter: Callable = None) -> Union[str, bytes, int, float]:
        """
        Retrieves a value from a Redis data storage.

        Args:
            key (str): The key associated with the stored data.
            converter (Callable, optional): A function to apply to the retrieved data. Defaults to None.

        Returns:
            Union[str, bytes, int, float]: The retrieved data.
        """
        data = self._redis.get(key)
        return converter(data) if converter is not None else data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from a Redis data storage.

        Args:
            key (str): The key associated with the stored string.

        Returns:
            str: The retrieved string.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer value from a Redis data storage.

        Args:
            key (str): The key associated with the stored integer.

        Returns:
            int: The retrieved integer.
        """
        return self.get(key, lambda x: int(x))
