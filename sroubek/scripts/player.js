const directionLeft  = 0;
const directionRight = 1;

class Player {
    speed = 8;
    direction = directionLeft;
    hasSquished = false;

    constructor(x, y, width, height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }

    update() {
        if (inputs[inputSquish]) {
            if (!this.hasSquished) {
                this.width /= 2;
                this.x += this.width / 2
            }
            this.hasSquished = true;
            return;
        } else {
            if (this.hasSquished) {
                this.x -= this.width / 2
                this.width *= 2;
            }
            this.hasSquished = false;
        }

        if (inputs[inputUp]) {
            this.y -= this.speed;
        }
        if (inputs[inputDown]) {
            this.y += this.speed;
        }
        if (inputs[inputLeft]) {
            this.x -= this.speed;
            this.direction = directionLeft;
        }
        if (inputs[inputRight]) {
            this.x += this.speed;
            this.direction = directionRight;
        }

        if (this.x < 0) {
            this.x = 0;
        }
        if (this.x > canvas.width - this.width) {
            this.x = canvas.width - this.width;
        }
        if (this.y < 0) {
            this.y = 0;
        }
        if (this.y > canvas.height - this.height) {
            this.y = canvas.height - this.height;
        }
    }

    draw() {
        if (this.direction == directionLeft) {
            c.drawImage(loadedTextures["player_left"], this.x, this.y, this.width, this.height);
        } else {
            c.drawImage(loadedTextures["player_right"], this.x, this.y, this.width, this.height);
        }
    }
}
