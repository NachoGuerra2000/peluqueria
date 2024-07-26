import streamlit as st
from streamlit_option_menu import option_menu
import os
from PIL import Image
from send_email import send
from google_sheets import GoogleSheets
import re
import uuid
from google_calendar import GoogleCalendar
import numpy as np
import datetime as dt

page_title = "Barberia"
page_icon ="🔎"
layout = "centered"

horas = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "17:30", "18:30", "19:30", "20:30"]
peluquero =["Cesar", "Oscar"]
pago =["","Efectivo($5000)", "Tarjeta($5500)", "Qr($5500)"]
recorte =["","Si", "No"]

document = "gestion-reservas"
sheet = "reservas"
credentials = st.secrets["google"]["credentials_google"]
idcalendar = "ustust1233@gmail.com"
idcalendar2 = "f307764522840717a5493f13900a3f15293c96e05d5deedd23fb27101904c4b1@group.calendar.google.com"
time_zone = "America/Argentina/Buenos_Aires"

def validate_email(email):
    pattern = r'^[\w.-]+@[\w.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False
    
def generate_uid():
    return str(uuid.uuid4())

def add_hour(time):
    parsed_time = dt.datetime.strptime(time, "%H:%M").time()
    new_time = (dt.datetime.combine(dt.date.today(), parsed_time) +dt.timedelta(hours=1, minutes=0)).time()
    return new_time.strftime("%H:%M")
    

st.set_page_config(page_title=page_title,page_icon=page_icon, layout=layout)

st.image("assets/Captura de pantalla (335).png")
st.title("CESAR Salon de Peluqueria")
st.text("Av. Aconquija 2018")

selected = option_menu(menu_title=None, options=["Reservar", "Portafolio", "Detalles"],
                        icons=["calendar-date", "building","clipboard-minus"],
                        orientation="horizontal")

if selected == "Detalles":
    st.subheader("Ubicacion")
    st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d3560.8638493303943!2d-65.2993795!3d-26.812463499999996!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1ses-419!2sar!4v1717094214921!5m2!1ses-419!2sar" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""",unsafe_allow_html=True)
    
    st.subheader("Horarios")
    dia, hora = st.columns(2)
    
    dia.text("Lunes")
    hora.text("8:00 a 13:00 - 17:30 a 20:30")
    dia.text("Martes")
    hora.text("8:00 a 13:00 - 17:30 a 20:30")
    dia.text("Miercoles")
    hora.text("8:00 a 13:00 - 17:30 a 20:30")
    dia.text("Jueves")
    hora.text("8:00 a 13:00 - 17:30 a 20:30")
    dia.text("Viernes")
    hora.text("8:00 a 13:00 - 17:30 a 20:30")
    dia.text("Sabado")
    hora.text("8:00 a 13:00 - 17:30 a 20:30")
    
    
    
    st.subheader("Instagram")
    st.markdown("Siguenos [aqui](https://www.instagram.com/saloncesaryerbabuena/) en Instagram")

if selected == "Portafolio":
    def load_images(image_folder):
        images = []
        for file_name in os.listdir(image_folder):
            if file_name.endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                img_path = os.path.join(image_folder, file_name)
            images.append(img_path)
        return images

    def image_carousel(images, image_width):
        current_image = st.session_state.get('current_image', 0)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if st.button('Prev'):
                if current_image > 0:
                    st.session_state.current_image = current_image - 1

        with col2:
            st.image(images[current_image],width=image_width)

        with col3:
            if st.button('Next'):
                if current_image < len(images) - 1:
                    st.session_state.current_image = current_image + 1

        
        
            
    st.title('Carrusel de Fotos')

    
    image_folder = 'assets'
    images = load_images(image_folder)
    if images:
        image_carousel(images,image_width=300)
        st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!4v1717095853401!6m8!1m7!1so2s2pZiTT3enEMNB_OKpsQ!2m2!1d-26.81231066269706!2d-65.2993872512011!3f182.89651259999687!4f-13.092193534363744!5f0.7820865974627469" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""", unsafe_allow_html=True)
    else:
        st.write('No se encontraron imágenes en la carpeta especificada.')

        #st.image("assets/captura de pantalla (331).png", caption="Esta es una foto de la peluqueria")
        #st.image("assets/captura de pantalla (332).png", caption="Cliente satisfecho")
        #st.image("assets/captura de pantalla (333).png", caption="Otro cliente")
        #st.image("assets/captura de pantalla (334).png", caption="Foto del Lugar")
        
if selected == "Reservar":
    st.subheader("Reservar")
    c1, c2 = st.columns(2)
    
    nombre = c1.text_input("Tu nombre*")
    email = c2.text_input("Tu email*")
    fecha = c1.date_input("Fecha")
    peluquero = c1.selectbox("Peluquero", peluquero)
    if fecha:
        if peluquero == "Cesar":
            id = idcalendar
        elif peluquero == "Oscar":
            id = idcalendar2
        calendar = GoogleCalendar(credentials, id)
        hours_blocked = calendar.get_events_start_time(str(fecha))
        result_hours = np.setdiff1d(horas, hours_blocked)
        
    hora = c2.selectbox("Hora", result_hours)
    pago = c1.selectbox("Metodo de Pago*", pago)
    recorte = c1.selectbox("Recorte de Barba", recorte)
    corte = c2.text_area("Tipo de Corte")
    
    enviar = st.button("Reservar")
    
    st.text("SI QUERES CANCELAR EL TURNO, LLAMA A ESTE NUMERO")
    st.text("📞 03815189918")
    
    
    if enviar:
        with st.spinner("Cargando..."): 
            
            if nombre =="":
                st.warning("El nombre es obligatorio")
            elif email =="":
                st.warning("El email es obligatorio")            
            elif not validate_email(email):
                st.warning("El email no es valido")    
            else:
                parsed_time = dt.datetime.strptime(hora, "%H:%M").time()
                hours1 = parsed_time.hour
                minutes1 = parsed_time.minute
                end_hours = add_hour(hora)
                parsed_time2 = dt.datetime.strptime(end_hours, "%H:%M").time()
                hours2 = parsed_time2.hour
                minutes2 = parsed_time2.minute
                start_time = dt.datetime(fecha.year, fecha.month, fecha.day, hours1-3, minutes1).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
                end_time = dt.datetime(fecha.year, fecha.month, fecha.day, hours2-3, minutes2).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
                calendar = GoogleCalendar(credentials, id)
                calendar.create_event(nombre, start_time,end_time,time_zone)
                
                uid = generate_uid()
                data = [[nombre, email, str(fecha), hora, peluquero, pago, corte]]
                gs = GoogleSheets(credentials, document, sheet)
                range = gs.get_last_row_range()
                gs.write_data(range, data)
                
                
                send(email, nombre, fecha, hora, peluquero, pago, recorte, corte,)
            
            
            st.success("Su turno fue reservado con exito")    
            
            