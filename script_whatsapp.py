import re
from datetime import datetime
import os

def parse_message(line, attachments_path, html, current_date, author):
    # Utilise une expression régulière pour extraire le date, l'expéditeur et le contenu du message
    pattern = r'\[(.*?)\] (.*?): (.*)'
    match = re.match(pattern, line)
    if match:
        timestamp_str, sender, content = match.groups()
        timestamp = datetime.strptime(timestamp_str, '%d/%m/%Y %H:%M:%S')
        
        print("\nContent :  ", content)

        # Formatte le message comme une bulle de discussion
        css_class = "my-message" if sender == author else "their-message"
        # Remplace les '\n' par des balises '<br>'
        formatted_content = content.replace('£', '<br>')

        # Vérifie si la date du message est différente de la date actuelle
        if current_date != timestamp.date():
            # Ajoute la date au milieu de la page
            html += f'<div class="message-container"><div class="message">{timestamp.strftime("%d/%m/%Y")}</div></div>\n'
            current_date = timestamp.date()

        html += f'<div class="message-container">'

        # Vérifie si le message contient une pièce jointe
        file_path = parse_attachment(content, attachments_path)
        if file_path:
            #return timestamp, sender, file_path  # Retourne le chemin de la pièce jointe comme contenu
            print(f"Intégration de la pièce jointe : {file_path}")
            print("extension : ", file_path[-3:])
            if file_path[-3:] != "mp4" :
                html += f'<div class="message attachment {css_class}"><img class="attachment" src="{file_path}" alt="Attachment"></div>\n'
            else : 
                html += f'<div class="message attachment {css_class}"><video class="attachment" src="{file_path}" alt="Attachment"></div>\n'

        # Si le message ne contient pas de pièce jointe, retourne le contenu normal
        else: 
            html += f'<div class="message {css_class}"><span class="sender">{sender}</span><br>{formatted_content}<br><i>{timestamp.strftime("%H:%M")}</i></div>\n'

        html += '</div>'
    return html, current_date


def parse_attachment(content, attachments_path):
    # Utilise une expression régulière pour extraire le nom de fichier de la pièce jointe
    pattern = r'< pièce jointe : (.+?) >'
    match = re.search(pattern, content)
    if match:
        print('!!! Find IT ')
        attachment_filename = match.group(1)
        file_path = os.path.join(attachments_path, attachment_filename)
        return file_path
    return None

def generate_html_layout():
    # Génère le contenu HTML à partir des messages
    html = '<html>\n<head>\n<style>\nbody { font-family: Arial, sans-serif; }\n.message-container { display: flex; flex-direction: column; align-items: center; }\n.message { max-width: 70%; margin: 10px; padding: 10px; border-radius: 15px; }\n.sender { font-weight: bold; }\n.attachment { margin-top: 5px; width: 100%; height: auto; }\n.my-message { background-color: #DCF8C6; align-self: flex-end; }\n.their-message { background-color: #E0E0E0; align-self: flex-start; }\n</style>\n</head>\n<body>\n'

    return html


def read_log_file(input_file_path, attachments_path, html_content, author):
    # Lit le fichier de logs et renvoie une liste de messages
    messages = []
    current_date = None
    with open(input_file_path, 'r', encoding='utf-8') as file:
        current_message = ""
        new_message =""
        for line in file:
            #print("/!\ Line in read :  ", line)
            # Vérifie si la ligne commence par '[' et que le contenu précédent est vide
            if line.startswith('[') and not new_message:
                current_message = line
                
            # Vérifie si la ligne commence par '[' et que le contenu précédent n'est pas vide
            elif line.startswith('[') and new_message:
                # Ajoute la ligne au contenu du message en cours
                html_content, current_date = parse_message(new_message, attachments_path, html_content, current_date, author)
                new_message = ""
                current_message += line.strip()

            elif not line.startswith('[') :
                new_message += '£' + line.strip()

            new_message += current_message
            # print("Etat new message : ", new_message)
            current_message = ""
        # Traite le dernier message s'il existe
        if new_message:
            html_content, current_date = parse_message(new_message, attachments_path, html_content, current_date, author)

    return html_content


def write_html_file(html_content, output_file_path):
    # Écrit le contenu HTML dans un fichier
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

def main(input_file_path, output_file_path, attachments_path, author):
    # Point d'entrée principal
    #messages = read_log_file(input_file_path, attachments_path)
    #html_content = generate_html(messages, attachments_path)
    
    
    html_content = generate_html_layout()
    html_content = read_log_file(input_file_path, attachments_path, html_content, author)

    write_html_file(html_content, output_file_path)

if __name__ == "__main__":
    # Vérifiez si le nombre d'arguments est correct
    import sys
    if len(sys.argv) != 5:
        print("Utilisation : python script.py chemin_fichier_log.txt chemin_sortie.html chemin_pieces_jointes author(au format du nom dans le fichier input.txt)")
    else:
        # Appel du script avec les chemins des fichiers d'entrée et de sortie
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
