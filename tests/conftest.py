import pytest
from unittest.mock import patch, MagicMock
from player import PlaylistPlayer

# ============================================================
#  FIXTURE: patched_image_utils
#  - Mockea PIL and ImageTk to avoid loading real images
#  - It is used in tests that need icons or images
# ============================================================
@pytest.fixture
def patched_image_utils():
    fake_image = MagicMock(name="FakePILImage")
    fake_resized = MagicMock(name="FakeResizedImage")
    fake_photo = MagicMock(name="FakePhotoImage")

    fake_image.resize.return_value = fake_resized

    with (
        patch("modules.image_utils.resource_path", return_value="fake/path.png") as mock_resource,
        patch("modules.image_utils.Image.open", return_value=fake_image) as mock_open,
        patch("modules.image_utils.ImageTk.PhotoImage", return_value=fake_photo) as mock_photo
    ):
        yield {
            "fake_image": fake_image,
            "fake_resized": fake_resized,
            "fake_photo": fake_photo,
            "mock_resource": mock_resource,
            "mock_open": mock_open,
            "mock_photo": mock_photo,
        }


# ============================================================
#  FIXTURE: mock_player_real
#  - REAL Player (real logic)
#  - Mocke ONLY VLC and Tkinter root
#  - Ideal for tests that need to prove real errors
# ============================================================
@pytest.fixture
def mock_player_real(mocker):
    mock_root = MagicMock()
    mock_root.bind = MagicMock()
    mock_root.after = MagicMock()

    player = PlaylistPlayer(mock_root)

    # Mockear SOLO VLC
    player.vlc_instance = mocker.Mock()
    player.player = mocker.Mock()

    return player


# ============================================================
#  FIXTURE: mock_player
#  - Completely isolated player
#  - Mockea UI, VLC and methods that should not be executed
#  - Ideal for tests that do NOT want real logic
# ============================================================
@pytest.fixture
def mock_player():
    mock_root = MagicMock()
    mock_root.bind = MagicMock()

    mock_media_player = MagicMock()

    with (
        patch("player.vlc.Instance") as mock_vlc_instance,
        patch("player.setup_ui"),
        patch("player.PlaylistPlayer.bind_events"),
        patch("player.PlaylistPlayer.update_time", return_value=None),
        patch("player.PlaylistPlayer.init_eq", return_value=None),
        patch("player.PlaylistPlayer.set_duration", return_value=None),
        patch("player.PlaylistPlayer.exit_fullscreen_video", return_value=None),
        patch("player.PlaylistPlayer.start_eq_light_loop", return_value=None),
        patch("player.PlaylistPlayer.force_layout_refresh", return_value=None),
        patch("player.PlaylistPlayer.track_mouse", return_value=None),
        patch("player.PlaylistPlayer.breathe_hal", return_value=None),
    ):
        # Mock VLC instance
        instance = MagicMock()
        instance.media_player_new.return_value = mock_media_player
        mock_vlc_instance.return_value = instance

        # Crear player
        player = PlaylistPlayer(mock_root)
        player.is_playing = False

        # Prevent after() from running real loops
        player.root.after = MagicMock()

        # UI mocks
        player.style = MagicMock()
        player.mp6_label_left = MagicMock()
        player.mp6_label_right = MagicMock()
        player.time_slider = MagicMock()
        player.current_time_label = MagicMock()
        player.total_time_label = MagicMock()
        player.volume_label = MagicMock()
        player.play_pause_button = MagicMock()
        player.stop_button = MagicMock()
        player.mute_button = MagicMock()
        player.volume_label_frame = MagicMock()
        player.listbox = MagicMock()
        player.video_frame = MagicMock()
        player.stop_off = MagicMock()

        # Listbox behavior
        player.listbox.selection_clear = MagicMock()
        player.listbox.selection_set = MagicMock()
        player.listbox.activate = MagicMock()

        # VLC player mock
        player.player = MagicMock()
        player.player.play = MagicMock()
        player.player.get_time = MagicMock()
        
        player.play_from_selection = MagicMock()

        # Images
        player.mp6 = MagicMock()
        player.mp6_off = MagicMock()
        player.pause_big = MagicMock()
        player.play_off = MagicMock()
        player.stop_on = MagicMock()

        # Flags
        player.slider_dragging = False
        player.updating_slider = False

    return player, player.player
