import streamlit as st
import requests

API_BASE_URL = "https://myblog-production-ae88.up.railway.app/"

def main():
    st.set_page_config(page_title="Blog Manager", layout="centered")
    st.title("Article Manager (Blog API)")

    # ===========================
    # SECTION: LIST ARTICLES
    # ===========================
    st.header("List of Articles")

    if st.button("Load Articles"):
        url_list = f"{API_BASE_URL}/articles"
        st.write(">>> [DEBUG] GET:", url_list)  # Log de depuração
        response = requests.get(url_list)

        st.write(">>> [DEBUG] Status Code (List):", response.status_code)
        try:
            st.write(">>> [DEBUG] Response JSON (List):", response.json())
        except:
            st.write(">>> [DEBUG] Response Text (List):", response.text)

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

    # ===========================
    # SECTION: CREATE ARTICLE
    # ===========================
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
            # URL do POST /articles
            url_create = f"{API_BASE_URL}/articles"

            # Logs de depuração para verificar a rota e o payload
            st.write(">>> [DEBUG] POST:", url_create)
            st.write(">>> [DEBUG] Payload:", payload)

            response = requests.post(url_create, json=payload)

            st.write(">>> [DEBUG] Status Code (Create):", response.status_code)
            try:
                st.write(">>> [DEBUG] Response JSON (Create):", response.json())
            except:
                st.write(">>> [DEBUG] Response Text (Create):", response.text)

            if response.status_code == 201:
                st.success("Article created successfully!")
            else:
                st.error(f"Failed to create article: {response.text}")

    # ===========================
    # SECTION: EDIT ARTICLE
    # ===========================
    st.header("Edit Existing Article")

    article_id_edit = st.number_input("Article ID to Edit", min_value=1, step=1)
    if st.button("Load Article Data"):
        url_edit_get = f"{API_BASE_URL}/articles/{article_id_edit}"
        st.write(">>> [DEBUG] GET (Edit):", url_edit_get)
        response = requests.get(url_edit_get)

        st.write(">>> [DEBUG] Status Code (Edit GET):", response.status_code)
        try:
            st.write(">>> [DEBUG] Response JSON (Edit GET):", response.json())
        except:
            st.write(">>> [DEBUG] Response Text (Edit GET):", response.text)

        if response.status_code == 200:
            article_data = response.json()
            st.session_state["edit_article"] = article_data
        else:
            st.error("Article not found or request error.")

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
                url_update = f"{API_BASE_URL}/articles/{article_data['id']}"

                st.write(">>> [DEBUG] PUT:", url_update)
                st.write(">>> [DEBUG] Payload (Update):", payload_update)

                resp_update = requests.put(url_update, json=payload_update)

                st.write(">>> [DEBUG] Status Code (Update):", resp_update.status_code)
                try:
                    st.write(">>> [DEBUG] Response JSON (Update):", resp_update.json())
                except:
                    st.write(">>> [DEBUG] Response Text (Update):", resp_update.text)

                if resp_update.status_code == 200:
                    st.success("Article updated successfully!")
                    st.session_state["edit_article"] = resp_update.json()
                else:
                    st.error(f"Failed to update article: {resp_update.text}")

    # ===========================
    # SECTION: DELETE ARTICLE
    # ===========================
    st.header("Delete Article")

    article_id_delete = st.number_input("Article ID to Delete", min_value=1, step=1)
    if st.button("Delete"):
        url_delete = f"{API_BASE_URL}/articles/{article_id_delete}"
        st.write(">>> [DEBUG] DELETE:", url_delete)

        resp_delete = requests.delete(url_delete)

        st.write(">>> [DEBUG] Status Code (Delete):", resp_delete.status_code)
        try:
            st.write(">>> [DEBUG] Response JSON (Delete):", resp_delete.json())
        except:
            st.write(">>> [DEBUG] Response Text (Delete):", resp_delete.text)

        if resp_delete.status_code == 200:
            st.success("Article deleted successfully!")
        else:
            st.error(f"Failed to delete article: {resp_delete.text}")


if __name__ == "__main__":
    main()
