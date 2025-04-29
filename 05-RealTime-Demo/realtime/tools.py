import yfinance as yf
import chainlit as cl
import plotly
import httpx
from datetime import datetime
from typing import Optional, List


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

# BASE_URL = "http://localhost:8020"
BASE_URL = "http://localhost:8020"


# HERRAMIENTAS IBERO
ibero_calendar_def = {
    "name": "display_ibero_calendar",
    "description": "Displays the Ibero academic calendar for the 2025 cycle.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to display alongside the calendar PDF."
            }
        },
        "required": ["message"]
    }
}

async def display_ibero_calendar(message: str):
    """
    Displays the Ibero academic calendar PDF.
    """
    elements = [
        cl.Pdf(
            name="ibero_calendar",
            display="inline",
            path="/Users/emiliosandoval/Documents/ibero2025/casos-ia-ibero-diplomado/05-RealTime-Demo/sources/calendario2025.pdf"
        )
    ]
    await cl.Message(content=message, elements=elements).send()

ibero_calendar_tool = (ibero_calendar_def, display_ibero_calendar)

parking_map_def = {
    "name": "display_parking_map",
    "description": "Displays the Ibero parking map image showing the different parking areas on campus.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to display alongside the parking map."
            }
        },
        "required": ["message"]
    }
}

async def display_parking_map(message: str):
    """
    Displays the Ibero parking map image.
    """
    image = cl.Image(
        path="/Users/emiliosandoval/Documents/ibero2025/casos-ia-ibero-diplomado/05-RealTime-Demo/sources/mapa-estacionamiento.png",
        name="parking_map",
        display="inline"
    )
    await cl.Message(
        content=message,
        elements=[image],
    ).send()

parking_map_tool = (parking_map_def, display_parking_map)

registration_form_def = {
    "name": "display_registration_form",
    "description": "Displays the Ibero registration form PDF document.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to display alongside the registration form PDF."
            }
        },
        "required": ["message"]
    }
}

async def display_registration_form(message: str):
    """
    Displays the Ibero registration form PDF.
    """
    elements = [
        cl.Pdf(
            name="registration_form",
            display="inline",
            path="/Users/emiliosandoval/Documents/ibero2025/casos-ia-ibero-diplomado/05-RealTime-Demo/sources/SOLICITUD DE REGISTRO.pdf"
        )
    ]
    await cl.Message(content=message, elements=elements).send()

registration_form_tool = (registration_form_def, display_registration_form)

registration_video_def = {
    "name": "display_registration_video",
    "description": "Displays a tutorial video about first-round registration at Ibero.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to display alongside the registration tutorial video."
            }
        },
        "required": ["message"]
    }
}

async def display_registration_video(message: str):
    """
    Displays the Ibero registration tutorial video.
    """
    video = cl.Video(
        path="/Users/emiliosandoval/Documents/ibero2025/casos-ia-ibero-diplomado/05-RealTime-Demo/sources/Te ayudamos en tu reinscripción de primera vuelta.mp4",
        name="registration_video",
        display="inline"
    )
    await cl.Message(content=message, elements=[video]).send()

registration_video_tool = (registration_video_def, display_registration_video)

# HERRAMIENTAS DE TEXTO PARA INFORMACIÓN DE CONTACTO

escolares_email_def = {
    "name": "display_escolares_email",
    "description": "Displays the email contact for Servicios Escolares at Ibero.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to display alongside the email contact."
            }
        },
        "required": ["message"]
    }
}

async def display_escolares_email(message: str):
    """
    Displays the email for Servicios Escolares.
    """
    text = cl.Text(
        name="escolares_email",
        content="servicios.escolares@ibero.mx",
        display="inline",
        language="markdown"
    )
    await cl.Message(content=message, elements=[text]).send()

escolares_email_tool = (escolares_email_def, display_escolares_email)

escolares_phone_def = {
    "name": "display_escolares_phone",
    "description": "Displays the phone number for Servicios Escolares at Ibero.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to display alongside the phone number."
            }
        },
        "required": ["message"]
    }
}

async def display_escolares_phone(message: str):
    """
    Displays the phone number for Servicios Escolares.
    """
    text = cl.Text(
        name="escolares_phone",
        content="5559504093",
        display="inline",
        language="markdown"
    )
    await cl.Message(content=message, elements=[text]).send()

escolares_phone_tool = (escolares_phone_def, display_escolares_phone)

deportes_email_def = {
    "name": "display_deportes_email",
    "description": "Displays the email contact for Hugo Martínez, who handles sports related inquiries at Ibero.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to display alongside the email contact."
            }
        },
        "required": ["message"]
    }
}

async def display_deportes_email(message: str):
    """
    Displays the email for Hugo Martínez (sports contact).
    """
    text = cl.Text(
        name="deportes_email",
        content="hugo.martinez@ibero.mx",
        display="inline",
        language="markdown"
    )
    await cl.Message(content=message, elements=[text]).send()

deportes_email_tool = (deportes_email_def, display_deportes_email)

deportes_phone_def = {
    "name": "display_deportes_phone",
    "description": "Displays the phone number for Hugo Martínez, who handles sports related inquiries at Ibero.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to display alongside the phone number."
            }
        },
        "required": ["message"]
    }
}

async def display_deportes_phone(message: str):
    """
    Displays the phone number for Hugo Martínez (sports contact).
    """
    text = cl.Text(
        name="deportes_phone",
        content="55 4514 9423",
        display="inline",
        language="markdown"
    )
    await cl.Message(content=message, elements=[text]).send()

deportes_phone_tool = (deportes_phone_def, display_deportes_phone)

campus_location_def = {
    "name": "display_campus_location",
    "description": "Displays the address and location information for the Ibero campus.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to display alongside the campus location."
            }
        },
        "required": ["message"]
    }
}

async def display_campus_location(message: str):
    """
    Displays the Ibero campus location information.
    """
    text = cl.Text(
        name="campus_location",
        content="Prolongación Paseo de la Reforma 880, Lomas de Santa Fe, Ciudad de México, C.P. 01219",
        display="inline",
        language="markdown"
    )
    await cl.Message(content=message, elements=[text]).send()

campus_location_tool = (campus_location_def, display_campus_location)

ibero_website_def = {
    "name": "display_ibero_website",
    "description": "Displays the official website URL for Universidad Iberoamericana.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to display alongside the website URL."
            }
        },
        "required": ["message"]
    }
}

async def display_ibero_website(message: str):
    """
    Displays the official Ibero website URL.
    """
    text = cl.Text(
        name="ibero_website",
        content="https://ibero.mx/",
        display="inline",
        language="markdown"
    )
    await cl.Message(content=message, elements=[text]).send()

ibero_website_tool = (ibero_website_def, display_ibero_website)

# Lista de herramientas disponibles
tools = [
    draw_plotly_chart,
    ibero_calendar_tool,
    parking_map_tool,
    registration_form_tool,
    registration_video_tool,
    escolares_email_tool,
    escolares_phone_tool,
    deportes_email_tool,
    deportes_phone_tool,
    campus_location_tool,
    ibero_website_tool
]

