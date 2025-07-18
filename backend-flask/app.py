import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import arxiv
from transformers import BartForConditionalGeneration, BartTokenizer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma  # Updated import
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
import chromadb

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Hugging Face BART model and tokenizer for summarization
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)
model.eval()  # Set model to evaluation mode

# Initialize ChromaDB (in-memory explicitly with EphemeralClient)
chroma_client = chromadb.EphemeralClient()
collection_name = "article-summaries"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = Chroma(
    collection_name=collection_name,
    embedding_function=embeddings,
    client=chroma_client
)


# Function to fetch articles from ArXiv
def fetch_arxiv_articles(query, max_results=5):
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    articles = []
    for result in client.results(search):
        articles.append({
            "id": result.entry_id.split("/")[-1],
            "title": result.title,
            "abstract": result.summary,
            "full_text": result.summary  # ArXiv API doesn't provide full text; using abstract
        })
    return articles


# Function to fetch articles from HAL
def fetch_hal_articles(query, max_results=5):
    url = f"https://api.archives-ouvertes.fr/search/?q={query}&rows={max_results}&sort=producedDate_tdate desc"
    response = requests.get(url)
    data = response.json()
    articles = []
    for doc in data.get("response", {}).get("docs", []):
        articles.append({
            "id": doc.get("docid"),
            "title": doc.get("title_s", ["No Title"])[0],
            "abstract": doc.get("abstract_s", ["No Abstract"])[0],
            "full_text": doc.get("abstract_s", ["No Abstract"])[0]  # HAL API doesn't provide full text
        })
    return articles


# Function to summarize using BART
def summarize_article(text):
    # Split text if it's too long
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=200)  # BART has a max length of 1024 tokens
    chunks = text_splitter.split_text(text)

    # Summarize each chunk using BART
    summaries = []
    for chunk in chunks:
        # Prepare the input with a prompt
        prompt = f"Summarize the following scientific article in 3-5 sentences, highlighting the key concepts:\n\n{chunk}"
        inputs = tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True)

        # Generate summary
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=150,  # Adjust based on desired summary length
            min_length=50,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary.strip())

    # Combine summaries and summarize again if needed
    combined_summary = " ".join(summaries)
    if len(summaries) > 1:
        # Re-summarize the combined summary if it's too long
        inputs = tokenizer(combined_summary, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=150,
            min_length=50,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        combined_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return combined_summary


# API endpoint to search and summarize articles
@app.route('/summarize-articles', methods=['POST'])
def summarize_articles():
    try:
        data = request.get_json()
        query = data.get("query")
        if not query:
            return jsonify({"error": "Query is required."}), 400

        # Fetch articles from ArXiv and HAL
        arxiv_articles = fetch_arxiv_articles(query)
        hal_articles = fetch_hal_articles(query)
        all_articles = arxiv_articles + hal_articles

        if not all_articles:
            return jsonify({"error": "No articles found for the query."}), 404

        # Summarize articles and store in ChromaDB
        summaries = []
        texts_to_embed = []
        metadatas = []
        ids = []

        for article in all_articles:
            summary = summarize_article(article["full_text"])
            summaries.append({
                "id": article["id"],
                "title": article["title"],
                "summary": summary
            })
            texts_to_embed.append(summary)
            metadatas.append({"article_id": article["id"], "title": article["title"]})
            ids.append(article["id"])

        # Store summaries in ChromaDB
        vector_store.add_texts(
            texts=texts_to_embed,
            metadatas=metadatas,
            ids=ids
        )

        return jsonify({"summaries": summaries})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API endpoint to retrieve summaries from ChromaDB
@app.route('/get-summaries', methods=['POST'])
def get_summaries():
    try:
        data = request.get_json()
        query = data.get("query")
        if not query:
            return jsonify({"error": "Query is required."}), 400

        # Search ChromaDB for relevant summaries
        results = vector_store.similarity_search(query, k=5)

        summaries = []
        for doc in results:
            summaries.append({
                "article_id": doc.metadata["article_id"],
                "title": doc.metadata["title"],
                "summary": doc.page_content
            })

        return jsonify({"summaries": summaries})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)