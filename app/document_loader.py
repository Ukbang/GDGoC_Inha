from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.document_loaders import PyPDFLoader, UnstructuredFileLoader
from langchain_core.documents.base import Document

def generate_title_and_summary(document_text:str, model:str="gpt-4o-mini", temperature:int =0.0):
    """LLM을 이용해 문서 조각의 제목과 요약 생성"""
    llm = ChatOpenAI(model=model, temperature=temperature)

    prompt = f"""
    다음 문서의 제목과 요약을 만들어 주세요
    요약은 20글자 이내로 작성해 주세요:

    문서 내용:
    {document_text}

    1. 제목: 
    2. 요약:
    """
    response = llm.invoke(prompt).content.strip()

    title = "Untitled"
    summary = "No Summary"    

    if not response:
        return title, summary

    # 제목과 요약을 파싱
    try:
        lines = response.split("\n")
        title = lines[0].replace("1. 제목: ", "").strip()
        summary = "\n".join(lines[1:]).replace("2. 요약:", "").strip()
    except:
        pass

    return title, summary

def create_retriever(loader: BaseLoader, chunk_size: int=300, chunk_overlap: int=50):

    """
    로드된 파일만 제공되면 제목과 요약 생성 후 리트리버를 생성해주는 모듈
    """

    Embeddings = OpenAIEmbeddings()

    # 텍스트 스플리터 생성
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, 
                                               chunk_overlap=chunk_overlap, 
                                               separators=["\n\n"])
    
    split_docs = loader.load_and_split(splitter)

    add_doc_list = []
    for doc in split_docs:
        title, summary = generate_title_and_summary(doc.page_content)
        doc.metadata["title"] = title
        doc.metadata["summary"] = summary
        add_doc_list.append(doc)

    vector_store = FAISS.from_documents(add_doc_list, Embeddings)
    retriever = vector_store.as_retriever()

    return retriever