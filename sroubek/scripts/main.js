let canvas = document.getElementById("canvas");
let c = canvas.getContext("2d");
let lastFrameTime;
let frameTime;
let updateSpeed;
let game;

function loop() {
    if (!game.stop) {
        frameTime += Date.now() - lastFrameTime;
        lastFrameTime = Date.now();

        // Updating variables
        if (frameTime >= updateSpeed) {
            frameTime -= updateSpeed;

            game.update();
        }

        clearBackground("skyblue");

        game.draw();

        requestAnimationFrame(loop);
        return;
    } else {
        fillTextCenter("Game over!", "bold 60px courier new", "red", 250, 3);
        fillTextCenter("Your final score is: " + game.score, "bold 30px courier new", "red", 300, 2);

        loadedSounds["metal_pipe"].play();
    }
}

newGame();
