import requests


def run_spiders():

    spiders = [
        "canada_buyandsell",
        "canada_montreal",
        # "chile_compra_records",
        # "chile_compra_releases", #  Scraper needs fixing, not ocds format in API, need to follow links
        # "dhangadhi",
        # "georgia_opendata",
        # "georgia_records",
        # "georgia_releases",
        # "honduras_cost",
        # "honduras_oncae",
        # "indonesia_bandung",
        # "mexico_cdmx",
        # "mexico_grupo_aeroporto",
        # "mexico_inai",
        # "mexico_jalisco", # Errors https://contratacionesabiertas.jalisco.gob.mx/OCApi/2017/contracts
        # "moldova",
        # "moldova_old",
        # "moldova_records",
        # "moldova_releases",

        # Error authentication_credentials_missing
        # "paraguay_base",
        # "paraguay_dncp_records",
        # "paraguay_dncp_releases",
        # "paraguay_hacienda",

        # "scotland",

        # API link redireccts to html page http://gpp.ppda.go.ug/api/v1/releases?tag=tender&page=1
        # "uganda",


        # "uruguay",
        # "zambia",
        
    ]
    for s in spiders:
        data = {
            'project': 'kingfisher',
            'spider': s,
            'note': "Started by Sim.",
        }
        resp = requests.post("http://104.155.19.156/schedule.json", data=data)
        print(resp)

        


if __name__ == '__main__':
    run_spiders()
