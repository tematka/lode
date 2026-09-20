# lode
Hra lodě pro jednoho hráče proti počítači

## instalace
Je potřeba mít stažený python a pygame. Samotná hra se spustí spuštěním souboru main.py

## popis hry
### pokládání lodí
Po spuštění se oběví okno s tabulkou 10 x 10 do které hráč umístí své lodě. Loď umístí tak, že klikne na bílé políčko. Pokud se dá loď umístit, objeví se modrá políčka kde může být konec lodi kterou aktuálně imisťuje. Po kliknuti na nějaké z těchto políček se pole kde byla umístěna loď zbarví do zelena a a okolní pole kam již nesmí být položena loď do červena. Hra nedovolí položit loď pokud tam na ní není místo. V takovém případě se nic neděje, dokud není vybrané místo pro loď, kde být položena může

### střílení
Po položení lodí hráčem položí své lodě na pozadí počítač a začíná samotná hra. Poté se oběví dvě tabulky. V levé tabulce zadává hráč své střeli a pokud se trefí do lodě počítače, zbarví se toto pole na červeno. Pokud na trefeném poli není loď, sbarví se do modra. Pokud hráč potopí celou loď počítače, sbarví se všechna pole okolo lodě do modra. V pravé tabulce jsou potom zobrazené hráčovi lodě. Pole na kterých jsou položené lodě jsou v tabulce zelené. Dále se v pravé tabulce zobrazuje jak střílí počítač. Trefy lodí a vody jsou zobrazené v pravé tabulce stejně jako u hráče

### vyhodnocení 
V okamžiku, kdy hráč nebo počítač potopí protivníkovi všechny lodě, zavře se grafické okno s hrou a do konzole se vypíše kdo vyhrál.
