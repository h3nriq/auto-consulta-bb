def site_map():
    SITE_MAP = {
        "inputs": {
            "busca_municipio": {
                "xpath": "/html/body/div/div[3]/div[1]/apw-ng-app/app-template/bb-layout/div/div/div/div/div/bb-layout-column/ng-component/div/div/div/app-demonstrativo-daf/form/div/div/div/bb-card/bb-card-body/bb-text-field/div/input"
            },
            "data_inicial": {
                "xpath": "/html/body/div/div[3]/div[1]/apw-ng-app/app-template/bb-layout/div[1]/div/div/div/div/bb-layout-column/ng-component/div/div/div/app-demonstrativo-daf-selecao/div/div[2]/div/div/form/bb-card/bb-card-body/div[1]/bb-date-field/bb-text-field/div/input"
            },
            "data_final": {
                "xpath": "/html/body/div/div[3]/div[1]/apw-ng-app/app-template/bb-layout/div[1]/div/div/div/div/bb-layout-column/ng-component/div/div/div/app-demonstrativo-daf-selecao/div/div[2]/div/div/form/bb-card/bb-card-body/div[2]/bb-date-field/bb-text-field/div/input"
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
                "xpath": "/html/body/div/div[3]/div[1]/apw-ng-app/app-template/bb-layout/div/div/div/div/div/bb-layout-column/ng-component/div/div/div/app-demonstrativo-daf/form/div/div/div/bb-card/bb-card-footer/div[2]/button"
            },
            "continuar_page2": {
                "xpath": "/html/body/div/div[3]/div[1]/apw-ng-app/app-template/bb-layout/div[1]/div/div/div/div/bb-layout-column/ng-component/div/div/div/app-demonstrativo-daf-selecao/div/div[2]/div/div/form/bb-card/bb-card-footer/div/button[2]"
            },
            "royalties": {
                "xpath": "/html/body/div/div[3]/div[1]/apw-ng-app/app-template/bb-layout/div[2]/div/div/bb-select-menu/bb-menu/ul/li[10]/a"
            },
             "fpm": {
                "xpath": "/html/body/div/div[3]/div[1]/apw-ng-app/app-template/bb-layout/div[2]/div/div/bb-select-menu/bb-menu/ul/li[32]/a"
            },
        },
        "select": {
            "beneficiarios": {
                "xpath": "/html/body/div[1]/div/div/div/div/form/div[2]/div/select"
            }
        },
        "span": {
            "credito_beneficiario": {
                "xpath": '//*[@id="root"]/div[3]/div[1]/apw-ng-app/app-template/bb-layout/div[1]/div/div/div/div/bb-layout-column/ng-component/div/div/div/app-demonstrativo-daf-final/div/div[2]/div/div/bb-card/bb-card-body/div/table/tbody/tr[13]/td[3]'
            }
        },
        "class": {
            "overlay_municipio": {
                "xpath": '/html/body/div/div[3]/div[1]/apw-ng-app/app-template/bb-layout/div[1]/div/div/div/div/bb-layout-column/ng-component/div/div/div/app-demonstrativo-daf-selecao/div/div[2]/div/div/form/bb-card/bb-card-body/bb-select-field[1]'
            },
            "overlay_fundo": {
                "xpath": '/html/body/div/div[3]/div[1]/apw-ng-app/app-template/bb-layout/div[1]/div/div/div/div/bb-layout-column/ng-component/div/div/div/app-demonstrativo-daf-selecao/div/div[2]/div/div/form/bb-card/bb-card-body/bb-select-field[2]'
            },
        }
    }
    
    
    return SITE_MAP
    