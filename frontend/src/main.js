import checkboxService from './services/checkbox.js';

const grid = document.getElementById('grid');
const content = document.getElementById('content');

const TOTAL_CHECKBOXES = 1_000_000;
const CHECKBOX_SIZE = 20;
const GAP = 2; 
const CHECKBOX_SPACE = CHECKBOX_SIZE + GAP;
const BUFFER_ROWS = 10; 

let boxesPerRow = 0;
let renderedCheckboxes = {};

const getBoxesPerRow = () => {
    return Math.floor(grid.clientWidth / CHECKBOX_SPACE);
};

const renderCheckboxes = (state) => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const windowHeight = window.innerHeight;
    const contentTop = grid.offsetTop;

    boxesPerRow = getBoxesPerRow();

    const totalRows = Math.ceil(TOTAL_CHECKBOXES / boxesPerRow);
    const contentHeight = totalRows * CHECKBOX_SPACE;
    content.style.height = `${contentHeight}px`;

    const startRow = Math.max(0, Math.floor((scrollTop - contentTop) / CHECKBOX_SPACE) - BUFFER_ROWS);
    const endRow = Math.min(totalRows, Math.ceil((scrollTop - contentTop + windowHeight) / CHECKBOX_SPACE) + BUFFER_ROWS);

    const startIndex = startRow * boxesPerRow;
    const endIndex = Math.min(TOTAL_CHECKBOXES, endRow * boxesPerRow);

    const indicesToRender = new Set();
    for (let i = startIndex; i < endIndex; i++) {
        indicesToRender.add(i);
    }

    Object.keys(renderedCheckboxes).forEach((key) => {
        const index = parseInt(key, 10);
        if (!indicesToRender.has(index)) {
            content.removeChild(renderedCheckboxes[index]);
            delete renderedCheckboxes[index];
        }
    });

    const handleCheck = async (event) => {
        const index = event.target.getAttribute('data-index')
        event.target.checked = event.target.checked
        const result = await checkboxService.check(index)
        state[result.index] = result.value
    }

    for (let i = startIndex; i < endIndex; i++) {
        const col = i % boxesPerRow;
        const row = Math.floor(i / boxesPerRow);
        const left = `${col * CHECKBOX_SPACE}px`;
        const top = `${row * CHECKBOX_SPACE}px`;

        if (renderedCheckboxes[i]) {
            const checkbox = renderedCheckboxes[i];
            checkbox.style.left = left;
            checkbox.style.top = top;
        } else {
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'checkbox';
            checkbox.dataset.index = i;
            checkbox.onclick = handleCheck
            
            checkbox.checked = Boolean(state[i])

            checkbox.style.left = left;
            checkbox.style.top = top;

            content.appendChild(checkbox);
            renderedCheckboxes[i] = checkbox;
        }
    }
};

let scrollTimeout;
let state = (await checkboxService.state()).state.split('')
state = state.map((char) => parseInt(char))
const handleScroll = () => {
    if (scrollTimeout) {
        cancelAnimationFrame(scrollTimeout);
    }
    scrollTimeout = requestAnimationFrame(() => {
        renderCheckboxes(state);
    });
};

const handleResize = () => {
    renderCheckboxes(state);
};

window.addEventListener('scroll', handleScroll);
window.addEventListener('resize', handleResize);
renderCheckboxes(state);
