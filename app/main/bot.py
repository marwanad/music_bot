from flask import Blueprint, request, Response, redirect, url_for, render_template
from kik.messages import messages_from_json, TextMessage, VideoMessage, StartChattingMessage, SuggestedResponseKeyboard, TextResponse
from kik import KikApi, Configuration

from . import main
from setup import kik
from wubble import WubbleMessage
import music

MAIN_SR = [TextResponse(body=sr) for sr in ['Start a quiz', 'Custom track', 'Share', 'Settings']]
INTRO_BODY = 'Hi you reached the intro stage, tap a sr for more options :+1:'

preview_base_url = "https://p.scdn.co/mp3-preview/"

@main.route('/receive', methods=['POST'])
def receive():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        if isinstance(message, TextMessage):
            if((message.body) == "give track pls"):
                kik.send_messages([
                    WubbleMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    url=url_for("main.music_player", id=music.get_song_from_genre("pop"),_external=True)
                )
                    ])
        return Response(status=200)

@main.route('/musicplayer/<id>', methods=['GET'])
def music_player(id):
    return render_template('main/sound_frame.html', preview_url=preview_base_url+id)

@main.route('/intro', methods=['GET'])
def intro():
    to = request.args.get('to')
    chat_id = request.args.get('chat_id')
    body = INTRO_BODY

    if to and chat_id:
        kik.send_messages([
            TextMessage(
                to=to,
                chat_id=chat_id,
                body=body,
                keyboards=[SuggestedResponseKeyboard(responses=MAIN_SR)]
            )
        ])
    return Response(status=200)

if __name__ == '__main__':
    manager.run()