/**
 * SCARCITY TRAP - AFTER EFFECTS AUTOMATION SCRIPT
 * Automatically creates composition structure and layer hierarchy
 *
 * Usage: File > Scripts > Run Script File > SETUP_COMPOSITIONS.jsx
 */

// Constants
var PROJECT_WIDTH = 1920;
var PROJECT_HEIGHT = 1080;
var PROJECT_FPS = 23.976;
var BG_COLOR = [1, 1, 1]; // White RGB

// Scene definitions: [name, start_time, duration]
var SCENES = [
    ["Scene 01 - Definition", 0, 1.15],
    ["Scene 02 - Limited Resources", 1.15, 1.30],
    ["Scene 03 - Decision Bandwidth", 2.45, 1.35],
    ["Scene 04 - Poor Trap", 4.20, 1.40],
    ["Scene 05 - Cognitive Capacity", 6.00, 1.30],
    ["Scene 06 - Quality of Life", 7.30, 1.30],
    ["Scene 07 - Scarcity Mindset", 9.00, 1.30],
    ["Scene 08 - Poor Decisions", 10.30, 1.30],
    ["Scene 09 - Consequences", 12.00, 1.15],
    ["Scene 10 - Path Forward", 13.15, 0.45]
];

// Convert time string (MM:SS) to seconds
function timeToSeconds(timeStr) {
    var parts = timeStr.split(":");
    return parseInt(parts[0]) * 60 + parseInt(parts[1]);
}

// Convert seconds to frame count
function secondsToFrames(seconds) {
    return Math.round(seconds * PROJECT_FPS);
}

// Create a new composition
function createComposition(name, duration_seconds) {
    if (app.project == null) {
        alert("No project open!");
        return null;
    }

    var comp = app.project.items.addComp(
        name,
        PROJECT_WIDTH,
        PROJECT_HEIGHT,
        1, // pixel aspect ratio
        secondsToFrames(duration_seconds),
        PROJECT_FPS
    );

    // Set background color
    comp.bgColor = BG_COLOR;

    return comp;
}

// Create master composition
function createMasterComposition() {
    // Master duration: 14 minutes = 840 seconds
    var masterComp = createComposition("MASTER - Scarcity Trap (14:00)", 840);

    if (masterComp == null) return null;

    // Create 10 scene compositions
    var sceneComps = [];

    for (var i = 0; i < SCENES.length; i++) {
        var scene = SCENES[i];
        var sceneName = scene[0];
        var duration = scene[2];

        var sceneComp = createComposition(sceneName, duration);

        if (sceneComp != null) {
            sceneComps.push(sceneComp);
            alert("✓ Created: " + sceneName);
        }
    }

    // Add scene compositions to master comp in reverse order
    // (so Scene 1 is on top in timeline)
    for (var i = sceneComps.length - 1; i >= 0; i++) {
        var sceneComp = sceneComps[i];
        var scene = SCENES[i];
        var startTime = timeToSeconds(scene[1].toString());

        // Create layer from composition
        var layer = masterComp.layers.add(sceneComp);

        // Set in/out times
        layer.inPoint = startTime;
        layer.outPoint = startTime + scene[2] * 60; // Convert to seconds for layer timing
    }

    alert("✓ Master composition created with all scenes!\n" +
          "Total scenes: " + sceneComps.length + "\n" +
          "Master duration: 840 seconds (14:00)");

    return masterComp;
}

// Create audio tracks in master
function createAudioTracks(masterComp) {
    // Create audio track layers (as placeholders)
    // Note: You'll need to import actual audio files manually

    var solidLayer = masterComp.layers.addSolid([0.2, 0.2, 0.2], "Audio - Placeholder", 100, 100, 1, 840);
    solidLayer.setParentWithoutChangingTerm(null);

    alert("✓ Audio track placeholders created.\n" +
          "Import your voiceover, music, and effects manually.");
}

// Create folder structure in project
function createProjectFolders() {
    var project = app.project;

    var folders = [
        "01_COMPOSITIONS",
        "02_FOOTAGE",
        "03_AUDIO",
        "04_EXPORTS"
    ];

    for (var i = 0; i < folders.length; i++) {
        var folderItem = project.items.addFolder(folders[i]);
        alert("✓ Created folder: " + folders[i]);
    }
}

// Main execution
function main() {
    // Disable dialogs for performance
    var originalDialogs = app.project.displayNewCompositionWarning;
    app.project.displayNewCompositionWarning = false;

    alert("Starting Scarcity Trap After Effects Setup...\n\n" +
          "This will create:\n" +
          "• 1 Master composition (14:00)\n" +
          "• 10 Scene compositions\n" +
          "• Project folder structure\n\n" +
          "Click OK to begin.");

    try {
        // Create project folders
        createProjectFolders();

        // Create master and scene compositions
        var masterComp = createMasterComposition();

        if (masterComp != null) {
            // Create audio track placeholders
            createAudioTracks(masterComp);

            alert("✅ SETUP COMPLETE!\n\n" +
                  "Next steps:\n" +
                  "1. Save your project\n" +
                  "2. Import generated images into appropriate scene folders\n" +
                  "3. Organize layers within each scene composition\n" +
                  "4. Import audio tracks (voiceover, music, effects)\n" +
                  "5. Begin animation and timing adjustments\n\n" +
                  "See SCARCITY_TRAP_PROJECT_SETUP.md for detailed layer structure.");
        }

    } catch (error) {
        alert("❌ Error during setup:\n" + error.toString());
    }

    // Restore dialog setting
    app.project.displayNewCompositionWarning = originalDialogs;
}

// Run main function
main();
