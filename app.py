import streamlit as st
from helper import make_stopwords, authenticate, get_user_tweeets, make_wordcloud

st.title(" ☁️ Analyse Your Tweets ☁️ ") 
st.subheader("Create a wordcloud out of your last 200 tweets!")
st.text_input("Enter a twitter username to begin", key="name")

if __name__ == "__main__":
    
    # if we didn't assign last_name yet, do it
    if "last_name" not in st.session_state:
        st.session_state.last_name = ""

    # if the user entered a new name
    if st.session_state.last_name != st.session_state.name:    
    
        # if we didn't load the stopwords yet, do it 
        if "all_stopwords" not in st.session_state:
            st.session_state.all_stopwords = make_stopwords()
    
        # if we didn't authenticate yet, do it 
        if "api" not in st.session_state:    

            st.session_state.api = authenticate(st.secrets["consumer_key"],
                                            st.secrets["consumer_secret"],
                                            st.secrets["access_token_key"],
                                            st.secrets["access_token_secret"])
                                            
            st.session_state.api = authenticate(st.secrets["consumer_key"],
                                            st.secrets["consumer_secret"],
                                            st.secrets["access_token_key"],
                                            st.secrets["access_token_secret"])

        
        
        # try getting the tweets; if the username is incorrect, display the except message     
        try:
            outtweets = get_user_tweeets(st.session_state.name,st.session_state.api)
        
            # check that the user has tweeted at least ten times, 
            # if not display the except message 
            try:
                cat = outtweets[1]  
            
                # display loading sign whie making the wordcould
                st.spinner()
                with st.spinner(text='We\'re building the wordcloud. Give it a sec...'):
                    figure = make_wordcloud(st.session_state.all_stopwords, outtweets)
                    st.pyplot(figure)
                    st.balloons()
                
            except:
                st.markdown("This account has fewer than 2 tweets. Tweet more and come back later or try again.")  
            
        except:
            st.markdown("This account doesn't exist. Please try again.")        