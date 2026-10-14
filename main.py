import os
from datetime import datetime
from typing import Optional
from urllib.parse import quote, urlencode

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

import crud
from auth import create_access_token, verify_password, verify_token
from database import SessionLocal, create_tables, get_db
from helpers import group_order_items, money, result_flag, whatsapp_number
from schemas import CategoryIn, OrderIn, PanelIn, PatientIn, TestIn

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECURE_COOKIES = os.getenv("SECURE_COOKIES", "false").lower() == "true"

app = FastAPI(title="Lab Management System", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
templates.env.globals.update(group_order_items=group_order_items, result_flag=result_flag)
templates.env.filters["money"] = money


def init_db():
    create_tables()
    with SessionLocal() as db:
        username = os.getenv("ADMIN_USERNAME", "admin")
        if not crud.get_admin_user(db, username):
            crud.create_admin_user(db, username, os.getenv("ADMIN_PASSWORD", "admin123"))


init_db()


# ── Helpers ──────────────────────────────────────────────────────────────────
def get_current_user(request: Request) -> str:
    username = verify_token(request.cookies.get("access_token", ""))
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return username


def render(request: Request, template: str, **context):
    return templates.TemplateResponse(request, template, context)


def redirect(url: str, msg: Optional[str] = None, error: Optional[str] = None):
    params = {k: v for k, v in (("msg", msg), ("error", error)) if v}
    return RedirectResponse(f"{url}?{urlencode(params)}" if params else url, status_code=303)


def get_order_or_404(db: Session, order_id: int):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="This order does not exist.")
    return order


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 401:
        return RedirectResponse("/login", status_code=303)
    if request.url.path.startswith("/api/"):
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
    return templates.TemplateResponse(
        request, "error.html", {"message": exc.detail, "user": None}, status_code=exc.status_code
    )


# ── Auth ─────────────────────────────────────────────────────────────────────
@app.get("/")
async def root(request: Request):
    return RedirectResponse("/dashboard" if verify_token(request.cookies.get("access_token", "")) else "/login")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return render(request, "login.html")


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    admin = crud.get_admin_user(db, username.strip())
    if not admin or not verify_password(password, admin.hashed_password):
        return render(request, "login.html", error="Incorrect username or password.", username=username)
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("access_token", create_access_token(admin.username), httponly=True, samesite="lax", secure=SECURE_COOKIES)
    return response


@app.get("/logout")
async def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("access_token")
    return response


# ── Dashboard ────────────────────────────────────────────────────────────────
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return render(
        request, "dashboard.html", user=user,
        stats=crud.get_dashboard_stats(db),
        pending_orders=crud.get_orders(db, status="pending", limit=8),
    )


