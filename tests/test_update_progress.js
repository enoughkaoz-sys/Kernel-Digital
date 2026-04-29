const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');

// Read the index.html file
const htmlPath = path.join(__dirname, '..', 'index.html');
const htmlContent = fs.readFileSync(htmlPath, 'utf-8');

// Extract the script content from index.html
const scriptMatch = htmlContent.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) {
    throw new Error('Could not find script block in index.html');
}
let scriptContent = scriptMatch[1];

// We need to modify the script content to expose the variables and functions to our test scope
// without relying on brittle string replacement, we'll wrap the whole thing in a function that returns the API.

test('updateProgress logic branches', async (t) => {
    // Setup global mocks
    global.window = {};

    // Mock the DOM
    const mockElements = {
        'progress-count': { textContent: '' },
        'progress-fill': { style: { width: '' } },
        'btn-unlock': {
            classes: new Set(),
            classList: {
                add(cls) { mockElements['btn-unlock'].classes.add(cls); }
            }
        },
        'modal-icon': { style: { cssText: '' } },
        'modal-title': { textContent: '' },
        'modal-desc': { textContent: '' },
        'modal-steps': { innerHTML: '' },
        'modal-btn-go': { onclick: null },
        'modal-overlay': { classList: { add() {}, remove() {} } },
        'preview-area': { querySelector: () => ({ style: {} }) },
        'unlocked-area': { classList: { add() {} }, scrollIntoView() {} },
        'lock-box': { style: { display: '' } }
    };

    global.document = {
        getElementById: (id) => {
            if (!mockElements[id]) {
                mockElements[id] = {
                    classList: { add() {}, remove() {} },
                    style: {}
                };
            }
            return mockElements[id];
        }
    };

    // To properly access let/const bindings from the top level,
    // we wrap the script in an IIFE that returns the variables and functions we need.
    const wrapper = new Function(`
        ${scriptContent.replace('window.open(', '// window.open(')}

        return {
            updateProgress: updateProgress,
            getCompletedTasks: () => completedTasks,
            getTotal: () => TOTAL,
        };
    `);

    const api = wrapper();

    await t.test('handles partial progress correctly', () => {
        // Reset state
        api.getCompletedTasks().clear();
        mockElements['btn-unlock'].classes.clear();

        // Add one task
        api.getCompletedTasks().add(1);
        api.updateProgress();

        // Verify state
        assert.strictEqual(mockElements['progress-count'].textContent, '1 / 3 tarefas');
        assert.ok(mockElements['progress-fill'].style.width.includes('33.333'));
        assert.strictEqual(mockElements['btn-unlock'].classes.has('active'), false);
    });

    await t.test('handles full progress correctly', () => {
        // Reset state
        api.getCompletedTasks().clear();
        mockElements['btn-unlock'].classes.clear();

        // Add all tasks
        api.getCompletedTasks().add(1);
        api.getCompletedTasks().add(2);
        api.getCompletedTasks().add(3);
        api.updateProgress();

        // Verify state
        assert.strictEqual(mockElements['progress-count'].textContent, '3 / 3 tarefas');
        assert.strictEqual(mockElements['progress-fill'].style.width, '100%');
        assert.strictEqual(mockElements['btn-unlock'].classes.has('active'), true);
    });
});
