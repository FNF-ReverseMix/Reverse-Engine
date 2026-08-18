package;

import flixel.FlxG;
import flixel.FlxState;
import flixel.text.FlxText;

class MainMenuState extends FlxState
{
    var menuItems:Array<String> = ["Story Mode", "Freeplay", "Options"];
    var curSelected:Int = 0;
    var textObjects:Array<FlxText> = [];

    override public function create():Void
    {
        super.create();
        
        for (i in 0...menuItems.length) {
            var menuText = new FlxText(100, 200 + (i * 80), 0, menuItems[i], 32);
            textObjects.push(menuText);
            add(menuText);
        }
        updateSelection();
    }

    override public function update(elapsed:Float):Void
    {
        super.update(elapsed);

        // Simple FNF-style menu navigation
        if (FlxG.keys.justPressed.UP) {
            curSelected -= 1;
            if (curSelected < 0) curSelected = menuItems.length - 1;
            updateSelection();
        }
        if (FlxG.keys.justPressed.DOWN) {
            curSelected += 1;
            if (curSelected >= menuItems.length) curSelected = 0;
            updateSelection();
        }
    }

    function updateSelection():Void
    {
        // Highlight selected text item
        for (i in 0...textObjects.length) {
            if (i == curSelected)
                textObjects[i].color = 0xFFFFFF00; // Yellow
            else
                textObjects[i].color = 0xFFFFFFFF; // White
        }
    }
}

