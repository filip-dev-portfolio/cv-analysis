import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from .config import (
    CV_DIR,
    JOB_DIR,
    MAX_CV_SIZE_MB,
    RESULT_DIR,
    ensure_directories,
)
from .document_parser import (
    DocumentParserError,
    extract_document,
)
from .matcher import matcher


# ---------------------------------------------------------------------------
# SETUP
# ---------------------------------------------------------------------------

ensure_directories()

app = FastAPI(
    title="CV Matcher",
    description="CV matching using Ollama and Qwen3 8B",
    version="1.0.0",
)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".md",
}


BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(
    directory=str(TEMPLATE_DIR)
)


# ---------------------------------------------------------------------------
# TEMPLATE HELPERS
# ---------------------------------------------------------------------------

def format_label(value: str) -> str:
    """
    Convert:

        matching_score

    into:

        Matching Score
    """

    return (
        value
        .replace("_", " ")
        .replace("-", " ")
        .title()
    )


templates.env.filters["format_label"] = format_label


# ---------------------------------------------------------------------------
# FILE VALIDATION
# ---------------------------------------------------------------------------

def validate_file(filename: str | None) -> Path:
    """
    Validate the uploaded filename and extension.
    """

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: {extension}. "
                f"Supported: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            ),
        )

    return Path(filename)


async def save_upload(
    upload: UploadFile,
    directory: Path,
) -> Path:
    """
    Save an uploaded file with a unique filename.
    """

    original_name = validate_file(
        upload.filename
    )

    unique_name = (
        f"{uuid.uuid4().hex}_"
        f"{original_name.name}"
    )

    destination = directory / unique_name

    contents = await upload.read()

    max_size = (
        MAX_CV_SIZE_MB * 1024 * 1024
    )

    if len(contents) > max_size:
        raise HTTPException(
            status_code=413,
            detail=(
                f"File is too large. Maximum size is "
                f"{MAX_CV_SIZE_MB} MB."
            ),
        )

    destination.write_bytes(contents)

    return destination


# ---------------------------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------------------------

@app.get("/")
async def index(request: Request):
    """
    Render the main CV Matcher page.
    """

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "result": None,
            "error": None,
            "cv_filename": None,
            "job_filename": None,
        },
    )


# ---------------------------------------------------------------------------
# HEALTH
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    """
    Simple health check for deployment platforms.
    """

    return {
        "status": "ok",
        "service": "cv-matcher",
    }


# ---------------------------------------------------------------------------
# MATCH
# ---------------------------------------------------------------------------

@app.post("/match")
async def match_cv(
    request: Request,
    cv: UploadFile = File(...),
    job: UploadFile = File(...),
):
    """
    Upload a CV and job description, extract their text,
    send them to the matcher, save the result, and render
    the result page.
    """

    try:

        # ---------------------------------------------------------------
        # SAVE CV
        # ---------------------------------------------------------------

        cv_path = await save_upload(
            cv,
            CV_DIR,
        )

        # ---------------------------------------------------------------
        # SAVE JOB
        # ---------------------------------------------------------------

        job_path = await save_upload(
            job,
            JOB_DIR,
        )

        # ---------------------------------------------------------------
        # EXTRACT DOCUMENTS
        # ---------------------------------------------------------------

        try:

            cv_text = extract_document(
                cv_path
            )

            job_text = extract_document(
                job_path
            )

        except DocumentParserError as exc:

            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={
                    "result": None,
                    "error": str(exc),
                    "cv_filename": cv.filename,
                    "job_filename": job.filename,
                },
            )

        # ---------------------------------------------------------------
        # CHECK CV TEXT
        # ---------------------------------------------------------------

        if not cv_text:

            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={
                    "result": None,
                    "error": (
                        "Could not extract any text "
                        "from the CV."
                    ),
                    "cv_filename": cv.filename,
                    "job_filename": job.filename,
                },
            )

        # ---------------------------------------------------------------
        # CHECK JOB TEXT
        # ---------------------------------------------------------------

        if not job_text:

            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={
                    "result": None,
                    "error": (
                        "Could not extract any text "
                        "from the job description."
                    ),
                    "cv_filename": cv.filename,
                    "job_filename": job.filename,
                },
            )

        # ---------------------------------------------------------------
        # MATCH WITH OLLAMA
        # ---------------------------------------------------------------

        try:

            result = await matcher.match(
                cv_text=cv_text,
                job_text=job_text,
            )

        except Exception as exc:

            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={
                    "result": None,
                    "error": f"Matching failed: {exc}",
                    "cv_filename": cv.filename,
                    "job_filename": job.filename,
                },
            )

        # ---------------------------------------------------------------
        # SAVE RESULT
        # ---------------------------------------------------------------

        result_id = uuid.uuid4().hex

        result_document = {
            "id": result_id,
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "cv_filename": cv.filename,
            "job_filename": job.filename,
            "result": result,
        }

        result_path = (
            RESULT_DIR / f"{result_id}.json"
        )

        result_path.write_text(
            json.dumps(
                result_document,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        # ---------------------------------------------------------------
        # DISPLAY RESULT
        # ---------------------------------------------------------------

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "result": result,
                "error": None,
                "cv_filename": cv.filename,
                "job_filename": job.filename,
            },
        )

    # -------------------------------------------------------------------
    # EXPECTED FASTAPI ERRORS
    # -------------------------------------------------------------------

    except HTTPException as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "result": None,
                "error": str(exc.detail),
                "cv_filename": cv.filename,
                "job_filename": job.filename,
            },
            status_code=exc.status_code,
        )

    # -------------------------------------------------------------------
    # UNEXPECTED ERRORS
    # -------------------------------------------------------------------

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "result": None,
                "error": f"An unexpected error occurred: {exc}",
                "cv_filename": cv.filename,
                "job_filename": job.filename,
            },
            status_code=500,
        )


# ---------------------------------------------------------------------------
# STORED RESULTS
# ---------------------------------------------------------------------------

@app.get("/results/{result_id}")
async def get_result(
    result_id: str,
):
    """
    Retrieve a previously stored matching result.
    """

    result_path = (
        RESULT_DIR / f"{result_id}.json"
    )

    if not result_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Result not found.",
        )

    try:

        return json.loads(
            result_path.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError as exc:

        raise HTTPException(
            status_code=500,
            detail="Stored result is invalid.",
        ) from exc
