CONFIRMACION_CITA_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirmación de Cita - Telefonía PTA</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Arial', sans-serif; background-color: #f4f4f4;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: bold;">Telefonía PTA</h1>
                            <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Confirmación de Cita</p>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h2 style="color: #333333; margin: 0 0 20px 0; font-size: 24px;">¡Hola {{ nombre }}!</h2>
                            <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                                Tu cita ha sido <strong style="color: #667eea;">agendada exitosamente</strong>. Aquí están los detalles:
                            </p>
                            
                            <!-- Detalles de la cita -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8f9fa; border-radius: 6px; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <table width="100%" cellpadding="8" cellspacing="0">
                                            <tr>
                                                <td style="color: #666666; font-size: 14px; padding: 8px 0;">
                                                    <strong style="color: #333333;">ID de Cita:</strong>
                                                </td>
                                                <td style="color: #667eea; font-size: 16px; font-weight: bold; text-align: right; padding: 8px 0;">
                                                    #{{ id_cita }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="color: #666666; font-size: 14px; padding: 8px 0; border-top: 1px solid #e0e0e0;">
                                                    <strong style="color: #333333;">Fecha y Hora:</strong>
                                                </td>
                                                <td style="color: #333333; font-size: 14px; text-align: right; padding: 8px 0; border-top: 1px solid #e0e0e0;">
                                                    {{ fecha_hora }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td colspan="2" style="color: #666666; font-size: 14px; padding: 15px 0 0 0; border-top: 1px solid #e0e0e0;">
                                                    <strong style="color: #333333;">Sucursal:</strong><br>
                                                    <span style="color: #333333; font-size: 15px; font-weight: bold;">{{ sucursal }}</span><br>
                                                    <span style="color: #666666; font-size: 13px; line-height: 1.5;">{{ direccion_sucursal }}</span>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td colspan="2" style="color: #666666; font-size: 14px; padding: 15px 0 0 0; border-top: 1px solid #e0e0e0;">
                                                    <strong style="color: #333333;">Motivo:</strong><br>
                                                    <span style="color: #666666; font-size: 13px; line-height: 1.5;">{{ descripcion }}</span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="color: #666666; font-size: 14px; line-height: 1.6; margin: 20px 0 0 0;">
                                Por favor, llega <strong>10 minutos antes</strong> de tu cita. Si necesitas reagendar o cancelar, comunícate al <strong style="color: #667eea;">1-800-PTA-AYUDA</strong>.
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                            <p style="color: #999999; font-size: 12px; margin: 0 0 10px 0;">
                                Gracias por elegir Telefonía PTA
                            </p>
                            <p style="color: #999999; font-size: 12px; margin: 0;">
                                © 2025 Telefonía PTA. Todos los derechos reservados.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

FACTURA_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Detalle de Facturación - Telefonía PTA</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Arial', sans-serif; background-color: #f4f4f4;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
        <tr>
            <td align="center">
                <table width="650" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #2d6a4f 0%, #40916c 50%, #52b788 100%); padding: 50px 30px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: bold; letter-spacing: 2px;">Telefonía PTA</h1>
                            <p style="color: #ffffff; margin: 15px 0 0 0; font-size: 18px; opacity: 0.95;">Detalle de Facturación</p>
                            <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 13px; opacity: 0.8;">Período de Facturación: {{ fecha_actual }}</p>
                        </td>
                    </tr>
                    
                    <!-- Info Cliente -->
                    <tr>
                        <td style="padding: 30px; background-color: #f8f9fa;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td width="50%" style="vertical-align: top;">
                                        <p style="margin: 0 0 5px 0; color: #666; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Facturado a:</p>
                                        <h2 style="color: #333333; margin: 0 0 5px 0; font-size: 20px;">{{ nombre }}</h2>
                                        <p style="color: #666666; font-size: 14px; margin: 0; line-height: 1.5;">
                                            ID Cliente: <strong style="color: #2d6a4f;">{{ id_cliente }}</strong><br>
                                            Fecha: <strong>{{ fecha_actual }}</strong>
                                        </p>
                                    </td>
                                    <td width="50%" style="text-align: right; vertical-align: top;">
                                        <p style="margin: 0 0 5px 0; color: #666; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Soporte 24/7</p>
                                        <p style="color: #2d6a4f; font-size: 18px; font-weight: bold; margin: 0 0 5px 0;">1-800-PTA-AYUDA</p>
                                        <p style="color: #666666; font-size: 13px; margin: 0;">soporte@telefoniaPTA.com.mx</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 20px 30px 30px 30px;">
                            <h3 style="color: #333333; margin: 0 0 20px 0; font-size: 22px; border-bottom: 2px solid #52b788; padding-bottom: 10px;">
                                Planes Contratados ({{ len_contratos }})
                            </h3>
                            
                            <!-- Contratos -->
                            {% for contrato in contratos %}
                            <table width="100%" cellpadding="0" cellspacing="0" style="background: linear-gradient(to right, #f8f9fa 0%, #ffffff 100%); border: 2px solid #52b788; border-radius: 8px; margin: 0 0 20px 0; overflow: hidden;">
                                <tr>
                                    <td style="background: linear-gradient(135deg, #2d6a4f 0%, #40916c 100%); padding: 18px 25px;">
                                        <table width="100%" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td>
                                                    <h3 style="color: #ffffff; margin: 0; font-size: 19px; font-weight: bold;">{{ contrato.nombre }}</h3>
                                                </td>
                                                <td style="text-align: right;">
                                                    <span style="background-color: rgba(255,255,255,0.2); color: #ffffff; padding: 5px 15px; border-radius: 15px; font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">
                                                        {{ contrato.status }}
                                                    </span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 25px;">
                                        {% if contrato.descripcion %}
                                        <p style="color: #666666; font-size: 14px; line-height: 1.6; margin: 0 0 20px 0; padding: 15px; background-color: #f1faee; border-left: 4px solid #52b788; border-radius: 4px;">
                                            <strong style="color: #2d6a4f;">Incluye:</strong> {{ contrato.descripcion }}
                                        </p>
                                        {% endif %}
                                        
                                        <table width="100%" cellpadding="10" cellspacing="0">
                                            <tr>
                                                <td style="color: #666666; font-size: 14px; padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                                                    <strong style="color: #333333;">💰 Pago Mensual:</strong>
                                                </td>
                                                <td style="color: #2d6a4f; font-size: 24px; font-weight: bold; text-align: right; padding: 12px 0; border-bottom: 1px solid #e0e0e0;">
                                                    ${{ contrato.pago_mensual }}.00 <span style="font-size: 14px; color: #666;">MXN</span>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="color: #666666; font-size: 14px; padding: 12px 0;">
                                                    <strong style="color: #333333;">📅 Próxima Fecha de Pago:</strong>
                                                </td>
                                                <td style="color: #333333; font-size: 15px; font-weight: 600; text-align: right; padding: 12px 0;">
                                                    {{ contrato.fecha_pago }}
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            {% endfor %}
                            
                            <!-- Subtotal & IVA -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0 20px 0;">
                                <tr>
                                    <td style="padding: 12px 20px; text-align: right;">
                                        <span style="color: #666666; font-size: 15px;">Subtotal:</span>
                                        <span style="color: #333333; font-size: 18px; font-weight: 600; margin-left: 20px;">${{ subtotal }}.00</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 20px; text-align: right; border-bottom: 2px dashed #e0e0e0;">
                                        <span style="color: #666666; font-size: 15px;">IVA (16%):</span>
                                        <span style="color: #333333; font-size: 18px; font-weight: 600; margin-left: 20px;">${{ iva }}.00</span>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Total -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="background: linear-gradient(135deg, #2d6a4f 0%, #40916c 100%); border-radius: 8px; margin: 20px 0 30px 0; box-shadow: 0 4px 8px rgba(45,106,79,0.3);">
                                <tr>
                                    <td style="padding: 25px 30px;">
                                        <table width="100%" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td style="color: #ffffff; font-size: 20px; font-weight: bold;">
                                                    💳 TOTAL A PAGAR
                                                </td>
                                                <td style="color: #ffffff; font-size: 32px; font-weight: bold; text-align: right;">
                                                    ${{ total }}.00 <span style="font-size: 16px; opacity: 0.9;">MXN</span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Métodos de Pago -->
                            <div style="background-color: #e7f5ec; border-radius: 8px; padding: 25px; margin: 30px 0;">
                                <h4 style="color: #2d6a4f; margin: 0 0 15px 0; font-size: 16px;">💳 Métodos de Pago Aceptados</h4>
                                <p style="color: #666666; font-size: 14px; line-height: 1.6; margin: 0;">
                                    ✓ Transferencia Bancaria (BBVA, Santander, Citibanamex, AFIRME)<br>
                                    ✓ Pago en Línea: <strong style="color: #2d6a4f;">www.ptatelefonia.com.mx</strong><br>
                                    ✓ Línea PTA: <strong style="color: #2d6a4f;">800 550 0510</strong> | WhatsApp: <strong style="color: #2d6a4f;">55 6610</strong><br>
                                    ✓ Sucursales físicas (horario 9:00 AM - 7:00 PM)
                                </p>
                            </div>
                            
                            <!-- Info Adicional -->
                            <div style="background-color: #fff8e1; border-left: 4px solid #ffc107; padding: 20px; margin: 20px 0; border-radius: 4px;">
                                <p style="color: #666666; font-size: 13px; line-height: 1.6; margin: 0;">
                                    <strong style="color: #f57c00;">⚠️ Importante:</strong> El pago debe realizarse antes de la fecha indicada para evitar cargos por mora. 
                                    En caso de presentar saldo vencido, se aplicará un recargo del 3% mensual y se podrá suspender temporalmente el servicio.
                                </p>
                            </div>
                        </td>
                    </tr>
                    
                    <!-- Footer Legal -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 30px; border-top: 2px solid #52b788;">
                            <h4 style="color: #2d6a4f; margin: 0 0 15px 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">📋 Información Legal</h4>
                            <p style="color: #666666; font-size: 12px; line-height: 1.7; margin: 0 0 15px 0; text-align: justify;">
                                <strong>Telefonía PTA S.A. de C.V.</strong> | RFC: TPA-850923-HG4 | Av. Reforma 180, Col. Juárez, CDMX 06600<br>
                                Este documento constituye una factura válida para efectos fiscales. Los servicios están sujetos a los términos y condiciones 
                                establecidos en el contrato de prestación de servicios. Conserve este documento para cualquier aclaración.
                            </p>
                            
                            <p style="color: #999999; font-size: 11px; line-height: 1.6; margin: 0; text-align: justify;">
                                <strong>Aviso de Privacidad:</strong> Sus datos personales son tratados conforme a la Ley Federal de Protección de Datos Personales. 
                                Para más información visite: www.ptatelefonia.com.mx/privacidad. Si desea dejar de recibir estos correos, responda con la palabra 
                                "BAJA" o comuníquese al 1-800-PTA-AYUDA.
                            </p>
                            
                            <div style="text-align: center; margin-top: 25px; padding-top: 20px; border-top: 1px solid #e0e0e0;">
                                <p style="color: #999999; font-size: 12px; margin: 0 0 8px 0;">
                                    <strong style="color: #2d6a4f;">Gracias por confiar en Telefonía PTA</strong>
                                </p>
                                <p style="color: #999999; font-size: 11px; margin: 0;">
                                    © 2025 Telefonía PTA S.A. de C.V. | Todos los derechos reservados.
                                </p>
                            </div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
