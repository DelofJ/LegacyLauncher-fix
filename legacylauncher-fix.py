import platform, os, json, shutil

if platform.system() == "Windows": mc_dir = os.path.join(os.getenv('APPDATA'), ".minecraft")
elif platform.system() == "Linux": mc_dir = os.path.join(os.getenv("HOME"), ".minecraft")
elif platform.system() == "Darwin": mc_dir = os.path.join(os.getenv("HOME"), "Library", "Application Support", "minecraft")
else: mc_dir = input("Enter the .minecraft path: ")

version_manifest = json.load(open(os.path.join(mc_dir, "versions", "version_manifest_v2.json")))
for i in version_manifest["versions"]:
	if i["releaseTime"] <= "2013-04-25T15:45:00+00:00": print(i["id"])
def choose():
	ver_choosen = input("Please enter the version of Minecraft you want to install the fix for: ")
	if not os.path.isfile(os.path.join(mc_dir, "versions", ver_choosen, ver_choosen + ".json")):
		print("Version not found, please launch it at least once and retry")
		return choose()
	else: return ver_choosen
ver_choosen = choose()

filename_json = os.path.join(mc_dir, "versions", ver_choosen, ver_choosen + ".json")

ver_json = json.load(open(filename_json))
scan = ["net.minecraft:launchwrapper", "org.apache.logging.log4j:log4j-api", "org.apache.logging.log4j:log4j-core", "com.mojang:authlib", "com.google.code.gson:gson", "org.apache.commons:commons-lang3", "com.google.guava:guava", "commons-io:commons-io", "commons-codec:commons-codec"]
legacylauncher_fix_lib_sup = [{"downloads": {"artifact": {"path": "org/apache/logging/log4j/log4j-api/2.8.1/log4j-api-2.8.1.jar","sha1": "e801d13612e22cad62a3f4f3fe7fdbe6334a8e72","size": 228859,"url": "https://libraries.minecraft.net/org/apache/logging/log4j/log4j-api/2.8.1/log4j-api-2.8.1.jar"}},"name": "org.apache.logging.log4j:log4j-api:2.8.1"},{"downloads": {"artifact": {"path": "org/apache/logging/log4j/log4j-core/2.8.1/log4j-core-2.8.1.jar","sha1": "4ac28ff2f1ddf05dae3043a190451e8c46b73c31","size": 1402925,"url": "https://libraries.minecraft.net/org/apache/logging/log4j/log4j-core/2.8.1/log4j-core-2.8.1.jar"}},"name": "org.apache.logging.log4j:log4j-core:2.8.1"},{"downloads": {"artifact": {"path": "com/mojang/authlib/2.3.31/authlib-2.3.31.jar","sha1": "bbd00ca33b052f73a6312254780fc580d2da3535","size": 87662,"url": "https://libraries.minecraft.net/com/mojang/authlib/2.3.31/authlib-2.3.31.jar"}},"name": "com.mojang:authlib:2.3.31"},{"downloads": {"artifact": {"path": "com/google/code/gson/gson/2.8.0/gson-2.8.0.jar","sha1": "c4ba5371a29ac9b2ad6129b1d39ea38750043eff","size": 231952,"url": "https://libraries.minecraft.net/com/google/code/gson/gson/2.8.0/gson-2.8.0.jar"}},"name": "com.google.code.gson:gson:2.8.0"},{"downloads": {"artifact": {"path": "org/apache/commons/commons-lang3/3.5/commons-lang3-3.5.jar","sha1": "6c6c702c89bfff3cd9e80b04d668c5e190d588c6","size": 479881,"url": "https://libraries.minecraft.net/org/apache/commons/commons-lang3/3.5/commons-lang3-3.5.jar"}},"name": "org.apache.commons:commons-lang3:3.5"},{"downloads": {"artifact": {"path": "com/google/guava/guava/21.0/guava-21.0.jar","sha1": "3a3d111be1be1b745edfa7d91678a12d7ed38709","size": 2521113,"url": "https://libraries.minecraft.net/com/google/guava/guava/21.0/guava-21.0.jar"}},"name": "com.google.guava:guava:21.0"},{"downloads": {"artifact": {"path": "commons-io/commons-io/2.5/commons-io-2.5.jar","sha1": "2852e6e05fbb95076fc091f6d1780f1f8fe35e0f","size": 208700,"url": "https://libraries.minecraft.net/commons-io/commons-io/2.5/commons-io-2.5.jar"}},"name": "commons-io:commons-io:2.5"},{"downloads": {"artifact": {"path": "commons-codec/commons-codec/1.10/commons-codec-1.10.jar","sha1": "4b95f4897fa13f2cd904aee711aeafc0c5295cd8","size": 284184,"url": "https://libraries.minecraft.net/commons-codec/commons-codec/1.10/commons-codec-1.10.jar"}},"name": "commons-codec:commons-codec:1.10"}]
legacylauncher_fix_flattening_layer = {"downloads": {"artifact": {"path": "net/minecraft/launchwrapper/1.12/launchwrapper-1.12.jar","sha1": "2f784ec07566fd0a912c985a3770c8d845a8af27","size": 38641,"url": "https://github.com/DelofJ/LegacyLauncher/releases/download/v1.12.1.1/launchwrapper-1.12.jar"}},"name": "net.minecraft:launchwrapper:1.12"}
legacylauncher_fix_no_flattening_layer = {"downloads": {"artifact": {"path": "net/minecraft/launchwrapper/1.12/launchwrapper-1.12.jar","sha1": "b74f75834af11ee62650866ed360fd30f2ee5ab5","size": 38612,"url": "https://github.com/DelofJ/LegacyLauncher/releases/download/v1.12.2.1/launchwrapper-1.12.jar"}},"name": "net.minecraft:launchwrapper:1.12"}

def poll():
	ask = input("Do you want the second layer of your skin to be flattened ? (y/n): ")
	if ask == "y" : return legacylauncher_fix_flattening_layer
	elif ask == "n": return legacylauncher_fix_no_flattening_layer
	else: print("I don't understand please retry"); return poll()
legacylauncher_fix = poll()

new_ver_json = dict()
for i in ver_json:
	if i != "libraries":
		new_ver_json[i] = ver_json[i]
	else:
		new_ver_json_libraries = []
		ii = 0
		for j in ver_json[i]:
			if not j["name"].split(":")[0] + ":" + j["name"].split(":")[1] in scan:
				new_ver_json_libraries.append(j)
				ii += 1
		for lib in legacylauncher_fix_lib_sup:
			new_ver_json_libraries.append(lib)
			ii += 1
		new_ver_json_libraries.append(legacylauncher_fix)
		new_ver_json[i] = new_ver_json_libraries
new_ver_json["id"] = ver_choosen + "-fix_skin"
new_folder = os.path.join(mc_dir, "versions", ver_choosen + "-fix_skin")
new_filename_json = os.path.join(mc_dir, "versions", ver_choosen + "-fix_skin", ver_choosen + "-fix_skin" + ".json")
if not os.path.exists(new_folder): os.makedirs(new_folder)
json.dump(new_ver_json, open(new_filename_json, 'w'))

filename_jar = os.path.join(mc_dir, "versions", ver_choosen, ver_choosen + ".jar")
new_filename_jar = os.path.join(mc_dir, "versions", ver_choosen + "-fix_skin", ver_choosen + "-fix_skin" + ".jar")
if os.path.isfile(filename_jar): shutil.copyfile(filename_jar, new_filename_jar)

print("Done, you can now launch " + ver_choosen + "-fix_skin")
input()
