from langchain_openai import ChatOpenAI
from typing import Literal
from pydantic import BaseModel, Field

class BinaryChecker(BaseModel):
    """
    당신은 질의와 문서의 연관성을 분석하는 분석가입니다. 
    문서 내에 질의에 대한 답변이 있는 경우 'yes' 라고 답변하고 없는 경우 'no'라고 답변하세요.
    """

    binary_score : Literal["yes", "no"] = Field(..., description="Documents are relevant to the question, 'yes' or 'no'")


def relevance_docs(context:str, 
                   query:str, 
                   model:str = "gpt-4o-mini", 
                   temperature:float = 0.0,
                   mode:str = "binary") -> Literal["yes", "no"]:
    
    if mode != "binary":
        raise ValueError("선택된 모드가 없습니다. 'binary' 모드를 선택해주세요.")
    
    else:
        llm = ChatOpenAI(model=model,
                        temperature=temperature,).with_structured_output(BinaryChecker)
        result = llm.invoke(f"문서 : {context} \n\n 질의 : {query}")

        assert result.binary_score in ["yes", "no"], f"❌ 잘못된 응답: {result.binary_score}"

        return result.binary_score

    
    
