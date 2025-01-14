from num2words import num2words as n2w
from word2number import w2n
import sys
import re
import uuid
import argparse
from pathlib import Path
import os
from tqdm import tqdm
import shutil
from time import time


def write_data_to_file(stats_file, file_index,path):
    called_func_name = inspect.currentframe().f_back.f_code.co_name
    if called_func_name == 'create_upgrades':
        if file_index == 0:
            file_path = WeaponUpgrades
        else:

            file_path = WeaponUpgrades.replace('ItemCombos.txt',f'ItemCombos{file_index}.txt')
    with open(file_path, 'w') as f:
        f.write(stats_file)
        f.close()
    file_index += 1
    stats_file = ''
    return stats_file, file_index
## Creates the upgrade combinations from the weapon upgrade file

def gen_combos(path,enchantment_dict):
    file = open(path, 'r').read()
    item_combo_dict = enchantment_dict
    eq_name = re.findall(r'new entry "(.+)"\n', file)
    stats_file = ''
    file_index = 0

    ## parses the stats file for the name of the upgrade
    bar_format = '{l_bar}{bar}| {n_fmt}/{total_fmt}'

    try:
        for item in tqdm(eq_name,desc='Generating Upgrade Combinations', bar_format=bar_format, colour='magenta', leave=False):
            if len(stats_file.encode('utf-8')) >= 20971520:
                stats_file, file_index = write_data_to_file(stats_file, file_index, UpgradedCombos)

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
        print('[+] Created Upgrade Combinations')
    except Exception as e:
        print(e)
        sys.exit(0)

    return stats_file




## creates a dictionary which maps number values to words based on the enchantment value specified

def create_dict(max_enchantment):
    max_enchantment = int(max_enchantment)+1
    enchantment_dict = {}
    bar_format = '{l_bar}{bar}| {n_fmt}/{total_fmt}'

    try:

        for i in tqdm(range(1,max_enchantment), bar_format=bar_format, desc='Generating Enchantment Dictionary',leave=False, colour='magenta'):
            if '-' in n2w(i):
                number_word = [ "".join(item.capitalize() for item in n2w(i).split('-'))][0]
            else:
                number_word = str.capitalize(n2w(i))

            enchantment_dict[str(i)] = number_word
            enchantment_dict[number_word] = str(i)
        print('[+] Created Enchantment Dictionary')

    except Exception as e:
        print(e)
        sys.exit(0)
    return enchantment_dict


## parses a stats file and generates upgraded versions of the items and then writes it to a new stats file

def create_upgrades(path, max_enchantment, enchantment_dict):

    stats_file = open(path,'r').read()
    stats_list = stats_file.split('\n\n')
    eq_file = ''
    bar_format = '{l_bar}{bar}| {n_fmt}/{total_fmt}'
    enchantment_type = ''

    try:

        for item in tqdm(stats_list,desc='Generating Upgrades', bar_format=bar_format, colour='magenta',leave=False):
            for i in range(1, int(max_enchantment)+1):
                enchanted_item = item
                i = str(i)
                IsWeaponType = item.count('type "Weapon"')
                IsArmorType = item.count('type "Armor"')
                if IsArmorType != 0:
                    enchantment_type = 'AC'
                    if 'data "Boosts"' not in item:
                        IsBoostsOnEquipPresent = item.count('data "BoostsOnEquip"')
                        IsBoostsPresent = item.count('data "Boosts"')

                        if IsBoostsOnEquipPresent == 0 and IsBoostsPresent == 0:
                            enchanted_item = enchanted_item + '\ndata "Boosts" "AC(0)"'
                        if IsBoostsOnEquipPresent != 0 and IsBoostsPresent == 0:
                            boosts_on_equip = re.findall(r'data "BoostsOnEquip" "(.+)"',enchanted_item)
                            append_enchantment = boosts_on_equip[0] + ';AC(0)'
                            if boosts_on_equip != []:
                                ac_boost = re.findall(r'AC\([0-9]\)',boosts_on_equip)
                                if ac_boost == []:
                                    enchanted_item = enchanted_item.replace(boosts_on_equip[0],append_enchantment)

                        if IsBoostsPresent != 0 and IsBoostsOnEquipPresent == 0:
                            boosts = re.findall(r'data "Boosts" "(.+)"',enchanted_item)
                            append_enchantment = boosts[0] + ';AC(0)'
                            if boosts != []:
                                ac_boost = re.findall(r'AC\([0-9]\)',boosts)
                                if ac_boost == []:
                                    enchanted_item = enchanted_item.replace(boosts[0],append_enchantment)
                        if IsBoostsOnEquipPresent != 0 and IsBoostsPresent != 0:
                            ac_boost = re.findall(r'AC\([0-9]\)',enchanted_item)
                            if ac_boost == []:
                                boosts = re.findall(r'data "Boosts" "(.+)"',enchanted_item)
                                append_enchantment = boosts[0] + ';AC(0)'
                                enchanted_item = enchanted_item.replace(boosts[0],append_enchantment)

                if IsWeaponType != 0:
                    enchantment_type = 'WeaponEnchantment'
                    if 'data "DefaultBoosts"' not in item:
                        enchanted_item = enchanted_item + '\ndata "DefaultBoosts" "WeaponEnchantment(0);WeaponProperty(Magical)"'
                    if 'WeaponEnchantment' not in enchanted_item:
                        default_boosts = re.findall(r'data "DefaultBoosts" "(.+)"', enchanted_item)
                        append_enchantment = default_boosts[0] + ';WeaponEnchantment(0)'
                        if default_boosts[0].count('WeaponProperty(Magical)') != 1:
                            append_enchantment + ';WeaponProperty(Magical)'
                        enchanted_item = enchanted_item.replace(default_boosts[0], append_enchantment)

                regex = re.findall(fr'{enchantment_type}\((\d)\)',enchanted_item)
                if regex == []:
                    continue
                if int(regex[0]) >= int(i):
                    continue
                if regex != []:
                    enchantment_word = '_Plus' + enchantment_dict[i]
                    item_name = re.findall(r'new entry "(.+)".*\n', enchanted_item)
                    if item_name != []:
                        item_name_updated = item_name[0] + enchantment_word
                        enchanted_item = enchanted_item.replace(f'new entry "{item_name[0]}"', f'new entry "{item_name_updated}"')
                        enchanted_item = enchanted_item.replace(f'{enchantment_type}({regex[0]})',f'{enchantment_type}({i})')
                        enchanted_item += '\n\n'
                        eq_file += enchanted_item
                    else:
                        continue
        print('[+] Created Upgrades')
    except Exception as e:
        print(e)
        sys.exit(0)
    return eq_file

