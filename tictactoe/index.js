const express = require('express');
const bodyParser = require('body-parser');
const { createServer } = require('node:http');
const { Server } = require('socket.io');

const PORT = 3000;
const app = express();
const server = createServer(app);
const io = new Server(server);

const winningCount = 5;
const tileCount = 15;
const tileSize = 40;
let board = [];
for (let i = 0; i < tileCount; i++) {
    board[i] = [];
    for (let j = 0; j < tileCount; j++) {
        board[i][j] = ' ';
    }
}

let userIDX = null;
let userIDO = null;
let currentPlayer = 'X';
let playing = false;
let ended = false;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

function checkWin(data) {
    const symbol = data.symbol;
    const x = data.x;
    const y = data.y;

    let out = {symbol: symbol};

    // Horizontal
    let count = 0;
    out.directionX = -1;
    out.directionY = 0;
    for (let i = 0; i < tileCount; i++) {
        if (board[i][y] === symbol) {
            count++;
            if (count >= winningCount) {
                out.x = i;
                out.y = y;
                io.emit('win', out);
                return true;
            };
        } else {
            count = 0;
        }
    }

    // Vertical
    count = 0;
    out.directionX = 0;
    out.directionY = -1;
    for (let i = 0; i < tileCount; i++) {
        if (board[x][i] === symbol) {
            count++;
            if (count >= winningCount) {
                out.x = x;
                out.y = i;
                io.emit('win', out);
                return true;
            };
        } else {
            count = 0;
        }
    }

    // Diagonal \
    count = 0;
    out.directionX = -1;
    out.directionY = -1;
    for (let i = -tileCount; i <= tileCount; i++) {
        const xi = x + i;
        const yi = y + i;
        if (xi >= 0 && xi < tileCount && yi >= 0 && yi < tileCount && board[xi][yi] === symbol) {
            count++;
            if (count >= winningCount) {
                out.x = xi;
                out.y = yi;
                io.emit('win', out);
                return true;
            };
        } else {
            count = 0;
        }
    }

    // Diagonal /
    count = 0;
    out.directionX = -1;
    out.directionY = 1;
    for (let i = -tileCount; i <= tileCount; i++) {
        const xi = x + i;
        const yi = y - i;
        if (xi >= 0 && xi < tileCount && yi >= 0 && yi < tileCount && board[xi][yi] === symbol) {
            count++;
            if (count >= winningCount) {
                out.x = xi;
                out.y = yi;
                io.emit('win', out);
                return true;
            };
        } else {
            count = 0;
        }
    }

    return false;
}

let currentInfo;

function infoTurn(player) {
    currentInfo = {msg: `Player '${player}' turn:`, replace: 'Your', player: player};
    io.emit('info', currentInfo);
}

function infoWaiting(player) {
    currentInfo = {msg: `Waiting for player '${player}' to connect...`, replace: 'you', player: player};
    io.emit('info', currentInfo);
}

function infoSurrender(player) {
    currentInfo = {msg: `Player '${player}' surrendered, player '${player === 'X' ? 'O' : 'X'}' wins the game.`, replace: 'you', player: player === 'X' ? 'O' : 'X'};
    io.emit('info', currentInfo);
}

function infoWin(player) {
    currentInfo = {msg: `Player '${player}' wins the game!`, replace: 'You', player: player};
    io.emit('info', currentInfo);
}

io.on('connection', (socket) => {
    if (userIDX === null && !playing) {
        userIDX = socket.id;
        socket.emit('player', 'X');
        console.log(`Player 'X' connected '${userIDX}'`);
        if (userIDO === null) {
            infoWaiting('O');
        } else {
            playing = true;
            infoTurn(currentPlayer);
        }
    } else if (userIDO === null && !playing) {
        userIDO = socket.id;
        socket.emit('player', 'O');
        console.log(`Player 'O' connected '${userIDO}'`);
        if (userIDX === null) {
            infoWaiting('X');
        } else {
            playing = true;
            infoTurn(currentPlayer);
        }
    } else {
        socket.emit('gameFull');
        socket.emit('info', currentInfo);
        console.log(`Spectator connected '${socket.id}'`);
    }

    socket.on('disconnect', () => {
        if (socket.id === userIDX) {
            console.log(`Player 'X' disconnected '${userIDX}'`);
            userIDX = null;
            if (playing && !ended) {
                ended = true;
                console.log(`Player 'X' surrendered`);
                infoSurrender('X');
            }
        } else if (socket.id === userIDO) {
            console.log(`Player 'O' disconnected '${userIDO}'`);
            userIDO = null;
            if (playing && !ended) {
                ended = true;
                console.log(`Player 'O' surrendered`);
                infoSurrender('O');
            }
        } else {
            console.log(`Spectator disconnected '${socket.id}'`);
        }
    });

    socket.on('click', (data) => {
        if (playing && !ended && data.x >= 0 && data.x < tileCount && data.y >= 0 && data.y < tileCount && board[data.x][data.y] === ' ') {
            if (socket.id === userIDX) {
                data.symbol = 'X';
                if (data.symbol === currentPlayer) {
                    board[data.x][data.y] = data.symbol;
                    console.log(`Player 'X' drew at [${data.x}; ${data.y}]`);
                    io.emit('drawSymbol', data);
                    if (checkWin(data)) {
                        ended = true;
                        console.log(`Player '${data.symbol}' wins the game!`);
                        infoWin(data.symbol);
                        return;
                    } else {
                        currentPlayer = 'O';
                        infoTurn(currentPlayer);
                    }
                }
            } else if (socket.id === userIDO) {
                data.symbol = 'O';
                if (data.symbol === currentPlayer) {
                    board[data.x][data.y] = data.symbol;
                    console.log(`Player 'O' drew at [${data.x}; ${data.y}]`);
                    io.emit('drawSymbol', data);
                    if (checkWin(data)) {
                        ended = true;
                        console.log(`Player '${data.symbol}' wins the game!`);
                        infoWin(data.symbol);
                        return;
                    } else {
                        currentPlayer = 'X';
                        infoTurn(currentPlayer);
                    }
                }
            }   
        }
    });

    socket.emit('initialData', {
        tileCount: tileCount,
        tileSize: tileSize,
        board: board
    });
});

server.listen(PORT, () => {
        console.log(`Server running on port: ${PORT}`);
});
