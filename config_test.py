# import builtins
import typing as t

T = t.TypeVar("T", bound="MetaFoo")


class MetaFoo(type, t.Generic[T]):
    @t.overload
    def __getitem__(cls, key: str) -> str:
        ...

    @t.overload
    def __getitem__(cls, key: tuple[str, t.Callable[[t.Any], T]]) -> T:
        ...

    @t.overload
    def __getitem__(cls, key: tuple[str, t.Type[set], t.Callable[[t.Any], T]]) -> set[T]:
        ...

    def __getitem__(
        cls,
        key: str | tuple[str, t.Callable[[t.Any], T]] | tuple[str, t.Type[set], t.Callable[[t.Any], T]],
    ) -> str | T | set[T]:
        match key:
            case (name, cast):
                return cast(name)

            case (name, set, cast):
                return {cast(e) for e in name.split(",")}

            case _:
                return str(key)


class Foo(metaclass=MetaFoo):
    ...


if t.TYPE_CHECKING:
    reveal_type(Foo["hello"])
    reveal_type(Foo["123", int])
    reveal_type(Foo["123,456,789", set, int])
else:
    print(Foo["hello"])  # "hello"
    print((f := Foo.__getitem__("1")), type(f))  # "hello" <class 'str'>
    print("---")

    print(Foo["1", int])  # 1
    print((f := Foo.__getitem__(("1", int))), type(f))  # 1 <class 'int'>
    print("---")

    print(Foo["123,456,789", set, int])  # {123, 456, 789}
    print(
        (f := Foo.__getitem__(("1", set, int))), type(f), type(f.copy().pop())
    )  # {123,356,789} <class 'set'> <class 'int'>
