import os
import dotenv
import typing as t

T = t.TypeVar("T")
G = t.TypeVar("G")


class MetaFoo(type, t.Generic[T]):
    @t.overload
    def __getitem__(cls, key: str) -> str:
        ...

    @t.overload
    def __getitem__(cls, key: tuple[str, t.Callable[[t.Any], T]]) -> T:
        ...

    @t.overload
    def __getitem__(cls, key: tuple[str, list[t.Callable[[t.Any], T]]]) -> set[T]:
        ...

    # def __getitem__(cls, key: t.Any) -> t.Any:
        # return key

    def __getitem__(
        cls,
        key: str
        | tuple[str, t.Callable[[t.Any], T]]
        | tuple[str, list[t.Callable[[t.Any], T]]],
    ) -> str | T | set[T]:
        if isinstance(key, tuple) and len(key) == 2:  # type specified
            if isinstance(key[1], list):  # type is as set
                # set logic
                return set([key[1][0](key[0])])

            return key[1](key[0])

        elif isinstance(key, str):  # No type specified
            return str(key)

        raise ValueError(
            f"Usage: Config['ENVVAR'], Config['ENVVAR', type], Config['ENVVAR', [type]]. Invalid key: {key!r}"
        )

class Foo(metaclass=MetaFoo):
    ...

# f: Foo = Foo()
print(Foo.__getitem__)
print(Foo["1"])
print((f := Foo.__getitem__("1")), type(f))
print("---")

print(Foo["1", int])
print((f := Foo.__getitem__(("1", int))), type(f))
print("---")

print(Foo["1", [int]])
print((f := Foo.__getitem__(("1", [int]))), type(f), type(f.copy().pop()))

