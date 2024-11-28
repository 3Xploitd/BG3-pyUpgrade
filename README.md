# pyUpgrade
A Python Script to create item upgrades to be compatible with KryptoHack's Upgrade Weapons And Armor mod. This script can be used to create standalone stats and itemCombo files or create a mod. The only requirement is that you must have a Weapons.txt file from another mod you want to create the upgrades for, Armor stats files aren't supported yet (but will be soon). 

## Usage
~~~python
usage: pyUpgrade.py [-h] -op {create_mod,files_only} [-n MODNAME] [-e ENCHANTMENT] -p PATH -s STATS_FILE -a AUTHOR_NAME
                                 [-d DESCRIPTION]

options:
  -h, --help            show this help message and exit
  -op {create_mod,files_only}, --operation {create_mod,files_only}
                        Specify whether to create a mod containing the upgraded weapons and weapon combinations or just standalone
                        files. Specify 'create_mod' to automatically create the mod for you. Specify 'files_only' to only create the
                        upgraded weapons and combinations text files.
  -n MODNAME, --modname MODNAME
                        The name of your mod
  -e ENCHANTMENT, --enchantment ENCHANTMENT
                        The enchantment level to create the upgrades for. Up to 10 is supported
  -p PATH, --path PATH  Path for the files to be saved to
  -s STATS_FILE, --stats-file STATS_FILE
                        Stats file to create the weapon upgrades and combinations from
  -a AUTHOR_NAME, --author-name AUTHOR_NAME
                        Specifies the author name for the created mod
  -d DESCRIPTION, --description DESCRIPTION
                        Adds a custom description to the mod. Otherwise the default is "This mod was created via PyUpgrade - A
                        script for making Weapon Mods Compatible with Kryptohack's UpgradeWeaponsAndArmor Mod."
~~~


### create mod

~~~
python3 pyUpgrade.py --operation create_mod --mod-name test123 --author-name yourname123 --enchantment 5 --path 'C:\Mods' --stats-file 'C:\Mods\somemod\Public\somemod\Stats\Data\Weapons.txt'
~~~

### create standalone stats files

~~~
python3 pyUpgrade.py --operation files_only --enchantment 5 --path 'C:\Mods' --stats-file 'C:\Mods\somemod\Public\somemod\Stats\Data\Weapons.txt'
~~~

### Things of Note
The script doesn't currently support armor files only weapons, don't worry though this will be coming soon. Depending on the number of weapons in the original mod it can take quite some time to create all the necessary combinations, in the future I am looking at speeding this up. If there are issues from the script make sure the weapons file you are using follows a similar format as below:

~~~
new entry "somename"
type "Weapon"
using "WPN_Shortbow_1"
Damage Type "Piercing"
data "RootTemplate" "some RootTemplateId"
data "ValueUUID" ""
data "Rarity" "Rare"
data "DefaultBoosts" "WeaponEnchantment(1);WeaponProperty(Magical)"
data "WeaponFunctors" ""
data "PassivesOnEquip" ""
data "Boosts" ""
data "StatusOnEquip" ""
data "BoostsOnEquipMainHand"  "UnlockSpell(Projectile_HamstringShot)"
data "Unique" "1"

new entry "somename"
type "Weapon"
using "WPN_Shortbow_1"
Damage Type "Piercing"
data "RootTemplate" "some RootTemplateId"
data "ValueUUID" ""
data "Rarity" "Rare"
data "DefaultBoosts" "WeaponEnchantment(2);WeaponProperty(Magical)"
data "WeaponFunctors" ""
data "PassivesOnEquip" ""
data "Boosts" ""
data "StatusOnEquip" ""
data "BoostsOnEquipMainHand"  "UnlockSpell(Projectile_HamstringShot)"
data "Unique" "1"
~~~

The order of the fields doesn't matter, neither does if they are all there. The regex used by the script should eliminate any issues but if any do arise this is the first thing I would check.
