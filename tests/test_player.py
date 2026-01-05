import pytest
from unittest.mock import MagicMock, patch
from player import PlaylistPlayer

@pytest.fixture
def mock_player():
    # Mock del root de Tkinter (evita errores por .bind)
    mock_root = MagicMock()
    mock_root.bind = MagicMock()

    # Mock del reproductor VLC
    mock_media_player = MagicMock()

    with (
        patch("player.vlc.Instance") as mock_vlc_instance,
        patch("player.setup_ui"),                     # evita cargar imágenes
        patch("player.PlaylistPlayer.bind_events"),   # evita binds reales
        patch("player.PlaylistPlayer.update_time"),   # evita loop .after()
    ):
        # Configurar el mock de VLC
        instance = MagicMock()
        instance.media_player_new.return_value = mock_media_player
        mock_vlc_instance.return_value = instance

        # Crear el reproductor con dependencias parcheadas
        player = PlaylistPlayer(mock_root)

        # 🔥 Mocks para todos los elementos de UI usados en stop()
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
   
    