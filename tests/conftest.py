import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def patched_image_utils():
    fake_image = MagicMock(name="FakePILImage")
    fake_resized = MagicMock(name="FakeResizedImage")
    fake_photo = MagicMock(name="FakePhotoImage")

    fake_image.resize.return_value = fake_resized

    with patch("modules.image_utils.resource_path", return_value="fake/path.png") as mock_resource, \
         patch("modules.image_utils.Image.open", return_value=fake_image) as mock_open, \
         patch("modules.image_utils.ImageTk.PhotoImage", return_value=fake_photo) as mock_photo:

        yield {
            "fake_image": fake_image,
            "fake_resized": fake_resized,
            "fake_photo": fake_photo,
            "mock_resource": mock_resource,
            "mock_open": mock_open,
            "mock_photo": mock_photo,
        }
