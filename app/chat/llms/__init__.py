from functools import partial
from .chatopenai import build_llm

llm_map={
    "gpt-4o": partial(build_llm, model_name="gpt-4o"),
}