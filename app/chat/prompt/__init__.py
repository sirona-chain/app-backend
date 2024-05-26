from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain.schema import HumanMessage, SystemMessage, BaseMessage
from langchain.chat_models import ChatOpenAI
from typing import List, Any

class ConcretePromptTemplate(ChatPromptTemplate, BaseModel):
    condense_question_llm: ChatOpenAI
    input_variables: List[str] = Field(default_factory=lambda: ["question"])

    def __init__(self, **data: Any):
        super().__init__(**data)
        print("this 0")
        if 'condense_question_llm' not in data:
            raise ValueError("condense_question_llm must be provided")
        print("this 1")
        self.condense_question_llm = data['condense_question_llm']
        print("this 2")
        self.input_variables = data.get('input_variables', ["question"])

    def initialize_conversation(self) -> SystemMessage:
        return SystemMessage(content="You are an assistant. Answer the following questions to the best of your ability.")

    def format(self, **kwargs: Any) -> str:
        question = kwargs.get('question', '')
        if not question:
            raise ValueError("The 'question' must be provided in kwargs")

        # Prepare the message for the LLM
        messages = [HumanMessage(content=question)]

        try:
            # Debugging: Print the messages
            print(f"Messages sent to LLM: {messages}")

            # Use condense_question_llm to process the message
            response = self.condense_question_llm(messages=messages)

            # Debugging: Print the raw response
            print(f"Raw response from LLM: {response}")

            if not response or not hasattr(response[0], 'text'):
                raise ValueError("The response from LLM is not in the expected format")

            return response[0].text
        except Exception as e:
            raise ValueError(f"Error running chat: {e}")

    def format_prompt(self, **kwargs: Any) -> List[BaseMessage]:
        question = kwargs.get('question', '')
        if not question:
            raise ValueError("The 'question' must be provided in kwargs")

        messages = [HumanMessage(content=question)]
        try:
            response = self.condense_question_llm(messages=messages)
            if not response or not hasattr(response[0], 'text'):
                raise ValueError("The response from LLM is not in the expected format")
        except Exception as e:
            raise ValueError(f"Error running chat: {e}")

        return [BaseMessage(content=response[0].text)]
