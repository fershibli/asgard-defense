# Asgard Defense

A tower defense based on Norse mythology: the heroes of Asgard must hold back the invasion of the other realms of Yggdrasil. Place Valkyries, Berserkers, Archers and Vikings along the path to stop the waves of enemies.

Developed in 2014 in the 4th semester of Digital Games at **Fatec Sao Caetano do Sul** by the group **Asgardian AGES**, and later presented at HappyCode.

## Features

- Four tower classes (Valkyrie, Berserker, Archer, Viking) placed on the map.
- Enemy waves following predefined paths, lives, mana and score.
- The game design document also planned colored armor types, tower upgrades and bosses such as the dragon Fafner.
- Stage select, tutorial, options (music, FPS) and credits screens.
- `Criador de Mapas.py`: the level editor I wrote to draw the maps and enemy paths (`exported_mapa.txt`, `exported_caminhos.txt`).
- UI built on `pyTreeBee`, my small pygame widget library.

## History

From `v001` (Aug 2014) to `v035` (Dec 2014), one commit per version, dated from the original files and art exports.

## Team - Asgardian AGES

| Name | Role |
|---|---|
| Maria Tereza Font Fernandes | Producer |
| Luiz Gustavo "Manchae" Pelatieri | Game designer / Artist |
| Fabrício do Nascimento | Artist / Writer |
| Guilherme "Freak" de Almeida | Programmer / Artist |
| Fernando Luiz Neme Chibli ([@fershibli](https://github.com/fershibli)) | Programmer |

In 2015 the same team went on to work on BGS.

## License

Asgard Defense by Asgardian AGES is licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). Music tracks are royalty-free tracks from their respective authors.

## Releases

Builds are made by GitHub Actions (`.github/workflows/release.yml`) for macOS, Windows and Linux. Push a tag such as `v1.0` (or run the workflow by hand) and the zipped builds are attached to a GitHub release.

The game is Python 2.7, which GitHub runners no longer ship: Linux builds inside the official `python:2.7` Docker image, Windows installs it with Chocolatey, and macOS uses the Intel installer through Rosetta (that job is allowed to fail).

To play from source: `python2.7 asgard_defense.py`.
