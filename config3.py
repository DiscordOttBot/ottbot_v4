import typing as t

T = t.TypeVar("T")


class MetaFoo(type):
    @t.overload
    def __getitem__(cls, key: str) -> str:
        ...

    @t.overload
    def __getitem__(cls, key: tuple[str, t.Callable[..., T]]) -> T:
        ...

    @t.overload
    def __getitem__(cls, key: tuple[str, t.Type[set], t.Callable[..., T]]) -> set[T]:
        ...

    def __getitem__(
        cls,
        key: t.Any,
    ) -> t.Any:
        match key:
            case (name, cast):
                return cast(name)

            case (name, _, cast):
                return {cast(e) for e in name.split(",")}

            case _:
                return str(key)


class Foo(metaclass=MetaFoo):
    ...


reveal_type(Foo["hello"])
reveal_type(Foo["123", int])
reveal_type(Foo["123,456,789", set, int])
