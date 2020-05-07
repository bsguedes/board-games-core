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


def pint(value):
    return float(value) if value != '' else 0


def parse_bonus(sheet):
    return [
        {
            "ID": c['ID'],
            "Name": c['Nome'],
            "Criterion": c['Habilidade'],
            "Range1": c['Range1'],
            "ScoreRange1": c['ScoreRange1'],
            "Range2": c['Range2'],
            "ScoreRange2": c['ScoreRange2'],
            "ScoreRangeCard": c['ScoreRangeCard']
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
            "TopRow": c['A1'],
            "MidRow": c['A2'],
            "BottomRow": c['A3'],
            "Cash": c['Cash'],
            "Attribute": c['Label'],
            "DefaultPoints": 10,
            "Points": c['Points'],
            "CE": c['Age'],
            "Year": c['Year'],
            "AbilityID": c['AbID'],
            "Cost": {
                "X1": c['X1'],
                "X2": c['X2'],
                "X3": c['X3'],
                "X4": c['X4'],
                "X5": c['X5'],
                "X": c['X']
            },
            "Gender": c['Gender'],
            "Lore": c['Lore']
        } for c in sheet[2:]
    ]
    return card_list


def parse_teams(sheet):
    return []


cards_json = parse_cards(cards)
teams_json = parse_teams(teams)
abilities_json = parse_abilities(abilities)
bonus_json = parse_bonus(bonus)

with open('v1.json', 'w') as fp:
    json.dump({
        "Cards": cards_json,
        "Champions": teams_json,
        "Abilities": abilities_json,
        "Bonus": bonus_json
    }, fp, indent=True, ensure_ascii=False)
