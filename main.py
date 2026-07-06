import json
import os
from datetime import timedelta
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markupsafe import Markup
from sqlalchemy.orm import Session

import crud
import schemas
from auth import verify_password, create_access_token, verify_token
from database import get_db, create_tables

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Lab Management System",
    docs_url=None,
    redoc_url=None
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")
templates.env.globals["group_order_items"] = crud.group_order_items
templates.env.filters["tojson"] = lambda value: Markup(json.dumps(value))

# Create database tables
create_tables()

# Initialize admin user
def init_admin():
    db = next(get_db())
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    
    if not crud.get_admin_user(db, admin_username):
        crud.create_admin_user(db, admin_username, admin_password)
    db.close()

init_admin()

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token or not (username := verify_token(token)):
        raise HTTPException(status_code=401, detail="Not authenticated")
    return username

# Routes
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    try:
        get_current_user(request)
        return RedirectResponse(url="/dashboard", status_code=302)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    admin = crud.get_admin_user(db, username)
    if not admin or not verify_password(password, admin.hashed_password):
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Incorrect username or password. Please try again."
        })
    
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=timedelta(hours=24)
    )
    
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key="access_token")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    stats = crud.get_dashboard_stats(db)
    recent_orders = crud.get_orders(db, limit=5)
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": user,
        "stats": stats,
        "recent_orders": recent_orders,
    })

