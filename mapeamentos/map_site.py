def site_map():
    SITE_MAP = {
        "inputs": {
            "busca_municipio": {
                "xpath": "/html/body/div[1]/div/div/div/div/form/div[2]/div/input"
            },
            "data_inicial": {
                "xpath": "/html/body/div[1]/div/div/div/div/form/div[3]/div/input"
            },
            "data_final": {
                "xpath": "/html/body/div[1]/div/div/div/div/form/div[4]/div/input"
            },
            "imprimir": {
                "xpath": "/html/body/div[1]/div/div/div/div/form/div/div[2]/div/div[2]/span[1]/input"
            },
            "voltar": {
                "xpath": "/html/body/div[1]/div/div/div/div/form/div/div[2]/div/div[2]/span[2]/input"
            }
        },
        "buttons": {
            "continuar": {
                "xpath": "/html/body/div[1]/div/div/div/div/form/div[3]/div/input[1]"
            },
            "continuar_page2": {
                "xpath": "/html/body/div[1]/div/div/div/div/form/div[6]/div/input[1]"
            }
        },
        "select": {
            "beneficiarios": {
                "xpath": "/html/body/div[1]/div/div/div/div/form/div[2]/div/select"
            }
        },
        "span": {
            "credito_beneficiario": {
                "xpath": '//*[@id="formulario:demonstrativoList:2:subTableLancamentos:2:j_id41"]/span',
                "id_td": "j_id41",
                "class_span": "extratoValorPositivo"
            }
        }
    }
    
    
    return SITE_MAP
    