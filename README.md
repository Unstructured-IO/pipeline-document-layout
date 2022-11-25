<h3 align="center">
  <img src="img/unstructured_logo.png" height="200">
</h3>

<h3 align="center">
  <p>Pre-Processing Pipeline for Layout Detection</p>
</h3>


The description for the pipeline repository goes here.
The API is hosted at `https://api.unstructured.io`.

## Developer Quick Start

* Using `pyenv` to manage virtualenv's is recommended
	* Mac install instructions. See [here](https://github.com/Unstructured-IO/community#mac--homebrew) for more detailed instructions.
		* `brew install pyenv-virtualenv`
	  * `pyenv install 3.8.15`
  * Linux instructions are available [here](https://github.com/Unstructured-IO/community#linux).

  * Create a virtualenv to work in and activate it, e.g. for one named `document_layout`:

	`pyenv  virtualenv 3.8.15 document_layout` <br />
	`pyenv activate document_layout`

* Run `make install`
* Run `pip install 'git+https://github.com/facebookresearch/detectron2.git@v0.4#egg=detectron2'`
* Start a local jupyter notebook server with `make run-jupyter` <br />
	**OR** <br />
	just start the fast-API locally with `make run-web-app`

#### Extracting whatever from some type of document

For example:
```
curl -X 'POST' \
  'http://localhost:8000/document-layout/v1.0.0/layout' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@sample-docs/example.png' -F 'model_type=yolox'| jq -C . | less -R
```

Where `files` includes the file to process, `model_type` can be 'default' (or blank) or 'yolox',
also is possible to use `force_ocr` to auto in order to try text extraction from your file, or
'true', in which case OCR will be used.

### Generating Python files from the pipeline notebooks

You can generate the FastAPI APIs from your pipeline notebooks by running `make generate-api`.

## Security Policy

See our [security policy](https://github.com/Unstructured-IO/pipeline-document_layout/security/policy) for
information on how to report security vulnerabilities.

## Learn more

| Section | Description |
|-|-|
| [Unstructured Community Github](https://github.com/Unstructured-IO/community) | Information about Unstructured.io community projects  |
| [Unstructured Github](https://github.com/Unstructured-IO) | Unstructured.io open source repositories |
| [Company Website](https://unstructured.io) | Unstructured.io product and company info |
