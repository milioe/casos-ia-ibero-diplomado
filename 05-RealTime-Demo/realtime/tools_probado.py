import yfinance as yf
import chainlit as cl
import plotly
import httpx  # Agregar httpx para manejar las solicitudes HTTP
from datetime import datetime
from typing import Optional, List

# Definición de la herramienta para programar citas con los doctores
schedule_appointment_def = {
    "name": "schedule_appointment",
    "description": "Schedules an appointment with a doctor by sending a request to their appointment URL. Appointments can be scheduled between 8:00 AM and 5:30 PM.",
    "parameters": {
        "type": "object",
        "properties": {
            "doctor_id": {
                "type": "integer",
                "description": "The doctor's ID (1 for 'Dr. Emilio Sandoval' or 2 for 'Dra. Vanessa López')"
            },
            "patient_name": {
                "type": "string",
                "description": "The name of the patient scheduling the appointment"
            },
            "date": {
                "type": "string",
                "description": "The date of the appointment in YYYY-MM-DD format"
            },
            "time": {
                "type": "string",
                "description": "The time of the appointment in HH:MM format (24-hour, between 08:00 and 17:30)"
            }
        },
        "required": ["doctor_id", "patient_name", "date", "time"]
    }
}

async def schedule_appointment_handler(doctor_id, patient_name, date, time):
    """
    Schedules an appointment with the specified doctor, enforcing the time restrictions (8:00 AM to 5:30 PM).
    """
    print(doctor_id)
    print(patient_name)
    print(date)
    print(time)
    try:
        base_url = "https://a33b5c7c-9125-4c7f-9a75-21587a9ed262-00-3j2a7cqi872mr.picard.replit.dev/doctors/"
        if doctor_id not in [1, 2]:
            return {"error": "Doctor not found. Available doctor IDs are 1 (Dr. Emilio Sandoval) and 2 (Dra. Vanessa López)."}

        # Validar formato de fecha y hora
        appointment_time = datetime.strptime(time, "%H:%M").time()
        earliest_time = datetime.strptime("08:00", "%H:%M").time()
        latest_time = datetime.strptime("17:30", "%H:%M").time()
        if not (earliest_time <= appointment_time <= latest_time):
            return {"error": "Appointments can only be scheduled between 8:00 AM and 5:30 PM."}

        # Construir la URL de la solicitud
        url = f"{base_url}{doctor_id}/appointments"
        
        # Realizar la solicitud POST usando httpx
        payload = {
            "patient_name": patient_name,
            "date": date,
            "time": time
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)

        if response.status_code == 200:
            return "Appointment scheduled successfully."
        else:
            print("falló")
            print(response)
            return {"error": f"Failed to schedule appointment. Status code: {response.status_code}"}

    except Exception as e:
        print("error", e)
        return {"error": str(e)}

schedule_appointment = (schedule_appointment_def, schedule_appointment_handler)

# Herramientas existentes
query_stock_price_def = {
    "name": "query_stock_price",
    "description": "Queries the latest stock price information for a given stock symbol.",
    "parameters": {
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "The stock symbol to query (e.g., 'AAPL' for Apple Inc.)"
            },
            "period": {
                "type": "string",
                "description": "The time period for which to retrieve stock data (e.g., '1d' for one day, '1mo' for one month)"
            }
        },
        "required": ["symbol", "period"]
    }
}

async def query_stock_price_handler(symbol, period):
    """
    Queries the latest stock price information for a given stock symbol.
    """
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        if hist.empty:
            return {"error": "No data found for the given symbol."}
        return hist.to_json()
 
    except Exception as e:
        return {"error": str(e)}

query_stock_price = (query_stock_price_def, query_stock_price_handler)

draw_plotly_chart_def = {
    "name": "draw_plotly_chart",
    "description": "Draws a Plotly chart based on the provided JSON figure and displays it with an accompanying message.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to display alongside the chart"
            },
            "plotly_json_fig": {
                "type": "string",
                "description": "A JSON string representing the Plotly figure to be drawn"
            }
        },
        "required": ["message", "plotly_json_fig"]
    }
}

async def draw_plotly_chart_handler(message: str, plotly_json_fig):
    fig = plotly.io.from_json(plotly_json_fig)
    elements = [cl.Plotly(name="chart", figure=fig, display="inline")]

    await cl.Message(content=message, elements=elements).send()
    
draw_plotly_chart = (draw_plotly_chart_def, draw_plotly_chart_handler)

# Nuevas herramientas que realizan solicitudes a los endpoints
# Definir la base URL para los endpoints
BASE_URL = "http://localhost:8000"

# Herramienta para obtener información de un material específico
get_material_info_def = {
    "name": "get_material_info",
    "description": "Retrieves information for a specific material by its ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "material_id": {
                "type": "string",
                "description": "The ID of the material to retrieve information for."
            }
        },
        "required": ["material_id"]
    }
}

