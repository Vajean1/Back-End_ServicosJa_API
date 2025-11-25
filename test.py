def pegar_latitude_longitude_do_endereco(cep : int, rua : str, numero : int) -> tuple:
    try:
        cep_limpo = ''.join(filter(str.isdigit, cep))
        
        if len(cep_limpo) != 8:
            return None, None

        response = requests.get(f'https://brasilapi.com.br/api/cep/v2/{cep_limpo}')
        response.raise_for_status()
        data = response.json()

        if data.get('location') and data['location'].get('coordinates'):
            lat = data['location']['coordinates'].get('latitude')
            lon = data['location']['coordinates'].get('longitude')
            
            if lat and lon:
                return lat, lon

        from geopy.geocoders import Nominatim 
        
        cep_data = requests.get(f'https://viacep.com.br/ws/{cep_limpo}/json/').json()

        if "erro" in cep_data:
            return None, None

        endereco_completo = f"{rua}, {numero}, {cep_data['localidade']}, {cep_data['uf']}, Brasil"
        geolocator = Nominatim(user_agent="ServicosJa/1.0", timeout=10)
        location = geolocator.geocode(endereco_completo)

        if location:
            return location.latitude, location.longitude
        else:
            return None, None

    except Exception as error:
        print(f"Erro na geocodificação do CEP {cep}: {error}")
        return None, None

