import pandas as pd
import streamlit as st
import os
from git import Repo
from PIL import Image

repo = Repo(os.getcwd())
st.set_page_config(
    page_title='CessAdvisor',
    page_icon = ":poop:"
)

st.write('# CessAdvisor')

perc = 'foto'
data = pd.read_csv("cess_data.csv", delimiter=';')

selected_toilet = st.selectbox("Seleziona Cesso ", data['nome'])
if selected_toilet:
    toilet_row = data[data['nome'] == selected_toilet]
    nome = toilet_row["nome"].iloc[0]
    st.write("## "+nome)
    com = toilet_row["commento"].iloc[0]
    st.write(com)
    voto = (toilet_row["voto"].iloc[0])
    if voto == 0:
        st.write("### Voto: 0 💩")
    else:
        if voto == 0.5:
            st.write("### 1/2 💩")
        else:
            if (voto %1 != 0):
                flag = True
            else:
                flag = False
            voto = int(toilet_row["voto"].iloc[0])
            vote = ""
            for i in range(voto):
                vote += "💩"
            if (flag) != 0:
                vote += " e 1/2"

            st.write("### Voto: "+vote)
    st.image(os.path.join(perc,(toilet_row['foto'].iloc[0])), width = 250)
    autore = toilet_row["autore"].iloc[0]
    st.write("Recensito da " +autore)


# Create a session state variable to keep track of whether or not the form should be displayed
if 'show_form' not in st.session_state:
    st.session_state.show_form = False

# Create a button to show/hide the form
if st.button("Inserisci nuova recensione"):
    st.session_state.show_form = not st.session_state.show_form

# Only display the form if show_form is True
if st.session_state.show_form:
    # Define the path to the CSV file
    csv_path = "cess_data_to_approve.csv"
    # Create a form to enter new data
    st.subheader("Inserisci nuova recensione")
    new_data = st.form(key='my_form')
    Nome = new_data.text_input("nome")
    Voto = new_data.number_input("voto", min_value = 0.0, max_value = 5.0, step = 0.5)
    Commento = new_data.text_input("commento")
    Autore = new_data.text_input("Autore")
    Foto = new_data.file_uploader("Immagine")
    submit_button = new_data.form_submit_button(label='Invia')
    # If the user clicks the submit button, append the new data to the CSV file
    if submit_button:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_path, delimiter=';')
        # Create a new row with the new data
        if Foto is not None:
            # Open the uploaded image file
            image = Image.open(Foto)
            
            # Get the file extension of the uploaded image
            file_ext = os.path.splitext(Foto.name)[1]
            
            # Create a new file name using the entered name and the original file extension
            Nome_Foto = f"{Nome}{file_ext}"
            
            # Save the image using the new file name
            image.save(os.path.join(perc,Nome_Foto))
            new_row = {'nome': Nome, 'voto': Voto, 'commento': Commento, 'autore' : Autore, 'foto' : Nome_Foto}
        else:
            new_row = {'nome': Nome, 'voto': Voto, 'commento': Commento, 'autore' : Autore}
        # Append the new row to the DataFrame
        df = df.append(new_row, ignore_index=True, )
        # Write the updated DataFrame back to the CSV file
        df.to_csv('prova.csv', index=False, header = False, sep = ";", mode = 'a')
        repo.index.add(['prova.csv'])
        repo.index.commit('aggiunti dati da validare')
        # Show a success message
        st.success("Nuovo cesso aggiunto, in attesa di approvazione!")
