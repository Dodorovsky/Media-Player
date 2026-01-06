import pytest
from unittest.mock import MagicMock, patch
from player import PlaylistPlayer

@pytest.fixture
def mock_player():
    # Tkinter root mock (prevents errors due to .bind)
    mock_root = MagicMock()
    mock_root.bind = MagicMock()

    # VLC Player Mock
    mock_media_player = MagicMock()

    with (
        patch("player.vlc.Instance") as mock_vlc_instance,
        patch("player.setup_ui"),                     # evita cargar imágenes
        patch("player.PlaylistPlayer.bind_events"),   # evita binds reales
        patch("player.PlaylistPlayer.update_time"),   # evita loop .after()
    ):
        # Configure the VLC mock
        instance = MagicMock()
        instance.media_player_new.return_value = mock_media_player
        mock_vlc_instance.return_value = instance

        # Create the player with patched dependencies
        player = PlaylistPlayer(mock_root)

        # Mocks for all UI elements used in stop()
        player.style = MagicMock()
        player.mp6_label_left = MagicMock()
        player.mp6_label_right = MagicMock()
        player.time_slider = MagicMock()
        player.current_time_label = MagicMock()
        player.total_time_label = MagicMock()
        player.volume_label = MagicMock()
        player.play_pause_button = MagicMock()
        player.stop_button = MagicMock()
        
        # Mocks of images used in stop() 
        player.mp6_off = MagicMock() 
        player.play_off = MagicMock() 
        player.stop_on = MagicMock()
        
        player.mute_button = MagicMock()
        player.volume_label_frame = MagicMock()
        

    return player, mock_media_player

    
def test_play_calls_vlc_play(mock_player):
    player, mock_vlc = mock_player
    player.play()
    mock_vlc.play.assert_called_once()
    
def test_pause_calls_vlc_pause(mock_player):
    player, mock_vlc = mock_player
    player.pause()
    mock_vlc.pause.assert_called_once()
    
def test_stop_calls_vlc_stop(mock_player):
    player, mock_vlc = mock_player
    player.stop()
    mock_vlc.stop.assert_called_once()
    
def test_load_calls_set_media(mock_player):
    player, mock_vlc = mock_player

    fake_path = "song.mp3"

    # Pretend that media_new returns a fake media object
    fake_media = MagicMock()
    player.vlc_instance.media_new.return_value = fake_media

    player.load_media_file(fake_path)

    # Verify that media_new was called with the correct path
    player.vlc_instance.media_new.assert_called_once_with(fake_path)

    # Verify that set_media was called with the fake media
    mock_vlc.set_media.assert_called_once_with(fake_media)

def test_set_volume_calls_vlc_volume(mock_player):
    player, mock_vlc = mock_player

    volume_value = 0
    player.set_volume(volume_value)

    mock_vlc.audio_set_volume.assert_called_once_with(volume_value)


def test_set_volume_unmutes_when_volume_above_one(mock_player):
    player, mock_vlc = mock_player

    player.is_muted = True  # estado inicial

    fake_volume = 50
    player.set_volume(fake_volume)

    # VLC recibe el volumen
    mock_vlc.audio_set_volume.assert_called_once_with(fake_volume)

    # UI cambia a estado "unmuted"
    player.volume_label.config.assert_any_call(fg="#CAFFFE")
    player.mute_button.config.assert_called_once_with(bg="#3E3838")
    player.volume_label_frame.config.assert_called_once_with(fg="green")
    player.style.configure.assert_called_with('TScale', troughcolor="#AC8433")

    # Flag interno actualizado
    assert player.is_muted is False
    
def test_set_volume_mutes_when_volume_zero(mock_player):
    player, mock_vlc = mock_player

    player.is_muted = False  # estado inicial

    fake_volume = 0
    player.set_volume(fake_volume)

    # VLC recibe el volumen
    mock_vlc.audio_set_volume.assert_called_once_with(fake_volume)

    # UI cambia a estado "muted"
    player.mute_button.config.assert_called_once_with(bg="#D21A1A")
    player.style.configure.assert_called_with('TScale', troughcolor="#D21A1A")

    # Flag interno actualizado
    assert player.is_muted is True

