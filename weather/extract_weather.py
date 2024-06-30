import requests
import csv
import time
from datetime import datetime

input_file = 'modis_2023_France.csv'
output_file = 'coordinates_updated4.csv'
api_key = 'dddda3a28cf44f32bea55d694b901a70'
start_date = datetime(2023, 1, 1)

def fetch_weather_data(latitude, longitude):
    url = f'https://api.weatherbit.io/v2.0/current?lat={latitude}&lon={longitude}&key={api_key}&units=M'

    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()

    except requests.exceptions.RequestException as e:
        print(f'Erreur lors de la requête API : {e}')
        return None

def main():
    try:
        with open(input_file, 'r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            data_rows = []
            for row in reader:
                try:
                    acq_date = datetime.strptime(row[5], '%Y-%m-%d')
                except ValueError:
                    print(f"Ignoré: Date invalide pour la ligne {reader.line_num}: {row[5]}")
                    continue

                if acq_date >= start_date:
                    data_rows.append({
                        'latitude': row[0],
                        'longitude': row[1],
                        'acq_date': row[5],
                        'temp': '',
                        'wind_speed': '',
                        'description': '',
                        'humidity': '',
                    })
        with open(output_file, 'w', newline='') as file:
            fieldnames = ['latitude', 'longitude', 'acq_date', 'temp', 'wind_speed', 'description', 'humidity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            for data_row in data_rows:
                latitude, longitude = data_row['latitude'], data_row['longitude']

                attempt = 1
                while attempt <= 3:
                    data = fetch_weather_data(latitude, longitude)
                    if data:
                        if 'data' in data and len(data['data']) > 0:
                            weather_data = data['data'][0]
                            temp = weather_data['temp']
                            wind_speed = weather_data['wind_spd']
                            description = weather_data['weather']['description']
                            humidity = weather_data['rh']
                            data_row['temp'] = temp
                            data_row['wind_speed'] = wind_speed
                            data_row['description'] = description
                            data_row['humidity'] = humidity
                            writer.writerow(data_row)
                            break
                        else:
                            print(f'Données météorologiques non trouvées pour la latitude {latitude}, longitude {longitude}')
                            break
                    else:
                        wait_time = 5 * attempt
                        print(f'Attente avant la nouvelle tentative dans {wait_time} secondes...')
                        time.sleep(wait_time)
                        attempt += 1

                if attempt > 3:
                    print(f'Impossible de récupérer les données pour la latitude {latitude}, longitude {longitude}')

        print(f'Données météorologiques mises à jour sauvegardées dans {output_file}')

    except FileNotFoundError:
        print('Erreur: Fichier non trouvé. Assurez-vous que le fichier CSV existe et est nommé correctement.')
    except IndexError:
        print('Erreur: Format incorrect du fichier CSV. Assurez-vous que chaque ligne a des valeurs de latitude et longitude.')
    except KeyError as e:
        print(f'Erreur: KeyError - {e}. Vérifiez la structure de la réponse de l\'API.')
    except requests.exceptions.HTTPError as e:
        print(f'Erreur HTTP lors de la requête : {e}')
    except requests.exceptions.RequestException as e:
        print(f'Erreur lors de la requête API : {e}')

if __name__ == "__main__":
    main()
