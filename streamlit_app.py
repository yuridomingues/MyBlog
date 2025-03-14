import streamlit as st
import requests

# Base URL of your API
API_BASE_URL = "https://myblog-production-ae88.up.railway.app"  # Ajuste para a URL real do seu back-end

st.set_page_config(page_title="Blog Manager", layout="centered")
st.title("Article Manager (Blog API)")

# =======================================
# SECTION: LIST ARTICLES
# =======================================
st.header("List of Articles")

if st.button("Load Articles"):
    # Chama GET /articles
    response = requests.get(f"{API_BASE_URL}/articles")
    if response.status_code == 200:
        articles = response.json()
        if articles:
            for article in articles:
                st.subheader(f"ID: {article['id']} | {article['title']}")
                st.write(article["content"])
                st.write(f"Published? {article['published']}")
                st.write("---")
        else:
            st.info("No articles found.")
    else:
        st.error("Failed to retrieve articles.")

# =======================================
# SECTION: CREATE ARTICLE
# =======================================
st.header("Create New Article")

with st.form("create_article_form"):
    new_title = st.text_input("Article Title", value="")
    new_content = st.text_area("Content")
    new_published = st.checkbox("Published?", value=False)

    submitted = st.form_submit_button("Create")
    if submitted:
        payload = {
            "title": new_title,
            "content": new_content,
            "published": new_published
        }
        # Chama POST /articles
        response = requests.post(f"{API_BASE_URL}/articles", json=payload)
        if response.status_code == 201:
            st.success("Article created successfully!")
        else:
            st.error(f"Failed to create article: {response.text}")

# =======================================
# SECTION: EDIT ARTICLE
# =======================================
st.header("Edit Existing Article")

article_id_edit = st.number_input("Article ID to Edit", min_value=1, step=1)
if st.button("Load Article Data"):
    # Chama GET /articles/{id}
    url = f"{API_BASE_URL}/articles/{article_id_edit}"
    response = requests.get(url)
    if response.status_code == 200:
        article_data = response.json()
        st.session_state["edit_article"] = article_data
    else:
        st.error("Article not found or request error.")

# Se temos dados salvos em session_state
if "edit_article" in st.session_state:
    article_data = st.session_state["edit_article"]
    with st.form("update_article_form"):
        updated_title = st.text_input("Title", value=article_data["title"])
        updated_content = st.text_area("Content", value=article_data["content"])
        updated_published = st.checkbox("Published?", value=article_data["published"])

        submitted_update = st.form_submit_button("Update")
        if submitted_update:
            payload_update = {
                "title": updated_title,
                "content": updated_content,
                "published": updated_published
            }
            # Chama PUT /articles/{id}
            url_update = f"{API_BASE_URL}/articles/{article_data['id']}"
            resp_update = requests.put(url_update, json=payload_update)
            if resp_update.status_code == 200:
                st.success("Article updated successfully!")
                st.session_state["edit_article"] = resp_update.json()
            else:
                st.error(f"Failed to update article: {resp_update.text}")

# =======================================
# SECTION: DELETE ARTICLE
# =======================================
st.header("Delete Article")

article_id_delete = st.number_input("Article ID to Delete", min_value=1, step=1)
if st.button("Delete"):
    # Chama DELETE /articles/{id}
    url_delete = f"{API_BASE_URL}/articles/{article_id_delete}"
    resp_delete = requests.delete(url_delete)
    if resp_delete.status_code == 200:
        st.success("Article deleted successfully!")
    else:
        st.error(f"Failed to delete article: {resp_delete.text}")
