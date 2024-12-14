class Game {
    bolts = [];
    boltSpeed = 4;
    timer = 0;
    score = 0;
    stop = false;

    player = new Player(
        canvas.width / 2 - loadedTextures["player_left"].width / 2,
        canvas.height / 2 - loadedTextures["player_left"].height / 2,
        loadedTextures["player_left"].width,
        loadedTextures["player_left"].height,
    );

    spawnBolt() {
        this.bolts.push(new Bolt(
            Math.random() * canvas.width,
            -loadedTextures["bolt"].height,
            loadedTextures["bolt"].width,
            loadedTextures["bolt"].height,
        ));
    }

    checkCollision() {
        for (let i = 0; i < this.bolts.length; i++) {
            if (this.player.x < this.bolts[i].x + this.bolts[i].width && this.player.x + this.player.width > this.bolts[i].x &&
            this.player.y < this.bolts[i].y + this.bolts[i].height && this.player.y + this.player.height > this.bolts[i].y) {
                return i;
            }
        }

        return -1;
    }

    update() {
        this.timer++;

        for (let i = 0; i < this.bolts.length; i++) {
            this.bolts[i].update(this.boltSpeed);
        }

        if (this.timer == 70) {
            this.timer = 0;

            for (let i = 0; i < 16; i++) {
                this.spawnBolt();
            }

            if (this.bolts.length > 48) {
                this.bolts.splice(0, 16);
                this.score++;
            }
        }

        this.player.update();

        let i = this.checkCollision();
        if (i != -1) {
            this.stop = true;
            this.bolts = [this.bolts[i]];
        }
    }

    draw() {
        for (let i = 0; i < this.bolts.length; i++) {
            this.bolts[i].draw();
        }

        this.player.draw();

        c.font = "20px courier new";
        c.fillStyle = "black";
        c.fillText("Score: " + this.score, 10, 30);
    }
}

function newGame() {
    lastFrameTime = Date.now();
    frameTime = 0;
    updateSpeed = 20;

    game = new Game();

    loop();
}
