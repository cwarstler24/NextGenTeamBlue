from os import path as os_path
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from src.logger import logger

router = APIRouter(prefix="", tags=["pages"])


@router.get("/index/", response_class=HTMLResponse)
async def index_page():
    logger.event("GET /index")
    htmlpath = os_path.join(os_path.dirname(__file__), "../index.html")
    try:
        htmlresponse = open(htmlpath, "r", encoding="utf-8")
    except FileNotFoundError as exc:
        logger.event("File not found", level="warning")
        raise HTTPException(status_code=404, detail="File not found") from exc
    except Exception as e:
        logger.event(f"Error getting request: {e}", level="error")
        raise HTTPException(status_code=500, detail="Error getting request") from e

    logger.event("Returning index page")
    return HTMLResponse(content=htmlresponse.read())


@router.get("/index_test/", response_class=HTMLResponse)
async def index_test_page():
    logger.event("GET /index_test")
    htmlpath = os_path.join(os_path.dirname(__file__), "../index_test.html")
    try:
        htmlresponse = open(htmlpath, "r", encoding="utf-8")
    except FileNotFoundError as exc:
        logger.event("File not found", level="warning")
        raise HTTPException(status_code=404, detail="File not found") from exc
    except Exception as e:
        logger.event(f"Error getting request: {e}", level="error")
        raise HTTPException(status_code=500, detail="Error getting request") from e

    logger.event("Returning index test page")
    return HTMLResponse(content=htmlresponse.read())


@router.get("/Documentation/Logos/SwaB_Logo.png")
async def get_logo():
    logger.event("GET /Documentation/Logos/SwaB_Logo.png")
    image_path = os_path.join(os_path.dirname(__file__),
                              "../../Documentation/Logos/SwaB_Logo.png")
    if not os_path.exists(image_path):
        logger.event("Image not found", level="warning")
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)


@router.get("/Documentation/Logos/Action_Hero_Cotton_Swab.png")
async def get_action_hero_logo():
    logger.event("GET /Documentation/Logos/Action_Hero_Cotton_Swab.png")
    image_path = os_path.join(os_path.dirname(__file__),
                              "../../Documentation/Logos/Action_Hero_Cotton_Swab.png")
    if not os_path.exists(image_path):
        logger.event("Image not found", level="warning")
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)

@router.get("/favicon/")
async def get_ico():
    logger.event("GET /favicon.ico", level="trace")
    image_path = os_path.join(os_path.dirname(__file__),
                              "../../Documentation/Logos/favicon.ico")
    if not os_path.exists(image_path):
        logger.event("Image not found", level="warning")
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)

@router.get("/index_test.html/")
async def redirect_index_test_html():
    logger.event("GET /index_test.html/")
    return RedirectResponse(url="/index_test/")


@router.get("/index/index_test.html/")
async def redirect_index_index_test_html():
    logger.event("GET /index_test.html/")
    return RedirectResponse(url="/index_test/")


@router.get("/index.html/")
async def redirect_index_html():
    logger.event("GET /index.html/")
    return RedirectResponse(url="/index/")
