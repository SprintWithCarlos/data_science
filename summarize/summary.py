from youtube_transcript_api import YouTubeTranscriptApi
import os
import openai
from pytube import YouTube


def summarize(url, api_key, language="en"):
    filename = "summary.md"
    language_array = [language]
    os.environ["OPENAI_API_KEY"] = api_key
    openai.api_key = os.getenv("OPENAI_API_KEY")
    yt = YouTube(url)
    title = yt.title
    author = yt.author
    video_id = url.split("=")[1]
    try:
        transcription = YouTubeTranscriptApi.get_transcript(
            video_id, language_array)
        data = [f'Transcript of "{title.lower()}" by {author}:']
        for item in transcription:
            data.append(item['text'].lower())
        max_chunk_length = 2048
        chunks = []
        current_chunk = []
        current_chunk_length = 0
        for sentence in data:
            current_chunk_length += len(sentence)
            if current_chunk_length > max_chunk_length:
                chunks.append(current_chunk)
                current_chunk = []
                current_chunk_length = 0
            current_chunk.append(sentence)
        chunks.append(current_chunk)
        summary_responses = []
        for chunk in chunks:
            sentences = " ".join(list(chunk))
            prompt = f"{sentences}\n\nTl;dr"
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=300,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=1
            )
            response_text = response["choices"][0]["text"]
            summary_responses.append(response_text)
        sentence = " ".join(summary_responses).replace(
            ": ", "").replace("\n", "")
        prompt = f"{sentence}\n\nTl;dr"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=300,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=1
        )
        executive_summary = response["choices"][0]["text"].replace(": ", "")
        new_array = [
            f"""# Transcript of "{title.capitalize()}" by {author.capitalize()}
Link: [{url}]({url})
## Executive Summary:
{executive_summary}
## Main Takeaways:
  """]
        for i, item in enumerate(summary_responses):
            new_item = item.replace(": ", "").replace("\n", "")
            new_array.append(f"""{i + 1}. {new_item}\n  """)
        sentence = "".join(new_array)
        with open(filename, "w") as f:
            f.write(sentence)
    except Exception as e:
        lines = str(e).splitlines()
        lines_array = []
        for i in range(12):
            lines_array.append(lines[i])
        message = """ """.join(list(lines_array))
        return (f"""An error occurred: {message}""")