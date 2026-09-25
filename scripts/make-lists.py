#!/usr/bin/env python3

from pathlib import Path
import subprocess
import json

# def create_pdf_book(filelist: Path):
#     output = filelist.with_suffix('.pdf')

#     cmd1 = ['chordpro', f'--filelist={filelist}', f'--output={output}', '--config=./config/settings.json']
#     # res1 = subprocess.run(cmd1, capture_output=True, text=True, check=True)
#     res1 = subprocess.run(cmd1, capture_output=True, text=True)
#     print(res1.stdout)
#     print(res1.stderr)

#     # 2. Bass konverzia s --decapo
#     # cmd2 = ['chordpro', src_file, '--output', dst_file_bass, '--decapo', '--config=./config/settings.json']
#     # res2 = subprocess.run(cmd2, capture_output=True, text=True, check=True)

#     # Vrátime výstupy na neskoršie vypísanie, aby sa nám nemiešali texty v konzole
#     # return src_file, res1.stdout + res2.stdout, res1.stderr + res2.stderr


# for filelist in Path("lists").glob('*.txt'):
#     create_pdf_book(filelist)

def get_output(path, suffix):
    output = path.with_suffix(suffix)
    return Path("books", *output.parts[1:])


def get_cover(data):
    if 'cover' in data:
        return [f"--cover={data['cover']}"]
    return []

def get_title(data):
    if 'cover' in data:
        return []

    if 'title' in data:
        return [f"--title={data['title']}"]

    return []

def get_songs_list(songs):
    return [s['path'] for s in songs]


def run_chordpro_cli(path, data):
    output_guitar = get_output(path, '.pdf')
    output_bass = get_output(path, '.bass.pdf')
    output_uke = get_output(path, '.uke.pdf')
    songs_list = get_songs_list(data['songs'])
    title_args = get_title(data)
    cover_args = get_cover(data)

    # 1. Guitar
    cmd1 = ['chordpro', *title_args, *cover_args, *songs_list, f'--output={output_guitar}', '--config=./config/settings.json']
    res1 = subprocess.run(cmd1, capture_output=True, text=True)
    print(res1.stdout)
    print(res1.stderr)

    # 2. Bass
    cmd2 = ['chordpro', '--diagrams=all', *title_args, *cover_args, *songs_list, '--decapo', f'--output={output_bass}', '--config=./config/bass.json']
    res2 = subprocess.run(cmd2, capture_output=True, text=True, check=True)

    print(res2.stdout)
    print(res2.stderr)

    # 3. Ukulele
    cmd2 = ['chordpro', '--diagrams=all', *title_args, *cover_args, *songs_list, '--decapo', f'--output={output_uke}', '--config=./config/ukulele.json']
    res2 = subprocess.run(cmd2, capture_output=True, text=True, check=True)

    print(res2.stdout)
    print(res2.stderr)


def create_songbook(path):
    with open(path, 'r') as f:
        data = json.load(f)

    run_chordpro_cli(path, data)

def create_complete_songbook():
    songs = []
    for song in Path("songs").glob('**/*.cho'):
        songs.append({ "path": str(song) })

    songbook = {
        "title": "Songbook",
        "cover": "songbooks/covers/songbook.pdf",
        "songs": list(sorted(songs, key=lambda x: x["path"]))
    }
    songbook_path = Path("songbooks/songbook.json")

    run_chordpro_cli(songbook_path, songbook)

for songbook in Path("songbooks").glob('*.json'):
    # create_songbook(songbook)
    pass

create_complete_songbook()
