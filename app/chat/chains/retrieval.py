from langchain.chains import LLMChain
from app.chat.chains.streamable import StreamableChain

class StreamingConversationalLLMChain(
    StreamableChain, LLMChain
):
    pass