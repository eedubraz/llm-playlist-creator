import streamlit as st
import google.generativeai as genai
from ytmusicapi import YTMusic
import json
import os

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
ytmusic = YTMusic("oauth.json")

def get_gemini_response(prompt_input):
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-001',
        system_instruction=[
            'Você é um expert DJ mundial.',
            'Sua tarefa é criar uma playlist de 30 músicas de acordo com o contexto.',
            'A resposta deve ser em formato JSON sendo uma sugestão de nome bem criativo e único para a playlist como chave principal e como valor uma lista de dicionarios com os campos "artist" e "music".'
        ],
        generation_config = genai.GenerationConfig(response_mime_type="application/json")
    )

    response = model.generate_content(prompt_input)
    return response.text

def get_music_id(artist_name, music_name):
    search_results = ytmusic.search(f"{artist_name} {music_name}",
                                    filter='songs')
    if search_results is not None:
        music_id = search_results[0]['videoId']
        return music_id
    else:
        print(f'{artist_name} {music_name} não encontrado!')

def create_music_playlist(gemini_response):
    data = json.loads(gemini_response)
    playlist_name = list(data.keys())[0]
    playlist_id = ytmusic.create_playlist(f'{playlist_name} by AI', f"Playlist {playlist_name} gerada por IA")

    list_music_id=[]
    for r in data.get(playlist_name):
         music_id = get_music_id(r['artist'], r['music'])
         if music_id is not None:
            list_music_id.append(music_id)
    
    ytmusic.add_playlist_items(playlist_id, list_music_id)

    print(f'Playlist {playlist_name} criada com sucesso')
    
    return playlist_name

st.header('Youtube Music Playlist Creator')
prompt = st.text_area('Descricao da playlist')
if st.button('Criar playlist'):
    response = get_gemini_response(prompt)
    playlist = create_music_playlist(response)
    st.text(f'Playlist {playlist} criada com sucesso!')