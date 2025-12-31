from modules.playlist_manager import load_playlist, create_playlist, add_to_playlist
import os
import pytest

def test_load_playlist_empty_file(tmp_path):
    playlist = tmp_path / "playlist.txt"
    playlist.write_text("", encoding="utf-8")

    result = load_playlist(playlist)

    assert isinstance(result, list)
    assert result == []

def test_load_playlist_with_content(tmp_path):
    playlist = tmp_path / "playlist.txt"
    playlist.write_text("ruta1.mp3\nruta2.mp4\n", encoding="utf-8")

    result = load_playlist(str(playlist))

    assert result == ["ruta1.mp3", "ruta2.mp4"]
    
def test_create_playlist_creates_empty_file(tmp_path):
    playlist = tmp_path / "new_playlist.txt"

    create_playlist(str(playlist))

    assert playlist.exists()
    assert playlist.read_text(encoding="utf-8") == ""

def test_add_to_playlist_adds_new(tmp_path):
    playlist = tmp_path / "playlist.txt"
    playlist.write_text("existente.mp3\n", encoding="utf-8")

    new, repeated = add_to_playlist(str(playlist), ["nuevo.mp3", "existente.mp3"])

    assert new == ["nuevo.mp3"]
    assert repeated == ["existente.mp3"]

    contenido = playlist.read_text(encoding="utf-8").splitlines()
    assert "existente.mp3" in contenido
    assert "nuevo.mp3" in contenido
    
@pytest.mark.parametrize(
    "existing, incoming, expected_new, expected_repeated",
    [
        ([], ["a"], ["a"], []),
        (["a"], ["a"], [], ["a"]),
        (["a"], ["a", "b"], ["b"], ["a"]),
        (["a", "b"], ["b", "c"], ["c"], ["b"]),
    ]
)
def test_add_to_playlist_parametrized(tmp_path, existing, incoming,
                                      expected_new, expected_repeated):
    playlist = tmp_path / "playlist.txt"
    playlist.write_text("\n".join(existing), encoding="utf-8")

    new, repeated = add_to_playlist(str(playlist), incoming)

    assert new == expected_new
    assert repeated == expected_repeated