def create_mod(path,modname,operation,author,description):

    if modname.count(' ') != 0:
        mod_folder = modname.replace(' ','_')
    else:
        mod_folder = modname

    folder_exists = Path(f'{path}\\{modname}').is_dir()
    if folder_exists == True:
        decision = input('The mod folder name already exists, would you like to overwrite it? Press Y/N:\n\n  ')
        if decision.lower() == 'y':
            try:
                shutil.rmtree(f'{path}\\{modname}', ignore_errors=True)
                print(f'[+] Deleted folder {modname}')
            except Exception as e:
                print(e)
                sys.exit(0)
        else:
            print(f'[!] Folder \'{modname}\' could not be deleted. Cannot continue to create the mod, the process will stop.')
            sys.exit(0)

    if folder_exists == False or decision.lower() == 'y':
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
            UpgradedCombos = f'{path}\\Public\\{mod_folder}\\Stats\\Generated\\ItemCombos.txt'
            os.mkdir(f'{path}\\Public\\{mod_folder}\\Stats\\Generated\\Data')
            WeaponUpgrades = f'{path}\\Public\\{mod_folder}\\Stats\\Generated\\Data\\Upgrades.txt'
            print('[+] Created mod file structure')

        except Exception as e:
            print(e)
            sys.exit(0)




    mod_uuid = uuid.uuid4()
    meta_lsx = f'''<?xml version="1.0" encoding="utf-8"?>
<save>
  <version major="4" minor="0" revision="9" build="331" />
  <region id="Config">
    <node id="root">
      <children>
				<node id="Dependencies" />
				<node id="ModuleInfo">
					<attribute id="Author" type="LSString" value="{author}" />
					<attribute id="CharacterCreationLevelName" type="FixedString" value="" />
					<attribute id="Description" type="LSString" value="{description}" />
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
					<attribute id="Version64" type="int64" value="36028797018963968" />
					<children>
            <node id="PublishVersion">
              <attribute id="Version64" type="int64" value="36028797018963968" />
            </node>
            <node id="Scripts" />
            <node id="TargetModes">
              <children>
                <node id="Target">
                  <attribute id="Object" type="FixedString" value="Story" />
                </node>
              </children>
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
    parser.add_argument('-d', '--description',help='Adds a custom description to the mod. Otherwise the default is "This mod was created via PyUpgrade - A script for making Weapon Mods Compatible with Kryptohack\'s UpgradeWeaponsAndArmor Mod."', default='This mod was created via PyUpgrade - A script for making Weapon Mods Compatible with Kryptohack\'s UpgradeWeaponsAndArmor Mod.', action='store')
    args = parser.parse_args()
    if args.operation == 'create_mod' and not args.modname or not args.author_name:
        parser.error("Must use '-op/--operation','-n/--modname', and '-a/--author-name' together when creating a mod.")

    description = args.description
    operation = args.operation
    max_enchantment = args.enchantment
    path = args.path
    modname = args.modname
    start_time = time()
    if operation == 'create_mod':
        author = args.author_name
        WeaponUpgrades,UpgradedCombos = create_mod(path,modname,operation,author,description)
    else:
        WeaponUpgrades = f'{path}\\WeaponUpgrades.txt'
        UpgradedCombos = f'{path}\\UpgradedCombos.txt'

    enchantment_dict = create_dict(max_enchantment)
    eq_file = create_upgrades(args.stats_file, max_enchantment, enchantment_dict)

    with open(WeaponUpgrades,'w') as fh:

        fh.write(eq_file)
        fh.close()
        print(f'[+] Upgrades written to {WeaponUpgrades}')
    item_combos = gen_combos(WeaponUpgrades, enchantment_dict)
    with open(UpgradedCombos, 'w') as fh:

        fh.write(item_combos)
        fh.close()
        print(f'[+] Upgrade Combos written to {UpgradedCombos}')
    end_time = time()
    total_time = end_time - start_time
    if total_time >= 60:
        minutes = int(total_time // 60)
        seconds = total_time % 60
        print(f'Total execution time: {minutes} minutes and {seconds:.2f} seconds')

    else: print(f'Total execution time: {total_time:.2f} seconds')