# ── Patients ─────────────────────────────────────────────────────────────────
@app.get("/patients", response_class=HTMLResponse)
async def patients_page(request: Request, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return render(request, "patients.html", user=user, patients=crud.get_patients(db))


@app.post("/patients")
async def create_patient(
    name: str = Form(...), age: int = Form(...), gender: str = Form(...), phone: str = Form(...),
    user: str = Depends(get_current_user), db: Session = Depends(get_db),
):
    crud.create_patient(db, PatientIn(name=name.strip(), age=age, gender=gender, phone=phone.strip()))
    return redirect("/patients", msg="Patient added")


@app.post("/api/patients")
async def create_patient_api(
    name: str = Form(...), age: int = Form(...), gender: str = Form(...), phone: str = Form(...),
    user: str = Depends(get_current_user), db: Session = Depends(get_db),
):
    patient = crud.create_patient(db, PatientIn(name=name.strip(), age=age, gender=gender, phone=phone.strip()))
    return {"id": patient.id, "name": patient.name, "age": patient.age, "gender": patient.gender, "phone": patient.phone}


@app.post("/patients/{patient_id}/edit")
async def update_patient(
    patient_id: int,
    name: str = Form(...), age: int = Form(...), gender: str = Form(...), phone: str = Form(...),
    user: str = Depends(get_current_user), db: Session = Depends(get_db),
):
    crud.update_patient(db, patient_id, PatientIn(name=name.strip(), age=age, gender=gender, phone=phone.strip()))
    return redirect("/patients", msg="Patient updated")


@app.post("/patients/{patient_id}/delete")
async def delete_patient(patient_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        crud.delete_patient(db, patient_id)
    except crud.InUseError as e:
        return redirect("/patients", error=str(e))
    return redirect("/patients", msg="Patient deleted")


# ── Test catalog ─────────────────────────────────────────────────────────────
@app.get("/tests", response_class=HTMLResponse)
async def tests_page(request: Request, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return render(
        request, "tests.html", user=user,
        categories=crud.get_test_categories(db),
        panels=crud.get_panels(db),
        standalone_tests=crud.get_standalone_tests(db),
    )


@app.post("/test-categories")
async def create_category(name: str = Form(...), user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.create_test_category(db, CategoryIn(name=name.strip()))
    return redirect("/tests", msg="Category added")


def _test_form(
    name: str = Form(...),
    price: float = Form(0.0),
    unit: Optional[str] = Form(None),
    reference_range: Optional[str] = Form(None),
    category_id: int = Form(...),
    panel_id: Optional[str] = Form(None),
) -> TestIn:
    return TestIn(
        name=name.strip(), price=price,
        unit=(unit or "").strip() or None,
        reference_range=(reference_range or "").strip() or None,
        category_id=category_id,
        panel_id=int(panel_id) if panel_id else None,
    )


@app.post("/tests")
async def create_test(data: TestIn = Depends(_test_form), user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.create_test(db, data)
    return redirect("/tests", msg="Test added")


@app.post("/tests/{test_id}/edit")
async def update_test(test_id: int, data: TestIn = Depends(_test_form), user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.update_test(db, test_id, data)
    return redirect("/tests", msg="Test updated")


@app.post("/tests/{test_id}/delete")
async def delete_test(test_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        crud.delete_test(db, test_id)
    except crud.InUseError as e:
        return redirect("/tests", error=str(e))
    return redirect("/tests", msg="Test deleted")


def _panel_form(name: str = Form(...), description: Optional[str] = Form(None), price: float = Form(0.0)) -> PanelIn:
    return PanelIn(name=name.strip(), description=(description or "").strip() or None, price=price)


@app.post("/panels")
async def create_panel(data: PanelIn = Depends(_panel_form), user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.create_panel(db, data)
    return redirect("/tests", msg="Test group added")


@app.post("/panels/{panel_id}/edit")
async def update_panel(panel_id: int, data: PanelIn = Depends(_panel_form), user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.update_panel(db, panel_id, data)
    return redirect("/tests", msg="Test group updated")


@app.post("/panels/{panel_id}/delete")
async def delete_panel(panel_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        crud.delete_panel(db, panel_id)
    except crud.InUseError as e:
        return redirect("/tests", error=str(e))
    return redirect("/tests", msg="Test group deleted")


# ── Orders ───────────────────────────────────────────────────────────────────
@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return render(request, "orders.html", user=user, orders=crud.get_orders(db))


@app.get("/orders/new", response_class=HTMLResponse)
async def new_order_page(
    request: Request, patient_id: Optional[int] = None,
    user: str = Depends(get_current_user), db: Session = Depends(get_db),
):
    patients = [
        {"id": p.id, "name": p.name, "age": p.age, "gender": p.gender, "phone": p.phone}
        for p in crud.get_patients(db)
    ]
    panels = [
        {
            "id": p.id, "name": p.name, "price": p.price,
            "category": p.category.name if p.category else "Other",
            "tests": [t.name for t in p.tests],
        }
        for p in crud.get_panels(db)
    ]
    tests = [
        {"id": t.id, "name": t.name, "price": t.price, "category": t.category.name}
        for t in crud.get_standalone_tests(db)
    ]
    return render(
        request, "new_order.html", user=user,
        catalog={"patients": patients, "panels": panels, "tests": tests, "selectedPatientId": patient_id},
    )


@app.post("/orders")
async def create_order(
    request: Request,
    patient_id: int = Form(...),
    referred_by: Optional[str] = Form(None),
    sample_collected_at: Optional[str] = Form(None),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    form = await request.form()
    test_ids = [int(i) for i in form.getlist("test_ids")]
    panel_ids = [int(i) for i in form.getlist("panel_ids")]
    if not test_ids and not panel_ids:
        return redirect("/orders/new", error="Please select at least one test.")

    try:
        sample_date = datetime.fromisoformat(sample_collected_at) if sample_collected_at else None
    except ValueError:
        sample_date = None

    order = crud.create_order(db, OrderIn(
        patient_id=patient_id, test_ids=test_ids, panel_ids=panel_ids,
        referred_by=(referred_by or "").strip() or None, sample_collected_at=sample_date,
    ))
    return redirect(f"/orders/{order.id}", msg="Order placed. You can now enter results or print the invoice.")


@app.get("/orders/{order_id}", response_class=HTMLResponse)
async def order_detail_page(request: Request, order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return render(request, "order_detail.html", user=user, order=get_order_or_404(db, order_id))


@app.get("/orders/{order_id}/invoice", response_class=HTMLResponse)
async def invoice_page(request: Request, order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return render(request, "invoice.html", user=user, order=get_order_or_404(db, order_id))


@app.post("/orders/{order_id}/results")
async def save_results(request: Request, order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    order = get_order_or_404(db, order_id)
    crud.save_results(db, order, await request.form())
    if order.status == "completed":
        return redirect(f"/reports/{order_id}", msg="Results updated")
    return redirect(f"/orders/{order_id}", msg="Results saved")


@app.post("/orders/{order_id}/complete")
async def complete_order(request: Request, order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    order = get_order_or_404(db, order_id)
    crud.save_results(db, order, await request.form())
    crud.complete_order(db, order)
    return redirect(f"/reports/{order_id}", msg="Report is ready")


@app.post("/orders/{order_id}/delete")
async def delete_order(order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    order = get_order_or_404(db, order_id)
    if order.status != "pending":
        return redirect(f"/orders/{order_id}", error="Completed orders cannot be deleted.")
    crud.delete_order(db, order)
    return redirect("/orders", msg="Order deleted")


# ── Reports ──────────────────────────────────────────────────────────────────
@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return render(request, "reports.html", user=user, orders=crud.get_orders(db, status="completed"))


@app.get("/reports/{order_id}", response_class=HTMLResponse)
async def report_page(request: Request, order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    order = get_order_or_404(db, order_id)
    if order.status != "completed":
        return redirect(f"/orders/{order_id}", error="Enter the results and complete this order to see its report.")

    whatsapp_url = None
    phone = whatsapp_number(order.patient.phone)
    if phone:
        link = crud.get_or_create_share_link(db, order)
        report_url = str(request.url_for("shared_report", token=link.token))
        message = f"Hello! Your lab report from Khalid Medical Laboratory is ready: {report_url}"
        whatsapp_url = f"https://wa.me/{phone}?text={quote(message, safe='')}"
    return render(request, "report_detail.html", user=user, order=order, whatsapp_url=whatsapp_url)


@app.get("/r/{token}", response_class=HTMLResponse, name="shared_report")
async def shared_report_page(request: Request, token: str, db: Session = Depends(get_db)):
    order = crud.get_order_by_share_token(db, token)
    if not order or order.status != "completed":
        raise HTTPException(status_code=404, detail="This report link is invalid or has expired. Please contact the laboratory.")
    return render(request, "report_detail.html", user=None, order=order, public=True)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "8000")))
