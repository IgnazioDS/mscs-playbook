from src.cv.mini_project.defect_detection import run_defect_detection
from src.cv.mini_project.document_ocr_lite import run_doc_ocr_lite
from src.cv.mini_project.shelf_availability import run_shelf_availability


def test_defect_detect_smoke():
    output = run_defect_detection(seed=42, iou=0.5)
    assert "task: defect-detect" in output
    assert "metrics: precision=" in output
    assert "recall=" in output


def test_doc_ocr_lite_smoke():
    output = run_doc_ocr_lite(seed=42)
    assert "task: doc-ocr-lite" in output
    assert "metrics: precision=" in output


def test_shelf_availability_smoke():
    output = run_shelf_availability(seed=42)
    assert "task: shelf-availability" in output
    assert "confusion_matrix" in output
