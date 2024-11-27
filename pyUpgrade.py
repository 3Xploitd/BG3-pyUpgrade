from num2words import num2words as n2w
from word2number import w2n
import sys
import re
import uuid
import argparse
from pathlib import Path
import os



## Creates the upgrade combinations from the weapon upgrade file

def gen_combos(path,enchantment_dict):
    file = open(path, 'r').read()
    item_combo_dict = enchantment_dict
    eq_name = re.findall(r'new entry "(.+)"\n', file)
    stats_file = ''

    ## parses the stats file for the name of the upgrade
    for item in eq_name:
        bonus_word = re.findall(r'Plus(\w+)',item)
        item2 = re.findall(r'(.+)_Plus',item)
        if item2 != []:
            item2 = item2[0]
    ## creates the name of the original item that is used to create the upgrade
            if 'PlusOne' in item:
                item2 = re.findall(r'(.+)_Plus',item)[0]
            if 'PlusTwo' in item:
                if eq_name.count(item.replace('PlusTwo','PlusOne')) !=0:
                    item2 = item.replace('PlusTwo','PlusOne')
            if 'PlusThree' in item:
                if eq_name.count(item.replace('PlusThree','PlusTwo')) !=0:
                    item2 = item.replace('PlusThree','PlusTwo')
            if 'PlusFour' in item:
                if eq_name.count(item.replace('PlusFour','PlusThree')) !=0:
                    item2 = item.replace('PlusFour','PlusThree')
            if 'PlusFive' in item:
                if eq_name.count(item.replace('PlusFive','PlusFour')) !=0:
                    item2 = item.replace('PlusFive','PlusFour')
            if 'PlusSix' in item:
                if eq_name.count(item.replace('PlusSix','PlusFive')) !=0:
                    item2 = item.replace('PlusSix','PlusFive')
            if 'PlusSeven' in item:
                if eq_name.count(item.replace('PlusSeven','PlusSix')) !=0:
                    item2 = item.replace('PlusSeven','PlusSix')
            if 'PlusEight' in item:
                if eq_name.count(item.replace('PlusEight','PlusSeven')) !=0:
                    item2 = item.replace('PlusEight','PlusSeven')
            if 'PlusNine' in item:
                if eq_name.count(item.replace('PlusNine','PlusEight')) !=0:
                    item2 = item.replace('PlusNine','PlusEight')
            if 'PlusTen' in item:
                if eq_name.count(item.replace('PlusTen','PlusNine')) !=0:
                    item2 = item.replace('PlusTen','PlusNine')
            item3 = 'OBJ_InfernalPlate'
            item4 = 'OBJ_InfernalPlate_B'
            item5 = 'OBJ_InfernalPlate_C'
    ## creates the item combination entries to be able to craft the upgrades
            item_combo = f'new ItemCombination "{item}_A"\ndata "Type 1" "Object"\ndata "Object 1" "OBJ_Everlasting_Forge"\ndata "Combine 1" "Base"\ndata "Transform 1" "None"\ndata "Type 2" "Object"\ndata "Object 2" "{item2}"\ndata "Transform 2" "Consume"\ndata "Type 3" "Object"\ndata "Object 3" "{item3}"\ndata "Transform 3" "Consume"\n\nnew ItemCombinationResult "{item}_A_1"\ndata "ResultAmount 1" "1"\ndata "Result 1" "{item}"\ndata "PreviewStatsID" "{item}"\ndata "PreviewIcon" "{item}"\n\n'
            item_combo2 = f'new ItemCombination "{item}_B"\ndata "Type 1" "Object"\ndata "Object 1" "OBJ_Everlasting_Forge"\ndata "Combine 1" "Base"\ndata "Transform 1" "None"\ndata "Type 2" "Object"\ndata "Object 2" "{item2}"\ndata "Transform 2" "Consume"\ndata "Type 3" "Object"\ndata "Object 3" "{item4}"\ndata "Transform 3" "Consume"\n\nnew ItemCombinationResult "{item}_B_1"\ndata "ResultAmount 1" "1"\ndata "Result 1" "{item}"\ndata "PreviewStatsID" "{item}"\ndata "PreviewIcon" "{item}"\n\n'
            item_combo3 = f'new ItemCombination "{item}_C"\ndata "Type 1" "Object"\ndata "Object 1" "OBJ_Everlasting_Forge"\ndata "Combine 1" "Base"\ndata "Transform 1" "None"\ndata "Type 2" "Object"\ndata "Object 2" "{item2}"\ndata "Transform 2" "Consume"\ndata "Type 3" "Object"\ndata "Object 3" "{item5}"\ndata "Transform 3" "Consume"\n\nnew ItemCombinationResult "{item}_C_1"\ndata "ResultAmount 1" "1"\ndata "Result 1" "{item}"\ndata "PreviewStatsID" "{item}"\ndata "PreviewIcon" "{item}"\n\n'
            stats_file += item_combo
            stats_file += item_combo2
            stats_file += item_combo3
        else:
            continue
    return stats_file




