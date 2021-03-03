from io import BufferedReader
from typing import Dict, Tuple, Union

RequestsFileNameType = str
RequestsContentType = str
RequestsHeadersType = Dict[str, str]

RequestsFileType = Union[
    BufferedReader,
    Tuple[RequestsFileNameType, BufferedReader],
    Tuple[RequestsFileNameType, BufferedReader, RequestsContentType],
    Tuple[
        RequestsFileNameType,
        BufferedReader,
        RequestsContentType,
        RequestsHeadersType,
    ],
]
