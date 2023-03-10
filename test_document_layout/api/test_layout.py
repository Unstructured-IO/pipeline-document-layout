import os
from pathlib import Path
from fastapi.testclient import TestClient

from unstructured_api_tools.pipelines.api_conventions import get_pipeline_path
from prepline_document_layout.api.app import app

DIRECTORY = Path(__file__).absolute().parent

SAMPLE_DOCS_DIRECTORY = os.path.join(DIRECTORY, "..", "..", "sample-docs")

LAYOUT_ROUTE = get_pipeline_path("layout", pipeline_family="document-layout", semver="1.0.0")


def test_healthcheck():
    client = TestClient(app)
    response = client.get("/healthcheck")
    assert response.status_code == 200


def test_unknown_filetype():
    filename = "../pipeline-document-layout/sample-docs/example.pdf"
    client = TestClient(app)

    response = client.post(
        LAYOUT_ROUTE,
        headers={"Accept": "multipart/mixed"},
        files=[
            ("files", (filename, open(filename, "rb"), "sometipe/pdf")),
        ],
    )
    assert response.status_code == 404


def test_unknown_modeltype():
    filename = "../pipeline-document-layout/sample-docs/example.pdf"
    client = TestClient(app)

    response = client.post(
        LAYOUT_ROUTE,
        headers={"Accept": "multipart/mixed"},
        files=[
            ("files", (filename, open(filename, "rb"), "application/pdf")),
        ],
        data={"model_type": "badtypemodel"},
    )
    assert response.status_code == 422


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


def test_layout_pdf():
    filename = "../pipeline-document-layout/sample-docs/example.pdf"
    client = TestClient(app)

    response = client.post(
        LAYOUT_ROUTE,
        headers={"Accept": "multipart/mixed"},
        files=[
            ("files", (filename, open(filename, "rb"), "application/pdf")),
        ],
        data={"model_type": "yolox"},
    )
    assert response.status_code == 200


def test_layout_multipage_pdf():
    filename = "../pipeline-document-layout/sample-docs/example-multipage.pdf"
    client = TestClient(app)

    response = client.post(
        LAYOUT_ROUTE,
        headers={"Accept": "multipart/mixed"},
        files=[
            ("files", (filename, open(filename, "rb"), "application/pdf")),
        ],
    )
    assert response.status_code == 200


def test_layout_image():
    filename = "../pipeline-document-layout/sample-docs/example.png"
    client = TestClient(app)

    response = client.post(
        LAYOUT_ROUTE,
        headers={"Accept": "multipart/mixed"},
        files=[
            ("files", (filename, open(filename, "rb"), "image/png")),
        ],
    )
    assert response.status_code == 200


def test_healtcheck():
    client = TestClient(app)
    response = client.get("/healthcheck")
    assert "HEALTHCHECK STATUS: EVERYTHING OK!" in response.content.decode()
    assert response.status_code == 200


def test_multiple_files_type_content():
    filename = "../pipeline-document-layout/sample-docs/example.png"
    client = TestClient(app)

    response = client.post(
        LAYOUT_ROUTE,
        headers={"Accept": "multipart/mixed"},
        files=[
            ("files", (filename, open(filename, "rb"), "image/png")),
            ("files", (filename, open(filename, "rb"), "image/png")),
        ],
    )
    assert response.status_code == 200


def test_multiple_files_pdf():
    filename = "../pipeline-document-layout/sample-docs/example.pdf"
    client = TestClient(app)

    response = client.post(
        LAYOUT_ROUTE,
        files=[
            ("files", (filename, open(filename, "rb"), "application/pdf")),
            ("files", (filename, open(filename, "rb"), "application/pdf")),
        ],
    )
    assert response.status_code == 200