## creates a dictionary which maps number values to words based on the enchantment value specified

def create_dict(max_enchantment):
    max_enchantment = int(max_enchantment)+1
    enchantment_dict = {}
    for i in range(1,max_enchantment):
        if '-' in n2w(i):
            number_word = [ "".join(item.capitalize() for item in n2w(i).split('-'))][0]
        else:
            number_word = str.capitalize(n2w(i))

        enchantment_dict[str(i)] = number_word
        enchantment_dict[number_word] = str(i)
    return enchantment_dict


## parses a stats file and generates upgraded versions of the items and then writes it to a new stats file

def create_upgrades(path, max_enchantment, enchantment_dict):

    stats_file = open(path,'r').read()
    stats_list = stats_file.split('\n\n')
    eq_file = ''
    for item in stats_list:
        for i in range(1, int(max_enchantment)+1):
            enchanted_item = item
            i = str(i)
            if 'data "DefaultBoosts"' not in item:
                enchanted_item = enchanted_item + '\ndata "DefaultBoosts" "WeaponEnchantment(0);WeaponProperty(Magical)"'
            if 'WeaponEnchantment' not in enchanted_item:
                default_boosts = re.findall(r'data "DefaultBoosts" "(.+)"', enchanted_item)
                append_enchantment = default_boosts[0] + ';WeaponEnchantment(0)'
                if default_boosts[0].count('WeaponProperty(Magical)') != 1:
                    append_enchantment + ';WeaponProperty(Magical)'
                enchanted_item = enchanted_item.replace(default_boosts[0], append_enchantment)
            regex = re.findall(r'"WeaponEnchantment\((\d)\)',enchanted_item)
            if regex == []:
                continue
            if int(regex[0]) >= int(i):
                continue
            if regex != []:
                enchantment_word = '_Plus' + enchantment_dict[i]
                item_name = re.findall(r'new entry "(.+)"\n', enchanted_item)
                if item_name != []:
                    item_name_updated = item_name[0] + enchantment_word
                    enchanted_item = enchanted_item.replace(f'new entry "{item_name[0]}"', f'new entry "{item_name_updated}"')
                    enchanted_item = enchanted_item.replace(f'WeaponEnchantment({regex[0]})',f'WeaponEnchantment({i})')
                    enchanted_item += '\n\n'
                    eq_file += enchanted_item
                else:
                    continue
    return eq_file

