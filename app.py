from textwrap import indent
import streamlit as st
import matplotlib.pyplot as plt 
from streamlit_echarts import st_echarts
from helper import make_stopwords, authenticate,create_pie_chart, get_user_tweeets,count_values_in_column, make_wordcloud, preprocess, get_tweets

st.set_page_config(layout="wide")
st.title(" 🐦 Analyse Your Tweets 🐦 ") 
seleected = st.selectbox('Pick one', ['An Account', 'A Tag'])
if seleected == "An Account":
    st.subheader("Create a wordcloud out of your recents tweets!")
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
                        figure = make_wordcloud(preprocess(outtweets))
                        st.pyplot(figure)
                        st.balloons()

                        plt.savefig('twitter_new.png', format="png")

                        with open("twitter_new.png", "rb") as file:
                            btn = st.download_button(
                                    label="Download image",
                                    data=file,
                                    file_name="wordcloud.png",
                                    mime="image/png"
                            )
                    
                except:
                    st.markdown("This account has fewer than 2 tweets. Tweet more and come back later or try again.")  
                
            except:
                st.markdown("This account doesn't exist. Please try again.")  

else:
    st.subheader("Analyse 500 recent tweets on a Tag")
    st.text_input("Enter a twitter tag to begin", key="tag")  

    if __name__ == "__main__":
        
        # if we didn't assign last_name yet, do it
        if "last_tag" not in st.session_state:
            st.session_state.last_tag = ""

        # if the user entered a new name
        if st.session_state.last_tag != st.session_state.tag:    
        
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

                with st.spinner(text='We\'re getting the tweets. Give it a sec...'):
                    tw_list = get_tweets(st.session_state.tag,500, st.session_state.api)
            
                # check that the user has tweeted at least ten times, 
                # if not display the except message 
                try:
                    # tw = tw_list[4]  
                
                    # display loading sign whie making the wordcould
                    st.spinner()

                    with st.spinner(text='We\'re building the wordcloud. Give it a sec...'):
                        tw_list_negative = tw_list[tw_list["sentiment"]=="negative"]
                        tw_list_positive = tw_list[tw_list["sentiment"]=="positive"]
                        tw_list_neutral = tw_list[tw_list["sentiment"]=="neutral"]
                        pc = count_values_in_column(tw_list,"sentiment")
                        # create data for Pie Chart
                        names= ['{} {}%'.format(x,str(round(pc.loc[x,"Percentage"]))) for x in pc.index]
                        data=pc["Percentage"]
                        pie_data = [{'value':round(pc.loc[x,"Percentage"]), 'name': '{} {}%'.format(x,str(round(pc.loc[x,"Percentage"])))} for x in pc.index ]
                        wordfig = make_wordcloud(str(tw_list["text"].values))
                        wordfig_neg = make_wordcloud(str(tw_list_negative["text"].values))
                        wordfig_neu = make_wordcloud(str(tw_list_neutral["text"].values))
                        wordfig_pos = make_wordcloud(str(tw_list_positive["text"].values))
                        st.pyplot(wordfig)
                        # piefig = create_pie_chart(data,names)
                        # st.pyplot(piefig)

                        option = {
                            "legend": {"top": "bottom"},
                            "toolbox": {
                                "show": True,
                                "feature": {
                                    "mark": {"show": True},
                                    "dataView": {"show": True, "readOnly": False},
                                    "restore": {"show": True},
                                    "saveAsImage": {"show": True},
                                },
                            },
                            "series": [
                                {
                                    "name": "Percentage of Sentiments",
                                    "type": "pie",
                                    "radius": [50, 250],
                                    "center": ["50%", "50%"],
                                    "roseType": "area",
                                    "itemStyle": {"borderRadius": 8},
                                    "data": pie_data,
                                }
                            ],
                        }
                        st_echarts(
                            options=option, height="600px",
                        )

                        # st.write(pie_data)
                        # st.write(piefig)


                        col1, col2, col3 = st.columns(3)

                        col1.pyplot(wordfig_neg)
                        col2.pyplot(wordfig_neu)
                        col3.pyplot(wordfig_pos)
                        st.balloons()
                        
                    
                except:
                    st.markdown("This account has fewer than 2 tweets. Tweet more and come back later or try again.")  
                
            except:
                st.markdown("This account doesn't exist. Please try again.")  
