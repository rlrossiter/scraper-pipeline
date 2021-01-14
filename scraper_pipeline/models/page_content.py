import typing


class PageContent(typing.NamedTuple):
    page_id: str
    url: str
    req_time: str
    resp_time_ms: int
    statuscode: int
    content: str = None