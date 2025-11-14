from .init_db import main
import pytest
import os


@pytest.mark.skipif(os.environ.get("PYTEST_CI_MODE"), reason="does not work in CI pipeline")
def test_initialize_app_db():
    main()
    return
