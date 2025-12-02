import os
from datetime import timedelta
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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
            "error": "Invalid username or password"
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
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": user,
        "stats": stats
    })

# Patient routes
@app.get("/patients", response_class=HTMLResponse)
async def patients_page(request: Request, search: Optional[str] = None, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    patients = crud.get_patients(db, search=search)
    return templates.TemplateResponse("patients.html", {
        "request": request,
        "user": user,
        "patients": patients,
        "search": search or ""
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
    return RedirectResponse(url="/patients", status_code=302)

@app.get("/patients/{patient_id}/edit", response_class=HTMLResponse)
async def edit_patient_page(request: Request, patient_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return templates.TemplateResponse("edit_patient.html", {
        "request": request,
        "user": user,
        "patient": patient
    })

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
    return RedirectResponse(url="/patients", status_code=302)

@app.post("/patients/{patient_id}/delete")
async def delete_patient_endpoint(patient_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.delete_patient(db, patient_id)
    return RedirectResponse(url="/patients", status_code=302)

# Test routes
@app.get("/tests", response_class=HTMLResponse)
async def tests_page(
    request: Request, 
    category_id: Optional[int] = None,
    user: str = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    categories = crud.get_test_categories(db)
    tests = crud.get_tests(db, category_id)
    return templates.TemplateResponse("tests.html", {
        "request": request,
        "user": user,
        "categories": categories,
        "tests": tests,
        "selected_category": category_id
    })

@app.post("/test-categories")
async def create_category_endpoint(
    name: str = Form(...),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category_data = schemas.TestCategoryCreate(name=name)
    crud.create_test_category(db, category_data)
    return RedirectResponse(url="/tests", status_code=302)

@app.post("/tests")
async def create_test_endpoint(
    name: str = Form(...),
    price: float = Form(...),
    unit: Optional[str] = Form(None),
    reference_range: Optional[str] = Form(None),
    category_id: int = Form(...),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    test_data = schemas.TestCreate(
        name=name,
        price=price,
        unit=unit or None,
        reference_range=reference_range or None,
        category_id=category_id
    )
    crud.create_test(db, test_data)
    return RedirectResponse(url="/tests", status_code=302)

@app.get("/tests/{test_id}/edit", response_class=HTMLResponse)
async def edit_test_page(request: Request, test_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    test = crud.get_test(db, test_id)
    categories = crud.get_test_categories(db)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return templates.TemplateResponse("edit_test.html", {
        "request": request,
        "user": user,
        "test": test,
        "categories": categories
    })

@app.post("/tests/{test_id}/edit")
async def update_test_endpoint(
    test_id: int,
    name: str = Form(...),
    price: float = Form(...),
    unit: Optional[str] = Form(None),
    reference_range: Optional[str] = Form(None),
    category_id: int = Form(...),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    test_data = schemas.TestUpdate(
        name=name,
        price=price,
        unit=unit or None,
        reference_range=reference_range or None,
        category_id=category_id
    )
    crud.update_test(db, test_id, test_data)
    return RedirectResponse(url="/tests", status_code=302)

@app.post("/tests/{test_id}/delete")
async def delete_test_endpoint(test_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.delete_test(db, test_id)
    return RedirectResponse(url="/tests", status_code=302)

# Order routes
@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = crud.get_orders(db)
    return templates.TemplateResponse("orders.html", {
        "request": request,
        "user": user,
        "orders": orders
    })

@app.get("/orders/new", response_class=HTMLResponse)
async def new_order_page(request: Request, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    patients = crud.get_patients(db)
    tests = crud.get_tests(db)
    return templates.TemplateResponse("new_order.html", {
        "request": request,
        "user": user,
        "patients": patients,
        "tests": tests
    })

@app.post("/orders")
async def create_order_endpoint(
    request: Request,
    patient_id: int = Form(...),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    form_data = await request.form()
    test_ids = [int(tid) for tid in form_data.getlist("test_ids")]
    
    if not test_ids:
        return RedirectResponse(url="/orders/new", status_code=302)
    
    order_data = schemas.TestOrderCreate(patient_id=patient_id, test_ids=test_ids)
    crud.create_order(db, order_data)
    return RedirectResponse(url="/orders", status_code=302)

@app.get("/orders/{order_id}", response_class=HTMLResponse)
async def order_detail_page(request: Request, order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return templates.TemplateResponse("order_detail.html", {
        "request": request,
        "user": user,
        "order": order
    })

@app.post("/orders/{order_id}/complete")
async def complete_order_endpoint(order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.update_order_status(db, order_id, "completed")
    return RedirectResponse(url=f"/orders/{order_id}", status_code=302)

@app.post("/orders/{order_id}/delete")
async def delete_order_endpoint(order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Can only delete pending orders")
    
    crud.delete_order(db, order_id)
    return RedirectResponse(url="/orders", status_code=302)

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
async def report_detail_page(request: Request, order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order or order.status != "completed":
        raise HTTPException(status_code=404, detail="Completed order not found")
    
    return templates.TemplateResponse("report_detail.html", {
        "request": request,
        "user": user,
        "order": order
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
    
    return RedirectResponse(url=f"/reports/{order_id}", status_code=302)

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

@app.get("/reports/{order_id}/pdf")
async def download_report_pdf(order_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order or order.status != "completed":
        raise HTTPException(status_code=404, detail="Completed order not found")
    
    try:
        from utils import WEASYPRINT_AVAILABLE, generate_report_pdf, generate_report_html
        
        if WEASYPRINT_AVAILABLE:
            pdf_bytes = generate_report_pdf(order)
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename=report_{order_id}.pdf"}
            )
        
        html_content = generate_report_html(order)
        return Response(
            content=html_content.encode('utf-8'),
            media_type="text/html",
            headers={"Content-Disposition": f"inline; filename=report_{order_id}.html"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    uvicorn.run(app, host=host, port=port)