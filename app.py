import streamlit as st
import pickle
import numpy as np

# Load models and data
popular_df = pickle.load(open('model/popular.pkl', 'rb'))
pt = pickle.load(open('model/pt.pkl', 'rb'))
books = pickle.load(open('model/books.pkl', 'rb'))
similarity_scores = pickle.load(open('model/similarity_scores.pkl', 'rb'))

# Streamlit UI
st.set_page_config(page_title="Book Recommender", layout="wide")
st.title("📚 My Book Recommender System")

# Home Page - Display Top Books
st.header("Top 50 Books")
cols = st.columns(4)

for i in range(len(popular_df)):
    with cols[i % 4]:
        st.image(popular_df['Image-URL-M'].iloc[i], width=150)
        st.write(f"**{popular_df['Book-Title'].iloc[i]}**")
        st.write(f"👤 {popular_df['Book-Author'].iloc[i]}")
        st.write(f"⭐ {popular_df['avg_rating'].iloc[i]} ({popular_df['num_ratings'].iloc[i]} votes)")
        st.markdown("---")

# Recommendation Section
st.header("🔍 Get Book Recommendations")
user_input = st.text_input("Enter a book title:")

if st.button("Recommend"):
    if user_input not in pt.index:
        st.error("Book not found! Please try another book.")
    else:
        index = np.where(pt.index == user_input)[0]
        if len(index) == 0:
            st.error("Book not found! Please try another book.")
        else:
            index = index[0]  # Extract index value
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

            st.subheader("📖 Recommended Books:")
            for i in similar_items:
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                if temp_df.empty:
                    continue

                st.image(temp_df['Image-URL-M'].values[0], width=150)
                st.write(f"**{temp_df['Book-Title'].values[0]}**")
                st.write(f"👤 {temp_df['Book-Author'].values[0]}")
                st.markdown("---")
