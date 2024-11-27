# pyUpgrade
A Python Script to create item upgrades to be compatible with KryptoHack's Upgrade Weapons And Armor mod. This script can be used to create standalone stats and itemCombo files or create a mod. The only requirement is that you must have a Weapons.txt file from another mod you want to create the upgrades for, Armor stats files aren't supported yet (but will be soon). 

## Usage
~~~python
usage: pyUpgrade.py [-h] -op {create_mod,files_only} [-n MODNAME] [-e ENCHANTMENT] -p PATH -s STATS_FILE
                                 -a AUTHOR_NAME

options:
  -h, --help            show this help message and exit
  -op {create_mod,files_only}, --operation {create_mod,files_only}
                        Specify whether to create a mod containing the upgraded weapons and weapon combinations or
                        just standalone files. Specify 'create_mod' to automatically create the mod for you. Specify
                        'files_only' to only create the upgraded weapons and combinations text files.
  -n MODNAME, --modname MODNAME
                        The name of your mod
  -e ENCHANTMENT, --enchantment ENCHANTMENT
                        The enchantment level to create the upgrades for. Up to 10 is supported
  -p PATH, --path PATH  Path for the files to be saved to
  -s STATS_FILE, --stats-file STATS_FILE
                        Stats file to create the weapon upgrades and combinations from
  -a AUTHOR_NAME, --author-name AUTHOR_NAME
~~~


### create mod

~~~
python3 pyUpgrade.py --operation create_mod --mod-name test123 --author-name yourname123 --enchantment 5 --path 'C:\Mods' --stats-file 'C:\Mods\somemod\Public\somemod\Stats\Data\Weapons.txt'
~~~

### create standalone stats files

~~~
python3 pyUpgrade.py --operation files_only --enchantment 5 --path 'C:\Mods' --stats-file 'C:\Mods\somemod\Public\somemod\Stats\Data\Weapons.txt'
~~~
