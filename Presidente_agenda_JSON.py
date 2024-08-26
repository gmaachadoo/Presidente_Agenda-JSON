import argparse
import requests
import json
from datetime import datetime

parser = argparse.ArgumentParser(description='Extrair compromissos para uma data específica.')
parser.add_argument('--data', type=str, required=True, help='Data no formato DD/MM/AAAA')

args = parser.parse_args()
data_str = args.data

try:
    data = datetime.strptime(data_str, '%d/%m/%Y').strftime('%Y-%m-%d')
except ValueError:
    print("Formato de data inválido. Use o formato DD/MM/AAAA.")
    exit(1)


url = f'https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica-lula/agenda-do-presidente-da-republica/json/{data}'
request = requests.get(url)

commitments_list = []

if request.status_code == 200:
    try:
        commitments = request.json()
        if not commitments:
            print(f"Não há compromissos para a data {data_str}")
        else:
           for day in commitments:
               if day.get('day') == int(data_str.split('/')[0]):
                   if 'items' in day:
                       for compromisso in day['items']:
                           date = compromisso.get('datetime')
                           title = compromisso.get('title')
                           time = compromisso.get('start')
                           location = compromisso.get('location')
                           
                           commitments_list.append({
                               'data': date,
                               'titulo': title,
                               'horario': time,
                               'local': location
                           }) 
                    
    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON. Verifique o conteúdo da resposta.")
else:
    print(f"Erro ao acessar a URL. Status code: {request.status_code}")
    
with open('meu_arquivo_v2.json', 'w', encoding='utf-8') as arquivo_json:
    json.dump(commitments_list, arquivo_json, ensure_ascii=False, indent=4)

                
                