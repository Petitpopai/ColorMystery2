import pytest
from core import process_image

def test_process_image(capsys):
    # Call process_image with dummy parameters and check output.
    process_image("dummy.png", "number", "easy", "low", "numbers", "auto", 1024, 1024)
    captured = capsys.readouterr().out
    assert "Processing dummy.png" in captured

if __name__ == "__main__":
    pytest.main()