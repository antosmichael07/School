const socket = io();

const canvas = document.getElementById('canvas');
const c = canvas.getContext('2d');

const info = document.getElementById('info');
const modalGameFull = new bootstrap.Modal(document.getElementById('gameFullModal'));

let thisPlayer = ' ';
let lastMove;
let tileCount;
let tileSize;
let fontSize;
const tileBorderColor = '#aaa';
const tileColor = '#fff';
const tileColorHighlighted = '#ff0';

function drawBackground() {
    c.fillStyle = tileBorderColor;
    c.fillRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < tileCount; i++) {
        for (let j = 0; j < tileCount; j++) {
            c.fillStyle = tileColor;
            c.fillRect(i * tileSize + 1, j * tileSize + 1, tileSize - 2, tileSize - 2);
        }
    }
}

function drawSymbol(x, y, symbol) {
    if (lastMove !== null) {
        c.fillStyle = tileColor;
        c.fillRect(lastMove.x * tileSize + 1, lastMove.y * tileSize + 1, tileSize - 2, tileSize - 2);
        c.fillStyle = lastMove.symbol === 'X' ? 'red' : 'blue';
        c.font = `${fontSize}px Arial`;
        c.textAlign = 'center';
        c.textBaseline = 'middle';
        c.fillText(lastMove.symbol, lastMove.x * tileSize + tileSize / 2, lastMove.y * tileSize + tileSize / 2);
    }

    c.fillStyle = tileColorHighlighted;
    c.fillRect(x * tileSize + 1, y * tileSize + 1, tileSize - 2, tileSize - 2);
    c.fillStyle = symbol === 'X' ? 'red' : 'blue';
    c.font = `${fontSize}px Arial`;
    c.textAlign = 'center';
    c.textBaseline = 'middle';
    c.fillText(symbol, x * tileSize + tileSize / 2, y * tileSize + tileSize / 2);

    lastMove = {x: x, y: y, symbol: symbol};
}

socket.on('initialData', (data) => {
    tileCount = data.tileCount;
    tileSize = data.tileSize;
    fontSize = Math.ceil(tileSize * .75);
    lastMove = null;

    canvas.width = tileCount * tileSize;
    canvas.height = tileCount * tileSize;
    drawBackground();

    for (let i = 0; i < tileCount; i++) {
        for (let j = 0; j < tileCount; j++) {
            if (data.board[i][j] !== ' ') {
                drawSymbol(i, j, data.board[i][j]);
            }
        }
    }
});

socket.on('player', (player) => {
    thisPlayer = player;
});

socket.on('gameFull', () => {
    modalGameFull.show();
});

socket.on('drawSymbol', (data) => {
    drawSymbol(data.x, data.y, data.symbol);
});

socket.on('info', (msg) => {
    if (msg.player === thisPlayer) {
        let replace = new RegExp(`player '${msg.player}'`, 'gi');
        msg.msg = msg.msg.replace(replace, msg.replace);
        msg.msg = msg.msg.replace('wins', 'win');
    }

    info.innerHTML = msg.msg;
});

socket.on('win', (data) => {
    for (let i = 0; i < 5; i++) {
        const x = data.x + i * data.directionX;
        const y = data.y + i * data.directionY;

        c.fillStyle = tileColorHighlighted;
        c.fillRect(x * tileSize + 1, y * tileSize + 1, tileSize - 2, tileSize - 2);
        c.fillStyle = data.symbol === 'X' ? 'red' : 'blue';
        c.font = `${fontSize}px Arial`;
        c.textAlign = 'center';
        c.textBaseline = 'middle';
        c.fillText(data.symbol, x * tileSize + tileSize / 2, y * tileSize + tileSize / 2);
    }
});

canvas.addEventListener('click', (e) => {
    socket.emit('click', {
        x: Math.floor(e.offsetX / tileSize),
        y: Math.floor(e.offsetY / tileSize)
    });
});
