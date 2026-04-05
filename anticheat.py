from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def check_for_ai(candidate_text):
    # Q- what is python ?
    ai_baseline = "Python is a high-level, interpreted programming language known for its readability and versatility. It supports multiple programming paradigms."

    embeddings = model.encode([candidate_text,ai_baseline])
    similarity = cosine_similarity([embeddings[0]],[embeddings[1]])[0][0]

    print(f"similarity : {similarity:.2f}")

    if similarity > 0.80: 
        return "Likely AI generated"
    else:
        return "originally written , not ai generated"

sample_answer = "Python is a way for people to give instructions to computers using words and structures that look very similar to everyday English"

print(check_for_ai(sample_answer))