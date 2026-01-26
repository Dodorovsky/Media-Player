import pytest
from unittest.mock import MagicMock, Mock, patch
#from tests.helpers import simulate_vlc_stopped, simulate_vlc_playing
 
 
def test_toggle_play_pause_vlc_starts_playback_when_stopped(mock_player):
    player, vlc_player = mock_player

    vlc_player.is_playing.return_value = False
    vlc_player.play = MagicMock()
    vlc_player.pause = MagicMock()

    player.toggle_play()

    vlc_player.play.assert_called_once()
    vlc_player.pause.assert_not_called()
    assert player.is_playing is True

def test_toggle_play_pause_vlc_pauses_when_playing(mock_player):
    player, vlc_player = mock_player

    vlc_player.is_playing.return_value = True
    vlc_player.play = MagicMock()
    vlc_player.pause = MagicMock()

    player.toggle_play()

    vlc_player.pause.assert_called_once()
    vlc_player.play.assert_not_called()
    assert player.is_playing is False




