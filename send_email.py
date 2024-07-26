import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from dotenv import load_dotenv
import os


def send(email, nombre, fecha, hora, peluquero, pago, recorte, corte):
    
    user = st.secrets["emails"]["smtp_user"]
    password = st.secrets["emails"]["smtp_password"]
    sender_email = "Peluqueria Cesar"
    
    msg = MIMEMultipart()
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587    
    
    
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Reserva de pista"    
    
    message = f"""
    Hola {nombre},
    
    Su reserva ha sido realizada con exito...
    
    Fecha: {fecha}
    Hora: {hora}  
    Peluquero: {peluquero}  
    
    Recorte barba: {recorte}
    Tipo de corte: {corte}
    
    TOTAL = {pago}
    
    Gracias por confiar en nosotros.
    Un saludo!
        
    """    
    msg.attach(MIMEText(message, 'plain'))  
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(user, password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        
    except smtplib.SMTPException as e:
        st.exception("Error al enviar el email")
