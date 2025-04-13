document.addEventListener('DOMContentLoaded', function() {
    // Remove the old key elements
    document.querySelectorAll('.key').forEach(key => key.remove());

    // Position black keys correctly
    const blackKeys = document.querySelectorAll('.black-key');
    const positions = [
        1, // After first white key
        2, // After second white key
        4, // After fourth white key
        5, // After fifth white key
        6,  // After sixth white key
        8,  // After eighth white key
        9,  // After ninth white key
    ];

    blackKeys.forEach((key, index) => {
        const position = positions[index % positions.length];
        const offset = position * 48; // 40px (white key width) + 4px (margins)
        key.style.left = `${offset}px`;
    });

    // Add hover effect for the entire piano
    const piano = document.querySelector('.piano');
    piano.addEventListener('mouseover', () => {
        document.querySelectorAll('.white-key::after, .black-key::after')
            .forEach(key => key.style.opacity = '1');
    });

    piano.addEventListener('mouseleave', () => {
        document.querySelectorAll('.white-key::after, .black-key::after')
            .forEach(key => key.style.opacity = '0');
    });

    //keydown event listener
    document.addEventListener('keydown', (event) => {
        const key = event.key.toUpperCase(); //gets the pressed key
        const pianoKey = document.querySelector(`[data-key="${key}"]`);

        if (pianoKey) {
            //Add a class to the piano key to indicate it is pressed
            pianoKey.classList.add('pressed');

            //Remove the class after a short delay to simulate key release
            setTimeout(() => {
                pianoKey.classList.remove('pressed');
            }, 100);
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const sound = {
        65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
        87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
        83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
        69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
        68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
        70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
        84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
        71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
        89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
        72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
        85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
        74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
        75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
        79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
        76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
        80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
        186: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
    };

    const sequence = "weseeyou";
    let input = "";
    const piano = document.querySelector('.piano');
    const pianoContainer = document.querySelector('.piano-container'); // Ensure this is selected
    const creepyAudio = new Audio("../static/piano/Creepy-piano-sound-effect.mp3");
    const greatOldOne = "../static/piano/images/texture.jpeg";

    document.addEventListener('keydown', function (event) {
        const keyCode = event.keyCode;
        const key = event.key.toLowerCase(); // Normalize input to lowercase

        input += key;

        if (input.includes(sequence)) {
            awakenGreatOldOne();
            return;
        }

        if (sound[keyCode]) {
            const audio = new Audio(sound[keyCode]);
            audio.play();
        }

        const pianoKey = document.querySelector(`[data-key="${event.key.toUpperCase()}"]`);
        if (pianoKey) {
            pianoKey.classList.add('pressed');
            setTimeout(() => pianoKey.classList.remove('pressed'), 100);
        }
    });

    function awakenGreatOldOne() {
        piano.style.transition = 'opacity 2s';
        piano.style.opacity = '0';

        setTimeout(() => {
            pianoContainer.innerHTML = `
                <div class="piano-image-container">
                    <div class="awoken-text">I HAVE AWOKEN</div>

                    <img src="${greatOldOne}" alt="The Great Old One" class="piano-image">
                    </div>
            `;
        }, 1000);

        creepyAudio.play().catch(error => console.log("Autoplay blocked:", error));

        document.removeEventListener('keydown', arguments.callee);
    }
});
