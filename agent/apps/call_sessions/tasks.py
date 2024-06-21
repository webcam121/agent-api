import pdb

from celery import shared_task

from agent.apps.notifications.tasks import send_story_shared_email_to_giver
from agent.services import openai_api
from django.db.models import Q, F, When, Case, Value, Count
from django.db.models.functions import Coalesce
from django.db import models
from pydub import AudioSegment
from pydub.silence import split_on_silence
import io
from django.core.files import File


@shared_task
def summarize_call_session(call_session_id):
    from .models import CallSession, SummarySettings
    call_session = CallSession.objects.get(pk=call_session_id)
    first_name = call_session.receiver.user.first_name
    conversation = call_session.conversation.all().order_by('save_time')

    text = ''
    for conv in conversation:
        text += f"{conv.role.capitalize()}:\n{conv.content}\n\n"

    if text:
        text = 'Here is a conversation between assistant and User:\n' + text
    else:
        return 'No conversation to summarize.'
    text = text + (
        f'Now summarize the health issues and activities in the following format, refer the user by their name {first_name}.\n\n'
        'Well-being: [fill in health issues] (if the issue is an existing condition, point it out; '
        'if no issue, fill in "No issue reported". Use full sentences, past tense but be extremely concise)\n\n'
        'Activities: [fill in the activities the user did or plan to do] (if no activities, '
        'fill in "No specific activities". Use full sentences, past tense but be extremely concise.)'
    )

    summary_settings = SummarySettings.objects.get(summary_type='session_summary')
    summary = openai_api.generate(
        messages=[{'role': 'system', 'content': summary_settings.prompt}, {'role': 'user', 'content': text}],
        temperature=summary_settings.temperature,
        model=summary_settings.model,
        max_tokens=summary_settings.max_tokens
    )
    call_session.summary = summary

    call_session.save()
    send_story_shared_email_to_giver(receiver_id=call_session.receiver.pk, message=call_session.summary)

    text = (
        f'User:\n{first_name} is a senior. The following are records of {first_name} on the previous day\n\n'
        f'{summary}\n\n'
        'Read the records above then do the following.\n'
        '- If they had some new health issues, print the following string: "Health: '
        '[Summarize their health conditions in full sentences as something that happened '
        'in the past. All verb must be past tense. Don\'t include exact date. Be very concise]". '
        'Fill in the content in the [].\n'
        '- ELSE If they had no health issue, print the following string: "Health: N/A". Only print the paragraph.\n\n'
        '- If they mentioned he is going to do some activities, print the following string: "Activities:  '
        '[Summarize their activities in full sentences as something that happened in the past. Use past tense. Don\'t '
        'include exact date. Be very concise]".  Fill in the content in the [].\n' 
        '- ELSE If they didn\'t mentioned he is going to do some activities, print the '
        'following paragraph: "Activities: N/A". Only print the paragraph.'
    )
    summary_settings = SummarySettings.objects.get(summary_type='analyze_session_summary')
    summary = openai_api.generate(
        messages=[{'role': 'system', 'content': summary_settings.prompt}, {'role': 'user', 'content': text}],
        temperature=summary_settings.temperature,
        model=summary_settings.model,
        max_tokens=summary_settings.max_tokens
    )

    call_session.analyzer_summary = summary

    call_session.save()
    def _generate_summary(audio):
        combined_file = io.BytesIO()
        audio.export(combined_file, format='wav')
        combined_file.seek(0)
        call_session.audio = File(combined_file)
        call_session.audio.name = 'audio.wav'
        call_session.save()
        combined_file.close()  # Closing the BytesIO object as it's no longer needed.

    audio = AudioSegment.empty()
    for conv in conversation:
        print(conv.audio)
        audio_snippet = AudioSegment.from_file(conv.audio.open(mode='rb'))
        audio_chunks = split_on_silence(
            audio_snippet,
            min_silence_len=2000,
            silence_thresh=-45,
            keep_silence=500,
        )
        audio_processed = sum(audio_chunks)
        audio += audio_processed

    if audio:
        _generate_summary(audio)

    return summary


