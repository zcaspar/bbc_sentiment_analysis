const levels = [
    [
        {
            question: 'What does \"generative\" in generative AI refer to?',
            options: [
                'The ability to generate new content',
                'The capacity to store large datasets',
                'Training models to run faster',
                'Using AI for database queries'
            ],
            answer: 0,
            explanation: 'Generative AI focuses on creating new content such as text, images, or audio.'
        },
        {
            question: 'Which model type is commonly used for text generation?',
            options: ['Convolutional Neural Network', 'Generative Adversarial Network', 'Recurrent or Transformer-based model', 'Support Vector Machine'],
            answer: 2,
            explanation: 'Transformer-based models like GPT are widely used for text generation.'
        }
    ],
    [
        {
            question: 'What is a key challenge with generative models?',
            options: [
                'They always require labeled data',
                'Ensuring generated content is high quality and not biased',
                'They cannot be trained on GPUs',
                'They do not need any data to train'
            ],
            answer: 1,
            explanation: 'Managing quality and bias is a central challenge in generative AI.'
        },
        {
            question: 'What does \"prompt engineering\" refer to?',
            options: [
                'Designing electrical circuits',
                'Crafting inputs that guide a generative model',
                'Training a model from scratch',
                'Measuring hardware speed'
            ],
            answer: 1,
            explanation: 'Prompt engineering is creating effective prompts to elicit desired responses from a model.'
        }
    ],
    [
        {
            question: 'Which approach helps a generative model improve using human feedback?',
            options: [
                'Reinforcement Learning from Human Feedback (RLHF)',
                'Unsupervised Pre-training',
                'Data Augmentation',
                'Dropout Regularization'
            ],
            answer: 0,
            explanation: 'RLHF fine-tunes models based on preferences indicated by humans.'
        },
        {
            question: 'Why is data diversity important for generative models?',
            options: [
                'It reduces the need for GPUs',
                'It ensures the model can create varied and unbiased content',
                'It simplifies the network architecture',
                'It eliminates the need for training'
            ],
            answer: 1,
            explanation: 'A diverse dataset helps the model generalize and produce balanced outputs.'
        }
    ]
];

let currentLevel = 0;
let currentQuestion = 0;
let selectedOption = null;

const levelDisplay = document.getElementById('level-display');
const questionEl = document.getElementById('question');
const optionsEl = document.getElementById('options');
const nextBtn = document.getElementById('next-btn');

function loadQuestion() {
    const q = levels[currentLevel][currentQuestion];
    levelDisplay.textContent = `Level ${currentLevel + 1}`;
    questionEl.textContent = q.question;
    optionsEl.innerHTML = '';
    q.options.forEach((opt, index) => {
        const div = document.createElement('div');
        div.textContent = opt;
        div.className = 'option';
        div.addEventListener('click', () => selectOption(div, index));
        optionsEl.appendChild(div);
    });
    nextBtn.disabled = true;
}

function selectOption(element, index) {
    const optionDivs = document.querySelectorAll('.option');
    optionDivs.forEach(div => div.classList.remove('selected'));
    element.classList.add('selected');
    selectedOption = index;
    nextBtn.disabled = false;
}

nextBtn.addEventListener('click', () => {
    const q = levels[currentLevel][currentQuestion];
    const correct = selectedOption === q.answer;
    alert((correct ? 'Correct! ' : 'Incorrect. ') + q.explanation);
    selectedOption = null;
    currentQuestion++;
    if (currentQuestion >= levels[currentLevel].length) {
        currentLevel++;
        currentQuestion = 0;
        if (currentLevel >= levels.length) {
            questionEl.textContent = 'Congratulations! You completed all levels.';
            optionsEl.innerHTML = '';
            levelDisplay.textContent = 'All levels complete';
            nextBtn.style.display = 'none';
            return;
        }
    }
    loadQuestion();
});

loadQuestion();
