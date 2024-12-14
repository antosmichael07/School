let sounds = [
    "metal_pipe"
];
let loadedSounds = {};

for (let i = 0; i < sounds.length; i++) {
    loadedSounds[sounds[i]] = new Audio("./resources/sounds/" + sounds[i] + ".mp3");
}

let textures = [
    "player_left",
    "player_right",
    "bolt"
];
let loadedTextures = {};

for (let i = 0; i < textures.length; i++) {
    loadedTextures[textures[i]] = new Image();
    loadedTextures[textures[i]].src = "./resources/textures/" + textures[i] + ".png";
}
