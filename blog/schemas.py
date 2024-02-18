from pydantic import BaseModel, ConfigDict


class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: list[Blog]
    model_config = ConfigDict(from_attributes=True)

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
    model_config = ConfigDict(from_attributes=True)