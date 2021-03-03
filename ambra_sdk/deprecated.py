import functools
import inspect
import warnings


def deprecated(reason: str):
    """Set deprecated.

    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.

    >>> # The @deprecated is used with a 'reason'.
    >>> @deprecated("please, use another function")
    >>> def old_function(x, y):
    >>>   pass

    >>> # The @deprecated is used without any 'reason'.
    >>> @deprecated
    >>> def old_function(x, y):
    >>>   pass

    :param reason: reason
    :raises TypeError: unknown reason type
    :return: decorated method
    """
    if isinstance(reason, str):
        # The @deprecated is used with a 'reason'.
        def _decorator(func1):  # NOQA:WPS430

            if inspect.isclass(func1):
                fmt1 = 'Call to deprecated class {name} ({reason}).'
            else:
                fmt1 = 'Call to deprecated function {name} ({reason}).'

            @functools.wraps(func1)  # NOQA:WPS430
            def new_func1(*args, **kwargs):
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(
                    fmt1.format(name=func1.__name__, reason=reason),
                    category=DeprecationWarning,
                    stacklevel=2,
                )
                warnings.simplefilter('default', DeprecationWarning)
                return func1(*args, **kwargs)

            return new_func1

        return _decorator

    elif inspect.isclass(reason) or inspect.isfunction(reason):
        # The @deprecated is used without any 'reason'.
        func2 = reason

        if inspect.isclass(func2):
            fmt2 = 'Call to deprecated class {name}.'
        else:
            fmt2 = 'Call to deprecated function {name}.'

        @functools.wraps(func2)  # NOQA:WPS430
        def new_func2(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                fmt2.format(name=func2.__name__),
                category=DeprecationWarning,
                stacklevel=2,
            )
            warnings.simplefilter('default', DeprecationWarning)
            return func2(*args, **kwargs)

        return new_func2
    raise TypeError(repr(type(reason)))
