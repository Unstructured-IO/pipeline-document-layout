import os
from pathlib import Path
from fastapi.testclient import TestClient
import pytest
from unstructured_api_tools.pipelines.api_conventions import get_pipeline_path
from prepline_document_layout.api.app import app

DIRECTORY = Path(__file__).absolute().parent

SAMPLE_DOCS_DIRECTORY = os.path.join(DIRECTORY, "..", "..", "sample-docs")

LAYOUT_ROUTE = get_pipeline_path("layout", pipeline_family="document-layout", semver="1.0.0")


@pytest.mark.parametrize(
    "file_type, headers,model_type, file, expected_response_code",
    [
        ("sometype/pdf", {"Accept": "multipart/mixed"}, None, "example.pdf", 404),
        (
            "application/pdf",
            {"Accept": "multipart/mixed"},
            {"model_type": "badtypemodel"},
            "example.pdf",
            422,
        ),
    ],
)
def test_with_invalid_values(file_type, headers, model_type, file, expected_response_code):
    filename = os.path.join(SAMPLE_DOCS_DIRECTORY, file)
    client = TestClient(app)

    response = client.post(
        LAYOUT_ROUTE,
        headers=headers,
        files=[
            ("files", (filename, open(filename, "rb"), file_type)),
        ],
        data=model_type,
    )
    assert response.status_code == expected_response_code


def test_non_acceptable_media_type():
    filename = "../pipeline-document-layout/sample-docs/example.pdf"
    client = TestClient(app)

    response = client.post(
        LAYOUT_ROUTE,
        headers={"Accept": "badtype/mixed"},
        files=[
            ("files", (filename, open(filename, "rb"), "application/pdf")),
            ("files", (filename, open(filename, "rb"), "application/pdf")),
        ],
    )
    assert response.status_code == 406


def test_without_file():
    client = TestClient(app)
    response = client.post(LAYOUT_ROUTE, headers={"Accept": "badtype/mixed"}, files=[])
    assert response.status_code == 400


@pytest.mark.parametrize(
    "file_type, model_type, file, expected_response_code",
    [
        ("application/pdf", [], "example.pdf", 200),
        ("application/pdf", "yolox", "example.pdf", 200),
        ("application/pdf", [], "example-multipage.pdf", 200),
        ("application/pdf", "yolox", "example-multipage.pdf", 200),
        ("image/png", [], "example.png", 200),
        ("image/png", "yolox", "example.png", 200),
    ],
)
def test_files(file_type, model_type, file, expected_response_code):
    filename = os.path.join(SAMPLE_DOCS_DIRECTORY, file)
    client = TestClient(app)

    response = client.post(
        LAYOUT_ROUTE,
        headers={"Accept": "multipart/mixed"},
        files=[
            ("files", (filename, open(filename, "rb"), file_type)),
        ],
        data={"model_type": model_type},
    )
    assert response.status_code == expected_response_code


def test_healtcheck():
    client = TestClient(app)
    response = client.get("/healthcheck")
    assert "HEALTHCHECK STATUS: EVERYTHING OK!" in response.content.decode()
    assert response.status_code == 200


@pytest.mark.parametrize(
    "file_type, headers, file, expected_response_code",
    [
        ("application/pdf", [], "example.pdf", 200),
        ("application/pdf", {"Accept": "multipart/mixed"}, "example.pdf", 200),
        ("image/png", [], "example.png", 200),
        ("image/png", {"Accept": "multipart/mixed"}, "example.png", 200),
    ],
)
def test_multiple_files(file_type, headers, file, expected_response_code):
    filename = os.path.join(SAMPLE_DOCS_DIRECTORY, file)
    client = TestClient(app)

    response = client.post(
        LAYOUT_ROUTE,
        headers=headers,
        files=[
            ("files", (filename, open(filename, "rb"), file_type)),
            ("files", (filename, open(filename, "rb"), file_type)),
        ],
    )
    assert response.status_code == expected_response_code
