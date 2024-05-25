import random

from app.chat.models import ChatArgs
from app.chat.llms import llm_map
from app.chat.memories import memory_map
from app.chat.llms.chatopenai import build_llm
from app.chat.memories.sql_memory import build_memory
from app.chat.chains.retrieval import StreamingConversationalLLMChain
from app.chat.prompt import ConcretePromptTemplate
from langchain.chat_models import ChatOpenAI
from app.web.api import (
    set_conversation_components,
    get_conversation_components
)

def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """
 

    llm_name, llm = select_component(
        "llm",
        llm_map,
        chat_args,
        "gpt-4o"
    )
    memory_name, memory = select_component(
        "memory",
        memory_map,
        chat_args,
        "sql_buffer_memory"
    )

    set_conversation_components(
        chat_args.conversation_id,
        llm=llm_name,
        memory=memory_name
    )

    condense_question_llm = ChatOpenAI(streaming=False)

    prompt_template = ConcretePromptTemplate(
        condense_question_llm=condense_question_llm
    )

    # Initialize conversation with system message
    initial_message = prompt_template.initialize_conversation()
    condense_question_llm.invoke([initial_message])

    return StreamingConversationalLLMChain(
        llm=llm,
        memory=memory,
        prompt=prompt_template,
        metadata=chat_args.metadata
    )

def select_component(component_type, component_map, chat_args, component_name):
    components = get_conversation_components(chat_args.conversation_id)
    previous_component = components[component_type]

    if previous_component:
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        builder = component_map[component_name]
        return component_name, builder(chat_args)