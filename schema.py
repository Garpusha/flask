import typing
import pydantic
# from pydantic import validator


class CreateAd(pydantic.BaseModel):
    header: str
    text: str
    owner: str

    @pydantic.validator("text")
    def check_text_len(cls, value):
        if len(value) < 10:
            raise ValueError("Ad text is too short, at least 10 symbols.")
        return value

    @pydantic.validator("header")
    def check_header_len(cls, value):
        if len(value) < 5:
            raise ValueError("Header is too short, at least 5 symbols.")
        return value


class UpdateAd(pydantic.BaseModel):
    text: typing.Optional[str]
    header: typing.Optional[str]
    owner: str

    @pydantic.validator("text")
    def check_text_len(cls, value):
        if len(value) < 10:
            raise ValueError("Ad text is too short, at least 10 symbols.")
        return value

    @pydantic.validator("header")
    def check_header_len(cls, value):
        if len(value) < 5:
            raise ValueError("Header is too short, at least 5 symbols.")
        return value