def create_mod(path,modname,operation,author):

    if modname.count(' ') != 0:
        mod_folder = modname.replace(' ','_')
    else:
        mod_folder = modname

    if Path(f'{path}\\{modname}').is_dir() == False:
        try:

            path = f'{path}\\{modname}'
            os.mkdir(path)
            os.mkdir(f'{path}\\Mods')
            os.mkdir(f'{path}\\Mods\\{mod_folder}')
            meta_file = f'{path}\\Mods\\{mod_folder}\\meta.lsx'
            os.mkdir(f'{path}\\Public')
            os.mkdir(f'{path}\\Public\\{mod_folder}')
            os.mkdir(f'{path}\\Public\\{mod_folder}\\RootTemplates')
            os.mkdir(f'{path}\\Public\\{mod_folder}\\Stats')
            os.mkdir(f'{path}\\Public\\{mod_folder}\\Stats\\Generated')
            UpgradedCombos = f'{path}\\Public\\{mod_folder}\\Stats\\Generated\\UpgradeCombos.txt'
            os.mkdir(f'{path}\\Public\\{mod_folder}\\Stats\\Generated\\Data')
            WeaponUpgrades = f'{path}\\Public\\{mod_folder}\\Stats\\Generated\\Data\\WeaponUpgrades.txt'

        except Exception as e:
            print(e)
            sys.exit(0)


    mod_uuid = uuid.uuid4()
    meta_lsx = f'''<?xml version="1.0" encoding="utf-8"?>
<save>
	<version major="4" minor="1" revision="2" build="1" lslib_meta="v1,bswap_guids" />
	<region id="root">
		<node id="root">
			<children>
				<node id="Dependencies" />
				<node id="ModuleInfo">
					<attribute id="Author" type="LSString" value="{author}" />
					<attribute id="CharacterCreationLevelName" type="FixedString" value="" />
					<attribute id="Description" type="LSString" value="This mod was created via PyUpgrade - A script for making Weapon Mods Compatible with Kryptohack's UpgradeWeaponsAndArmor Mod." />
					<attribute id="Folder" type="LSString" value="{mod_folder}" />
					<attribute id="GMTemplate" type="FixedString" value="" />
					<attribute id="LobbyLevelName" type="FixedString" value="" />
					<attribute id="MD5" type="LSString" value="" />
					<attribute id="MainMenuBackgroundVideo" type="FixedString" value="" />
					<attribute id="MenuLevelName" type="FixedString" value="" />
					<attribute id="Name" type="FixedString" value="{mod_folder}" />
					<attribute id="NumPlayers" type="uint8" value="4" />
					<attribute id="PhotoBooth" type="FixedString" value="" />
					<attribute id="StartupLevelName" type="FixedString" value="" />
					<attribute id="Tags" type="LSWString" value="" />
					<attribute id="Type" type="FixedString" value="Add-on" />
					<attribute id="UUID" type="FixedString" value="{mod_uuid}" />
					<attribute id="Version64" type="int64" value="144820164012315624" />
					<children>
						<node id="PublishVersion">
							<attribute id="Version64" type="int64" value="144820164012315624" />
						</node>
					</children>
				</node>
			</children>
		</node>
	</region>
</save>'''

    with open(meta_file,'w') as fh:
        fh.write(meta_lsx)
        fh.close()
    return WeaponUpgrades,UpgradedCombos

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-op','--operation',help='Specify whether to create a mod containing the upgraded weapons and weapon combinations or just standalone files. Specify \'create_mod\' to automatically create the mod for you. Specify \'files_only\' to only create the upgraded weapons and combinations text files.',choices=['create_mod','files_only'],default='files_only',action='store',required=True)
    parser.add_argument('-n','--modname',help='The name of your mod',default=None,action='store')
    parser.add_argument('-e','--enchantment',help='The enchantment level to create the upgrades for. Up to 10 is supported',default='5',action='store')
    parser.add_argument('-p','--path',help='Path for the files to be saved to',action='store',required=True)
    parser.add_argument('-s','--stats-file',help='Stats file to create the weapon upgrades and combinations from',required=True)
    parser.add_argument('-a','--author-name',help='Specifies the author name for the created mod',default='test123',required=True)
    args = parser.parse_args()
    if args.operation == 'create_mod' and not args.modname or not args.author_name:
        parser.error("Must use '-op/--operation','-n/--modname', and '-a/--author-name' together when creating a mod.")

    operation = args.operation
    max_enchantment = args.enchantment
    path = args.path
    modname = args.modname
    enchantment_dict = create_dict(max_enchantment)
    eq_file = create_upgrades(args.stats_file, max_enchantment, enchantment_dict)
    if operation == 'create_mod':
        author = args.author_name
        WeaponUpgrades,UpgradedCombos = create_mod(path,modname,operation,author)
    else:
        WeaponUpgrades = f'{path}\\WeaponUpgrades.txt'
        UpgradedCombos = f'{path}\\UpgradedCombos.txt'
    with open(WeaponUpgrades,'w') as fh:
        fh.write(eq_file)
        fh.close()
    item_combos = gen_combos(WeaponUpgrades, enchantment_dict)
    with open(UpgradedCombos, 'w') as fh:
        fh.write(item_combos)
        fh.close()


