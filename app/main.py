from youtube_transcript_api import YouTubeTranscriptApi
from langchain_openai import ChatOpenAI
from langchain.tools import Tool, tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from pprint import pprint
import urllib.parse as urlparse
import os

load_dotenv()

############################################# Langchain ################################################

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant that specializes in summarizing video content. Below is the transcript of a YouTube video. Your task is to: \n"
                "1. Analyze the content carefully. \n"
                "2. Generate a concise, clear, and engaging summary that captures the key points discussed in the video. \n"
                "3. Use bullet points if there are multiple distinct ideas or topics.\n"
                "4. Ensure the summary is written in a way that is easy to understand, even for someone unfamiliar with the topic.\n"
                "5. Keep the summary under 150 words. \n"

                "Transcript: {transcript}"

                "Now, provide the summary:"

    ),
    ("user", "Summarize the transcript provided.")
])


class Summary(BaseModel):
    """Summary"""
    summary: str = Field(
        description="A complete summary as a single string"
    )

llm.with_structured_output(Summary)

chain = prompt | llm

# Generate summary
def get_summary(text):
    result = chain.invoke({"transcript": text})
    return result.content


############################################# YouTUbe ################################################

# Get video id
# def extract_video_id(url):
#     parsed_url = urlparse.urlparse(url)
#     query_params = urlparse.parse_qs(parsed_url.query)
#     return query_params.get("v", [None])[0]
def extract_video_id(url):
    # Проверяем, является ли ссылка короткой (youtu.be)
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]
    
    # Для стандартной ссылки youtube.com
    elif 'youtube.com' in url:
        # Находим параметр 'v=' и извлекаем ID видео
        start_index = url.find('v=')
        if start_index != -1:
            start_index += 2  # Пропускаем 'v='
            end_index = url.find('&', start_index)  # Ищем конец параметра
            if end_index == -1:  # Если параметров больше нет, берем до конца строки
                return url[start_index:]
            else:
                return url[start_index:end_index]
    
    return None


# Getting transcript
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'ru', "kz"]) 
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except Exception as e:
        return str(e)

def get_result(link):
    video_id = extract_video_id(link)
    transcript = get_transcript(video_id)
    summary = get_summary(transcript)
    return summary

############################################# Summarize ################################################
if __name__ == "__main__":
    link = input("link to the video:")
    print(get_result(link))