async def get_material_info_handler(material_id: str):
    """
    Retrieves information for a specific material by making a GET request to the /materials/{material_id} endpoint.
    """
    try:
        url = f"{BASE_URL}/materials/{material_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "Material not found."}
        else:
            return {"error": f"Failed to retrieve material info. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

get_material_info = (get_material_info_def, get_material_info_handler)

# Herramienta para obtener el stock total por almacén
get_stock_total_by_warehouse_def = {
    "name": "get_stock_total_by_warehouse",
    "description": "Retrieves the total stock grouped by warehouse.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

async def get_stock_total_by_warehouse_handler():
    """
    Retrieves the total stock by warehouse by making a GET request to the /materials/stock-by-warehouse/ endpoint.
    """
    try:
        url = f"{BASE_URL}/materials/stock-by-warehouse/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to retrieve stock by warehouse. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

get_stock_total_by_warehouse = (get_stock_total_by_warehouse_def, get_stock_total_by_warehouse_handler)

# Herramienta para obtener el stock total por sucursal
get_stock_total_by_branch_def = {
    "name": "get_stock_total_by_branch",
    "description": "Retrieves the total stock grouped by branch.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

async def get_stock_total_by_branch_handler():
    """
    Retrieves the total stock by branch by making a GET request to the /materials/stock-by-branch/ endpoint.
    """
    try:
        url = f"{BASE_URL}/materials/stock-by-branch/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to retrieve stock by branch. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

get_stock_total_by_branch = (get_stock_total_by_branch_def, get_stock_total_by_branch_handler)

# Herramienta para obtener las ventas totales por categoría
get_total_sales_by_category_def = {
    "name": "get_total_sales_by_category",
    "description": "Retrieves total sales grouped by product category.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

async def get_total_sales_by_category_handler():
    """
    Retrieves total sales grouped by product category by making a GET request to the /sales/total-by-category/ endpoint.
    """
    try:
        url = f"{BASE_URL}/sales/total-by-category/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to retrieve total sales by category. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

get_total_sales_by_category = (get_total_sales_by_category_def, get_total_sales_by_category_handler)

# Herramienta para obtener productos a reordenar
get_products_to_reorder_def = {
    "name": "get_products_to_reorder",
    "description": "Retrieves a list of products that need to be reordered based on inventory levels.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

async def get_products_to_reorder_handler():
    """
    Retrieves products that need to be reordered by making a GET request to the /products/reorder/ endpoint.
    """
    try:
        url = f"{BASE_URL}/products/reorder/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to retrieve products to reorder. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

get_products_to_reorder = (get_products_to_reorder_def, get_products_to_reorder_handler)

# Herramienta para obtener ventas mensuales por empleado
get_monthly_sales_by_employee_def = {
    "name": "get_monthly_sales_by_employee",
    "description": "Retrieves monthly sales data for employees, optionally filtering by employee ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "employee_id": {
                "type": "integer",
                "description": "Optional ID of the employee to filter sales data"
            }
        },
        "required": []
    }
}

async def get_monthly_sales_by_employee_handler(employee_id: Optional[int] = None):
    """
    Retrieves monthly sales data for employees by making a GET request to the /sales/monthly-by-employee/ endpoint.
    """
    try:
        url = f"{BASE_URL}/sales/monthly-by-employee/"
        params = {}
        if employee_id is not None:
            params["employee_id"] = employee_id
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to retrieve monthly sales by employee. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

get_monthly_sales_by_employee = (get_monthly_sales_by_employee_def, get_monthly_sales_by_employee_handler)

# Herramienta para obtener los productos más vendidos
get_top_selling_products_def = {
    "name": "get_top_selling_products",
    "description": "Retrieves the top-selling products, allowing the specification of the number of products to return.",
    "parameters": {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "The number of top-selling products to retrieve (1-100)",
                "default": 10
            }
        },
        "required": []
    }
}

async def get_top_selling_products_handler(limit: int = 10):
    """
    Retrieves the top-selling products by making a GET request to the /products/top-selling/ endpoint.
    """
    try:
        url = f"{BASE_URL}/products/top-selling/"
        params = {"limit": limit}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to retrieve top-selling products. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

get_top_selling_products = (get_top_selling_products_def, get_top_selling_products_handler)

# Lista de herramientas disponibles
tools = [
    query_stock_price,
    draw_plotly_chart,
    # schedule_appointment,
    # get_material_info,               # Nueva herramienta
    # get_stock_total_by_warehouse,    # Nueva herramienta
    # get_stock_total_by_branch,       # Nueva herramienta
    get_total_sales_by_category,
    get_products_to_reorder,
    get_monthly_sales_by_employee,
    get_top_selling_products
]
