const catchArena = document.querySelector("#catch-arena");
const catchStart = document.querySelector("#catch-start");
const starTarget = document.querySelector("#star-target");
const catchScore = document.querySelector("#catch-score");
const catchTime = document.querySelector("#catch-time");
const catchStatus = document.querySelector("#catch-status");
const catchHint = document.querySelector("#catch-hint");

let catchInterval;
let catchActive = false;
let score = 0;
let secondsRemaining = 20;

function moveStar() {
  const maxX = Math.max(0, catchArena.clientWidth - starTarget.offsetWidth);
  const maxY = Math.max(0, catchArena.clientHeight - starTarget.offsetHeight);
  starTarget.style.left = `${Math.random() * maxX}px`;
  starTarget.style.top = `${Math.random() * maxY}px`;
}

function finishCatchGame() {
  clearInterval(catchInterval);
  catchActive = false;
  starTarget.hidden = true;
  catchHint.hidden = false;
  catchHint.textContent = "Time's up!";
  catchStart.disabled = false;
  catchStart.textContent = "Play again";
  catchStatus.textContent = `Nice catch! You scored ${score} ${score === 1 ? "star" : "stars"}.`;
}

catchStart.addEventListener("click", () => {
  clearInterval(catchInterval);
  score = 0;
  secondsRemaining = 20;
  catchScore.textContent = score;
  catchTime.textContent = secondsRemaining;
  catchStatus.textContent = "Catch the star!";
  catchHint.hidden = true;
  starTarget.hidden = false;
  catchActive = true;
  catchStart.disabled = true;
  catchStart.textContent = "Game in progress";
  moveStar();

  catchInterval = setInterval(() => {
    secondsRemaining -= 1;
    catchTime.textContent = secondsRemaining;
    if (secondsRemaining === 0) finishCatchGame();
  }, 1000);
});

starTarget.addEventListener("click", () => {
  if (!catchActive) return;
  score += 1;
  catchScore.textContent = score;
  moveStar();
});

const memoryCells = [...document.querySelectorAll(".memory-cell")];
const memoryStart = document.querySelector("#memory-start");
const memoryStatus = document.querySelector("#memory-status");
const memoryRound = document.querySelector("#memory-round");
const memoryBest = document.querySelector("#memory-best");

let sequence = [];
let sequencePosition = 0;
let memoryActive = false;
let showingSequence = false;
let memoryRun = 0;
let bestRound = 0;

function pause(duration) {
  return new Promise((resolve) => setTimeout(resolve, duration));
}

async function playSequence(run) {
  sequence.push(Math.floor(Math.random() * memoryCells.length));
  sequencePosition = 0;
  showingSequence = true;
  memoryCells.forEach((cell) => {
    cell.disabled = true;
  });
  memoryRound.textContent = sequence.length;
  memoryStatus.textContent = "Watch the lights…";
  await pause(350);

  for (const cellIndex of sequence) {
    if (run !== memoryRun) return;
    memoryCells[cellIndex].classList.add("active");
    await pause(450);
    memoryCells[cellIndex].classList.remove("active");
    await pause(180);
  }

  if (run !== memoryRun) return;
  showingSequence = false;
  memoryCells.forEach((cell) => {
    cell.disabled = false;
  });
  memoryStatus.textContent = "Your turn — repeat the pattern.";
}

memoryStart.addEventListener("click", () => {
  memoryRun += 1;
  sequence = [];
  memoryActive = true;
  memoryStart.disabled = true;
  memoryStart.textContent = "Game in progress";
  playSequence(memoryRun);
});

memoryCells.forEach((cell, index) => {
  cell.addEventListener("click", () => {
    if (!memoryActive || showingSequence) return;
    cell.classList.add("active");
    setTimeout(() => cell.classList.remove("active"), 140);

    if (index !== sequence[sequencePosition]) {
      memoryActive = false;
      memoryRun += 1;
      memoryCells.forEach((button) => {
        button.disabled = true;
      });
      const completedRound = Math.max(0, sequence.length - 1);
      bestRound = Math.max(bestRound, completedRound);
      memoryBest.textContent = bestRound;
      memoryStatus.textContent = `Not quite — you reached round ${completedRound}.`;
      memoryStart.disabled = false;
      memoryStart.textContent = "Try again";
      return;
    }

    sequencePosition += 1;
    if (sequencePosition === sequence.length) {
      showingSequence = true;
      memoryCells.forEach((button) => {
        button.disabled = true;
      });
      memoryStatus.textContent = "Perfect! Get ready for the next round…";
      bestRound = Math.max(bestRound, sequence.length);
      memoryBest.textContent = bestRound;
      const run = memoryRun;
      setTimeout(() => {
        if (memoryActive && run === memoryRun) playSequence(run);
      }, 650);
    }
  });
});
