from langchain.prompts import BasePromptTemplate
from pydantic import BaseModel, Field
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI

class ConcretePromptTemplate(BasePromptTemplate, BaseModel):
    condense_question_llm: ChatOpenAI
    input_variables: list[str] = Field(default_factory=lambda: ["question"])

    class Config:
        arbitrary_types_allowed = True
    
    def initialize_conversation(self):
        # Create the initial system message
        system_message = SystemMessage(content="You are an assistant. Answer the following questions to the best of your ability.")
        return system_message

    def format(self, **kwargs):
        question = kwargs.get('question', '')

        if not question:
            raise ValueError("The 'question' must be provided in kwargs")
        
        # Create messages to send to the LLM
        messages = [
            HumanMessage(content=question)
        ]
        
        # Invoke the LLM to get the response
        response = self.condense_question_llm.invoke(messages)
        
        return response.content

    def format_prompt(self, **kwargs):
        question = kwargs.get('question', '')

        if not question:
            raise ValueError("The 'question' must be provided in kwargs")

        # Create messages for the current user question
        messages = [HumanMessage(content=question)]
        
        # Invoke the LLM to get the response
        response = self.condense_question_llm.invoke(messages)

        return response.content

    def to_messages(self):
        # This method should return a list of messages for the conversation
        return []
