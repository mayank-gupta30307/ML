import os
from langchain_classic.schema.document import Document
import pandas as pd
from tqdm import tqdm
import json
from embedding_fn import embedding
from langchain_community.vectorstores.chroma import Chroma

curr_dir = os.path.dirname(__file__)
medquad_path = os.path.join(curr_dir , "Data" , "medquad.csv")
WHO_jsons_path = os.path.join(curr_dir , "Data" , "WHO")


def make_db_from_csv(path):
    data = []
    db = pd.read_csv(path)
    print("Fetching Data from csv file...")
    for i in tqdm(range(len(db))):
        content = f"""Question : {db.iloc[i]["question"]}\n\n
        Answer : {db.iloc[i]["answer"]}\n\n
        Focus Area : {db.iloc[i]["focus_area"]}"""

        metadata = {"Source" : db.iloc[i]["source"]}
        doc = Document(
            page_content=content,
            metadata = metadata
        )
        data.append(doc)
    return data


def make_db_from_jsons(dir):
    data = []
    files = os.listdir(dir)
    print("Fetching Data from json files")
    for file in tqdm(files):
        with open(os.path.join(dir , file) , "r") as f:
            json_content = json.load(f)
            for k,v in json_content.items():
                if k=="link":
                    continue
                content = f"About {file[:-len(".json")]}\n{k}\n{v}"
                metadata = {"Source" : f"World Health Organisation data on {file[:-len(".json")]}" , "link" : json_content["link"]}
                doc = Document(
                    page_content = content,
                    metadata = metadata
                )
                data.append(doc)
    return data


def make_vectorstore(data):
    embedding_fn = embedding()
    if "Vectorstore" not in os.listdir(curr_dir):
        os.mkdir(os.path.join(curr_dir , "Vectorstore"))
    db = Chroma.from_documents(
        documents = data,
        embedding = embedding_fn,
        persist_directory = os.path.join(curr_dir , "Vectorstore")
    )


def compile_data(json_path , csv_path):
    json_data = make_db_from_jsons(json_path)
    csv_data = make_db_from_csv(csv_path)
    full_data = csv_data+json_data
    return full_data

def compiled_data():
    return compile_data(json_path = WHO_jsons_path , csv_path = medquad_path)

if __name__=="__main__":
    data = compile_data(json_path = WHO_jsons_path , csv_path = medquad_path)
    make_vectorstore(data = data)
    print("Vectorstore Creation Completed")

# 15:10