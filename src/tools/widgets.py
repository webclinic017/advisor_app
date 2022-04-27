import streamlit as st
import webbrowser
import src.tools.scripts as s0

# - - - - - HOME PAGE - - - - -
def home_widget_analyst_rec(subhead, table1):
    st.write(subhead)
    st.table(table1)


def home_widget_instructions(header, key):
    st.write(header)
    st.write(key)


def home_widget_tools(subhead, category_1, key_1):
    st.subheader(f" > {subhead} ")
    st.write(f" {category_1}  ")
    st.write(key_1)
    
    
def home_disclosure():
    st.write(f"{s0.financial_disclosure}")
    


# - - - - - SNAPSHOT PAGE - - - - -
def snapshot_widget(head, key):
    st.subheader(head)
    st.markdown(key)


def snapshot_widget_screener(key):
    st.dataframe(key.set_index("ranking"))


def snapshot_widget_index(keya, keyb):
    for r in range(len(keya)):
        st.write(f"{keya[r]} {keyb[r]}")
    st.write("__" * 25)


def widget_header(web1, subhead, key):
    st.write(f">Online Resources:")
    st.write(f"{web1}")
    st.subheader(f"{subhead}:")
    st.write(f"{key}")
    
def widget_header2(key):
    st.caption(f"{key}")    
    st.caption(" "*25)


def my_widget_overview(header, key):
    st.subheader(header)
    st.write(key)


def widget_online_resource(key):
    st.write(f"{' '*25}")
    st.markdown("__Online Resources__")
    st.caption(f" - {key}")
    st.write(f"{'_'*25}")


def widget_basic(head, subhead, key):
    st.header(f"{head}")
    st.subheader(f"{subhead}:")
    st.write(f" - {key}")


def my_widget_financial_disclosure(header, key):
    st.subheader(header)
    st.write(key)


def widget_prophet(key_1, key_2, web_address):
    st.caption(f"{key_1}")
    st.caption(f"{key_2}")
    st.write(' '*25)
    if st.button("Open Prophet Model Web Page"):
        webbrowser.open_new_tab(web_address)


def widget_analysis(subhead, key):
    st.write(f"{' '*25}")
    st.markdown(f"__{subhead}__")
    st.caption(f"{key}")
    st.write(f"{' '*25}")
    
def widget_analysis2(subhead, key):
    st.markdown(f"{subhead}")
    st.caption(f"{key}")
    st.write(f"{' '*25}")


def widget_univariate(key):
    st.caption(f"{key}")


# - - - - - XXXXX PAGE - - - - -