# Patient routes
@app.get("/patients", response_class=HTMLResponse)
async def patients_page(request: Request, search: Optional[str] = None, msg: Optional[str] = None, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    patients = crud.get_patients(db, search=search)
    return templates.TemplateResponse("patients.html", {
        "request": request,
        "user": user,
        "patients": patients,
        "search": search or "",
        "toast": msg,
    })

@app.post("/patients")
async def create_patient_endpoint(
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    phone: str = Form(...),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    patient_data = schemas.PatientCreate(name=name, age=age, gender=gender, phone=phone)
    crud.create_patient(db, patient_data)
    return RedirectResponse(url="/patients?msg=Patient+added+successfully", status_code=302)

@app.post("/patients/{patient_id}/edit")
async def update_patient_endpoint(
    patient_id: int,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    phone: str = Form(...),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    patient_data = schemas.PatientUpdate(name=name, age=age, gender=gender, phone=phone)
    crud.update_patient(db, patient_id, patient_data)
    return RedirectResponse(url="/patients?msg=Patient+updated+successfully", status_code=302)

@app.post("/patients/{patient_id}/delete")
async def delete_patient_endpoint(patient_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.delete_patient(db, patient_id)
    return RedirectResponse(url="/patients?msg=Patient+deleted", status_code=302)

@app.post("/api/patients")
async def create_patient_api(
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    phone: str = Form(...),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    patient_data = schemas.PatientCreate(name=name, age=age, gender=gender, phone=phone)
    patient = crud.create_patient(db, patient_data)
    return JSONResponse(content={
        "id": patient.id, "name": patient.name,
        "age": patient.age, "gender": patient.gender, "phone": patient.phone,
    })

# Test Catalog routes (Tests + Panels management)
@app.get("/tests", response_class=HTMLResponse)
async def tests_page(
    request: Request,
    msg: Optional[str] = None,
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    categories = crud.get_test_categories(db)
    panels = crud.get_panels(db)
    standalone_tests = crud.get_standalone_tests(db)
    return templates.TemplateResponse("tests.html", {
        "request": request,
        "user": user,
        "categories": categories,
        "panels": panels,
        "standalone_tests": standalone_tests,
        "toast": msg,
    })

@app.post("/test-categories")
async def create_category_endpoint(
    name: str = Form(...),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category_data = schemas.TestCategoryCreate(name=name)
    crud.create_test_category(db, category_data)
    return RedirectResponse(url="/tests?msg=Category+added", status_code=302)

@app.post("/tests")
async def create_test_endpoint(
    name: str = Form(...),
    price: float = Form(0.0),
    unit: Optional[str] = Form(None),
    reference_range: Optional[str] = Form(None),
    category_id: int = Form(...),
    panel_id: Optional[str] = Form(None),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    test_data = schemas.TestCreate(
        name=name,
        price=price,
        unit=unit or None,
        reference_range=reference_range or None,
        category_id=category_id,
        panel_id=int(panel_id) if panel_id else None,
    )
    crud.create_test(db, test_data)
    return RedirectResponse(url="/tests?msg=Test+added+successfully", status_code=302)

@app.post("/tests/{test_id}/edit")
async def update_test_endpoint(
    test_id: int,
    name: str = Form(...),
    price: float = Form(0.0),
    unit: Optional[str] = Form(None),
    reference_range: Optional[str] = Form(None),
    category_id: int = Form(...),
    panel_id: Optional[str] = Form(None),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    test_data = schemas.TestUpdate(
        name=name,
        price=price,
        unit=unit or None,
        reference_range=reference_range or None,
        category_id=category_id,
        panel_id=int(panel_id) if panel_id else None,
    )
    crud.update_test(db, test_id, test_data)
    return RedirectResponse(url="/tests?msg=Test+updated+successfully", status_code=302)

@app.post("/tests/{test_id}/delete")
async def delete_test_endpoint(test_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.delete_test(db, test_id)
    return RedirectResponse(url="/tests?msg=Test+deleted", status_code=302)

# Panel routes
@app.post("/panels")
async def create_panel_endpoint(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(0.0),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    panel_data = schemas.PanelCreate(name=name, description=description or None, price=price)
    crud.create_panel(db, panel_data)
    return RedirectResponse(url="/tests?msg=Test+group+added", status_code=302)

@app.post("/panels/{panel_id}/edit")
async def update_panel_endpoint(
    panel_id: int,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(0.0),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    panel_data = schemas.PanelUpdate(name=name, description=description or None, price=price)
    crud.update_panel(db, panel_id, panel_data)
    return RedirectResponse(url="/tests?msg=Test+group+updated", status_code=302)

@app.post("/panels/{panel_id}/delete")
async def delete_panel_endpoint(panel_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.delete_panel(db, panel_id)
    return RedirectResponse(url="/tests?msg=Test+group+deleted", status_code=302)

# Order routes
@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request, msg: Optional[str] = None, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = crud.get_orders(db)
    return templates.TemplateResponse("orders.html", {
        "request": request,
        "user": user,
        "view": "list",
        "orders": orders,
        "toast": msg,
    })

@app.get("/orders/new", response_class=HTMLResponse)
async def new_order_page(request: Request, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    patients = crud.get_patients(db)
    panels = crud.get_panels(db)
    standalone_tests = crud.get_standalone_tests(db)

    panels_data = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "category": p.category.name if p.category else "Other",
            "tests": [t.name for t in p.tests],
        }
        for p in panels
    ]
    tests_data = [
        {"id": t.id, "name": t.name, "price": t.price, "category": t.category.name}
        for t in standalone_tests
    ]

    return templates.TemplateResponse("orders.html", {
        "request": request,
        "user": user,
        "view": "new",
        "patients": patients,
        "panels_data": panels_data,
        "tests_data": tests_data,
    })

@app.post("/orders")
async def create_order_endpoint(
    request: Request,
    patient_id: int = Form(...),
    referred_by: Optional[str] = Form(None),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    form_data = await request.form()
    test_ids = [int(tid) for tid in form_data.getlist("test_ids")]
    panel_ids = [int(pid) for pid in form_data.getlist("panel_ids")]

    if not test_ids and not panel_ids:
        return RedirectResponse(url="/orders/new", status_code=302)

    order_data = schemas.TestOrderCreate(
        patient_id=patient_id, test_ids=test_ids, panel_ids=panel_ids, referred_by=referred_by
    )
    order = crud.create_order(db, order_data)
    return RedirectResponse(url=f"/orders/{order.id}", status_code=302)

@app.get("/orders/{order_id}", response_class=HTMLResponse)
async def order_detail_page(request: Request, order_id: int, msg: Optional[str] = None, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return templates.TemplateResponse("orders.html", {
        "request": request,
        "user": user,
        "view": "detail",
        "order": order,
        "toast": msg,
    })

@app.post("/orders/{order_id}/complete")
async def complete_order_endpoint(order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.update_order_status(db, order_id, "completed")
    return RedirectResponse(url=f"/reports/{order_id}?msg=Order+completed", status_code=302)

@app.post("/orders/{order_id}/save-results")
async def save_results_draft_endpoint(
    request: Request, order_id: int,
    user: str = Depends(get_current_user), db: Session = Depends(get_db)
):
    form_data = await request.form()
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for item in order.items:
        result_value = form_data.get(f"result_value_{item.id}")
        result_notes = form_data.get(f"result_notes_{item.id}")
        if result_value is not None:
            item_data = schemas.TestOrderItemUpdate(
                result_value=result_value if result_value.strip() else None,
                result_notes=result_notes if result_notes and result_notes.strip() else None,
            )
            crud.update_order_item_result(db, item.id, item_data)
    return RedirectResponse(url=f"/orders/{order_id}?msg=Results+saved", status_code=302)

@app.post("/orders/{order_id}/complete-with-results")
async def complete_with_results_endpoint(
    request: Request, order_id: int,
    user: str = Depends(get_current_user), db: Session = Depends(get_db)
):
    form_data = await request.form()
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for item in order.items:
        result_value = form_data.get(f"result_value_{item.id}")
        result_notes = form_data.get(f"result_notes_{item.id}")
        if result_value is not None:
            item_data = schemas.TestOrderItemUpdate(
                result_value=result_value if result_value.strip() else None,
                result_notes=result_notes if result_notes and result_notes.strip() else None,
            )
            crud.update_order_item_result(db, item.id, item_data)
    crud.update_order_status(db, order_id, "completed")
    return RedirectResponse(url=f"/reports/{order_id}?msg=Report+generated+successfully", status_code=302)

@app.post("/orders/{order_id}/delete")
async def delete_order_endpoint(order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Can only delete pending orders")
    
    crud.delete_order(db, order_id)
    return RedirectResponse(url="/orders?msg=Order+deleted", status_code=302)

# Reports routes
@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    completed_orders = crud.get_orders(db, status="completed")
    return templates.TemplateResponse("reports.html", {
        "request": request,
        "user": user,
        "orders": completed_orders
    })

@app.get("/reports/{order_id}", response_class=HTMLResponse)
async def report_detail_page(request: Request, order_id: int, msg: Optional[str] = None, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order or order.status != "completed":
        raise HTTPException(status_code=404, detail="Completed order not found")
    
    return templates.TemplateResponse("report_detail.html", {
        "request": request,
        "user": user,
        "order": order,
        "toast": msg,
    })

@app.get("/reports/{order_id}/edit", response_class=HTMLResponse)
async def edit_report_page(request: Request, order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return templates.TemplateResponse("edit_report.html", {
        "request": request,
        "user": user,
        "order": order
    })

@app.post("/reports/{order_id}/update-all")
async def update_all_report_items_endpoint(
    request: Request,
    order_id: int,
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    form_data = await request.form()
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update each item
    for item in order.items:
        result_value = form_data.get(f"result_value_{item.id}")
        result_notes = form_data.get(f"result_notes_{item.id}")
        
        if result_value is not None:
            item_data = schemas.TestOrderItemUpdate(
                result_value=result_value if result_value.strip() else None,
                result_notes=result_notes if result_notes and result_notes.strip() else None
            )
            crud.update_order_item_result(db, item.id, item_data)
    
    return RedirectResponse(url=f"/reports/{order_id}?msg=Results+saved+successfully", status_code=302)

@app.post("/reports/items/{item_id}/update")
async def update_report_item_endpoint(
    item_id: int,
    result_value: str = Form(...),
    result_notes: Optional[str] = Form(None),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item_data = schemas.TestOrderItemUpdate(
        result_value=result_value,
        result_notes=result_notes or None
    )
    item = crud.update_order_item_result(db, item_id, item_data)
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    
    return RedirectResponse(url=f"/reports/{item.order_id}/edit", status_code=302)


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    uvicorn.run(app, host=host, port=port)
