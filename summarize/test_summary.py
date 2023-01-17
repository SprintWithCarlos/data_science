import os
from mock import patch
from summary_for_test import summarize


current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, "summary.md")


@patch('summary_for_test.YouTubeTranscriptApi.get_transcript', return_value=[{'text': 'This is a test transcript.'}])
@patch('openai.Completion.create', return_value={'choices': [{'text': 'This is a summary.'}]})
@patch('summary_for_test.YouTube')
def test_summarize(mock_youtube, mock_openai_create, mock_yt_transcripts):
    if os.path.exists(filename):
        os.remove(filename)
        # print(f"{filename} deleted!")
    # time.sleep(5)
    # delete_file is being accessed here

    mock_youtube_instance = mock_youtube.return_value
    mock_youtube_instance.title = 'Test Title'
    mock_youtube_instance.author = 'Test Author'

    url = 'https://www.youtube.com/watch?v=6GQRnPlephU'
    api_key = 'test_api_key'

    summarize(url, api_key)

    mock_yt_transcripts.assert_called_once()
    mock_openai_create.assert_called()
    mock_youtube.assert_called_once_with(url)
    assert os.path.exists(filename)
    with open(filename, 'r') as f:
        summary = f.read()
        assert 'Transcript of' in summary
        assert 'Executive Summary' in summary
        assert 'Main Takeaways' in summary

    os.remove(filename)
