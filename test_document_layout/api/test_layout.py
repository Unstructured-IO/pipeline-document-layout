import os
from pathlib import Path
from fastapi.testclient import TestClient

from unstructured_api_tools.pipelines.api_conventions import get_pipeline_path
from prepline_document_layout.api.app import app

DIRECTORY = Path(__file__).absolute().parent

SAMPLE_DOCS_DIRECTORY = os.path.join(DIRECTORY, "..", "..", "sample-docs")


LAYOUT_ROUTE = get_pipeline_path("layout", pipeline_family="document-layout", semver="0.0.1")

# def test_memo_api():
#     filename = os.path.join(SAMPLE_DOCS_DIRECTORY, "sample-memo.pdf")
#     app.state.limiter.reset()
#     client = TestClient(app)
#     response = client.post(
#         MEMO_ROUTE,
#         files={
#             "files": (
#                 filename,
#                 open(filename, "rb"),
#             )
#         },
#     )

#     assert response.status_code == 200
#     assert response.json() == EXPECTED_RESPONSE


def test_layout_pdf():
    filename = "/Users/benjamin/Documents/pipeline-document-layout/sample-docs/example.pdf"
    app.state.limiter.reset()
    client = TestClient(app)
    response = client.post(
        LAYOUT_ROUTE,
        headers={"Accept": "multipart/mixed"},
        files=[
            ("files", (filename, open(filename, "rb"), "application/pdf")),
        ],
    )

    assert response.status_code == 200
