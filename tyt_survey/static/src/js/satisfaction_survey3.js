// script.js

let currentCategory = 'cat_1';
let currentQuestionIndex = 1;
const totalQuestions = {
    cat_1: 4,
    cat_2: 3,
    cat_3: 4,
    cat_4: 3,
    cat_5: 4,
    cat_6: 3,
    cat_7: 4,
};

// Obtener lista de todas las categorías
const categories = Object.keys(totalQuestions);

// Función para actualizar la pregunta actual
function updateQuestion() {
    const allQuestions = document.querySelectorAll('.question');
    allQuestions.forEach(question => question.style.display = 'none'); // Esconder todas las preguntas

    // Mostrar la pregunta actual
    const currentQuestionId = `${currentCategory}_${currentQuestionIndex}`;
    console.log(currentQuestionId);
    const currentQuestion = document.getElementById(currentQuestionId);
    if (currentQuestion) {
        currentQuestion.style.display = 'block';
        const childElements = currentQuestion.querySelectorAll('*');
        console.log(childElements);
        childElements.forEach(child => child.style.display = 'block');
    }

    // Actualizar la barra de categorías
    document.querySelectorAll('.category-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.category === currentCategory) {
            item.classList.add('active');
        }
    });

    // Deshabilitar el botón "Anterior" si estamos en la primera pregunta de la primera categoría
    document.getElementById('previous').disabled = (currentCategory === 'cat_1' && currentQuestionIndex === 1);
}

// Evento para el botón "Siguiente"
$('next').click(function () {
    // Pasar a la siguiente pregunta en la categoría actual
    currentQuestionIndex++;

    // Si llegamos al final de una categoría
    if (currentQuestionIndex > totalQuestions[currentCategory]) {
        const currentCategoryIndex = categories.indexOf(currentCategory);

        // Si no estamos en la última categoría, avanzar a la siguiente categoría
        if (currentCategoryIndex < categories.length - 1) {
            currentCategory = categories[currentCategoryIndex + 1];  // Avanzar a la siguiente categoría
            currentQuestionIndex = 1;  // Reiniciar al comienzo de la nueva categoría
        } else {
            // Si no hay más categorías, finaliza el formulario o muestra un mensaje
            alert('Encuesta completada');
            return;
        }
    }

    updateQuestion();
});

// Evento para el botón "Anterior"
$('previous').click(function () {
    // Volver a la pregunta anterior en la categoría actual
    currentQuestionIndex--;

    // Si estamos al comienzo de una categoría y queremos ir hacia atrás
    if (currentQuestionIndex < 1) {
        const currentCategoryIndex = categories.indexOf(currentCategory);

        // Si no estamos en la primera categoría, retroceder a la categoría anterior
        if (currentCategoryIndex > 0) {
            currentCategory = categories[currentCategoryIndex - 1];  // Retroceder a la categoría anterior
            currentQuestionIndex = totalQuestions[currentCategory];  // Ir a la última pregunta de esa categoría
        }
    }

    updateQuestion();
});

updateQuestion();