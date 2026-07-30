#=======LOAD MODULES==============
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
import langchain_community
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np


#To show web-app: complete page layout
st.set_page_config(layout="wide")

#To Give Title
st.title("AI RESUME GENERATOR")
st.write("""This app helps user to build customized professional
Resume with Latest job apply Links""")

st.image("bg.png")



# Step 3:API KEY
TAVILY_API_KEY = "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"
GOOGLE_API_KEY = "AQ.Ab8RN6IY8PK4p1AAGpJGv5JufJzNFk8B3drGwV6KULvw8YtHgg"
GROQ_API_KEY = "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"



model = ChatGoogleGenerativeAI(
    model ="gemini-3.5-flash-lite",
    google_api_key =GOOGLE_API_KEY
)
# response = model.invoke("Hellobuddy!")
# response.content[-1]['text']


def search_latest_new_jobs(query):
  """this function helps to fetch latest
  news or jobs related article using
  tavily"""

  client = TavilyClient(
      api_key = TAVILY_API_KEY)
  response = client.search(query)
  return response

# Agent Creation
agent = create_agent(
    model = model,
    tools= [search_latest_new_jobs])
# agent

def main_agent(agent, query):
  """This is the main agent, or leader agent
  orchestrate sub agents"""

  #giving prompt to create detailed prompt for code generation
  prompt = """You are AI assistant and below given is a prompt,
  your task is to give detailed prompt for this.
  You are a proffessional Resume generator where user will give
  their personal info, you have to create detailed resume
  for students or proffessional one,
  with advanced CSS proffessional designing
  it must be with dynamic UI and UX and, MAke sure to give output in HTML
  format only no markdowns allowed"""

  response = agent.invoke({'messages':[{'role':'user',
                                        'content':prompt}]})
  detailed_prompt = response["messages"][-1].content[-1]['text']

  #save prompt using file handling
  with open('prompt.txt','w') as f:
    f.write(detailed_prompt)

  user_details= f"""Below given is a user details generate
  Resume based on that, if not given
  keep: Default Resume: Python developer user details: {query}"""


  final_prompt = prompt + detailed_prompt + user_details

  #CODE GENERATION


  response = agent.invoke({'messages':[{'role':'user',
                                        'content':final_prompt}]})
  code = response["messages"][-1].content[-1]['text']
  return code


# code = main_agent(agent, "Rishabh, Python developer, Data Analyst, GENI AI EXPERT")
# from IPython import display as DISPLAY
# DISPLAY.HTML(code)


#fetch Latest Domain related Jobs using Tavily

def get_jobs(agent,
             Location = "Noida,Delhi",
             Profile = "Data Analysts, Data Science"):

              prompt = f"""Based on user given job profile,
              fetch latest jobs or job apply article
              using Naukri,Linkdein Indeed, or all popular
              job apply platforms, Show Results with
              JOB PROFILE NAME, LOCATION, Salary,Company Name,
              SHOE jobs only related to given
              {Location} and {Profile}. Output must be in
              Professional HTML Naukri theme cards with Dynamic Design,
              Show atleast Top 10-20 results with diect apply link"""



              response = agent.invoke({'messages':[{'role':'user',
                                        'content':prompt}]})
              code = response["messages"][-1].content[-1]['text']
              return code


# code = get_jobs(agent)
# DISPLAY.HTML(code)

