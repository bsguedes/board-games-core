import os
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(os.environ['DOCS_KEY'], scope)
client = gspread.authorize(credentials)

spreadsheet = client.open('ClassificacaoEtaria')

cards = spreadsheet.get_worksheet(0).get_all_records()
teams = spreadsheet.get_worksheet(1).get_all_records()
abilities = spreadsheet.get_worksheet(2).get_all_records()
bonus = spreadsheet.get_worksheet(3).get_all_records()
objectives = spreadsheet.get_worksheet(4).get_all_records()


def pint(value):
    return int(value) if value != '' else 0


def pfloat(value):
    return float(value) if value != '' else 0


def parse_bonus(sheet):
    return [
        {
            "ID": c['ID'],
            "Name": c['Nome'],
            "Criterion": c['Habilidade'],
            "Range1": str(c['Range1']),
            "ScoreRange1": pint(c['ScoreRange1']),
            "Range2": str(c['Range2']),
            "ScoreRange2": pint(c['ScoreRange2']),
            "ScoreRangeCard": pint(c['ScoreRangeCard'])
        } for c in sheet[0:]
    ]


def parse_abilities(sheet):
    return [
        {
            "ID": c['ID'],
            "Type": c['Tipo'],
            "Text": c['Texto'],
            "Expansion": c['Expansao'],
        } for c in sheet[0:]
    ]


def parse_cards(sheet):
    card_list = [
        {
            "ID": c['ID'],
            "Name": c['Name'],
            "TopRow": c['A1'] == 'TRUE',
            "MidRow": c['A2'] == 'TRUE',
            "BottomRow": c['A3'] == 'TRUE',
            "Cash": c['Cash'].count("$"),
            "Attribute": c['Label'],
            "DefaultPoints": 10,
            "Points": int(c['Points']),
            "CE": str(c['Age']),
            "Year": int(c['Year']),
            "AbilityID": int(c['AbID']),
            "Cost": {
                "X1": pfloat(c['X1']),
                "X2": pfloat(c['X2']),
                "X3": pfloat(c['X3']),
                "X4": pfloat(c['X4']),
                "X5": pfloat(c['X5']),
                "X": pfloat(c['X'])
            },
            "Gender": c['Gender'],
            "Lore": c['Lore'],
            "ImgPath": c['ImgPath']
        } for c in sheet[2:]
    ]
    return card_list


def parse_teams(sheet):
    return [
        {
            "Level": int(c['Nivel']),
            "Channel": c['Emissora'],
            "Champion": c['Campeao'],
            "Points": int(c['Pontos']),
            "CashCost": c['CustoHabilidade'].count("$"),
            "CardCost": c['CustoHabilidade'].count("{C}"),
            "TalentCost": {
                "X1": c['CustoHabilidade'].count("{X1}"),
                "X2": c['CustoHabilidade'].count("{X2}"),
                "X3": c['CustoHabilidade'].count("{X3}"),
                "X4": c['CustoHabilidade'].count("{X4}"),
                "X5": c['CustoHabilidade'].count("{X5}"),
                "X": c['CustoHabilidade'].count("{X}")
            },
            "AbilityID": int(c['IDAbility']),
            "AbilityName": c['Habilidade'],
            "AbilityType": c["TipoHabilidade"],
            "AbilityText": c["TextoHabilidade"]
        } for c in sheet[0:]
    ]


def parse_objectives(sheet):
    return sheet[0:]


with open('v1.json', 'w') as fp:
    json.dump({
        "Cards": parse_cards(cards),
        "Champions": parse_teams(teams),
        "Abilities": parse_abilities(abilities),
        "Bonus": parse_bonus(bonus),
        "Objectives": parse_objectives(objectives)
    }, fp, indent=True, ensure_ascii=False)
