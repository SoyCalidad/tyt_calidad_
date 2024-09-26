// Seleccionar el contenedor de la encuesta
const surveyForm = document.getElementById('satisfaction_survey_body');

// Verificar si estamos en la página correcta con el contenedor de la encuesta
if (surveyForm) {
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

    const categories = Object.keys(totalQuestions);

    // Función para actualizar la pregunta actual
    function updateQuestion() {
        const allQuestions = surveyForm.querySelectorAll('.question');
        allQuestions.forEach(question => question.style.display = 'none'); // Esconder todas las preguntas
        // Esconde todos los divs dentro de la pregunta
        allQuestions.forEach(question => {
            const childElements = question.querySelectorAll('*');
            childElements.forEach(child => child.style.display = 'none');
        })

        // Mostrar la pregunta actual
        const currentQuestionId = `${currentCategory}_${currentQuestionIndex}`;
        const currentQuestion = surveyForm.querySelector(`#${currentQuestionId}`);
        if (currentQuestion) {
            currentQuestion.style.display = 'block';
            const childElements = currentQuestion.querySelectorAll('*');
            childElements.forEach(child => child.style.display = 'block');
        }

        // Actualizar la barra de categorías
        const categoryItems = surveyForm.querySelectorAll('.category-item');
        categoryItems.forEach(item => {
            item.classList.remove('active');
            if (item.dataset.category === currentCategory) {
                item.classList.add('active');
            }
        });

        // Create Radio Buttons
        CreateRadioButtons();        

        // Deshabilitar el botón "Anterior" si estamos en la primera pregunta de la primera categoría
        surveyForm.querySelector('#previous').disabled = (currentCategory === 'cat_1' && currentQuestionIndex === 1);
    }

    // Evento para el botón "Siguiente"
    surveyForm.querySelector('#next').addEventListener('click', () => {
        currentQuestionIndex++;

        if (currentQuestionIndex > totalQuestions[currentCategory]) {
            const currentCategoryIndex = categories.indexOf(currentCategory);

            if (currentCategoryIndex < categories.length - 1) {
                currentCategory = categories[currentCategoryIndex + 1];
                currentQuestionIndex = 1;
            } else {
                alert('Encuesta completada');
                return;
            }
        }

        updateQuestion();
    });

    // Evento para el botón "Anterior"
    surveyForm.querySelector('#previous').addEventListener('click', () => {
        currentQuestionIndex--;

        if (currentQuestionIndex < 1) {
            const currentCategoryIndex = categories.indexOf(currentCategory);

            if (currentCategoryIndex > 0) {
                currentCategory = categories[currentCategoryIndex - 1];
                currentQuestionIndex = totalQuestions[currentCategory];
            }
        }

        updateQuestion();
    });

    // Inicializar con la primera pregunta
    updateQuestion();

    function CreateRadioButtons() {

        const currentQuestionId = `${currentCategory}_${currentQuestionIndex}`; // Asegúrate de que este ID coincida con el ID del elemento existente.
        const totalOptions = 10; // Por ejemplo, puedes tener 10 opciones.

        const divContainer = document.getElementById(currentQuestionId); // Selecciona el div existente.

        // Check if the div exists and the radioContainer exists in the div
        // If exists, does not create the radioContainer
        // If not exists, creates the radioContainer

        if (!divContainer) {
            const newDiv = document.createElement('div');
            newDiv.id = currentQuestionId;
            newDiv.className = 'TYTradioContainer';
            surveyForm.appendChild(newDiv);
        }
        

        if (divContainer) { // Verifica que el div existe antes de continuar.
            const radioContainer = divContainer.querySelector('#TYTradioContainer'); // Busca el contenedor de los radiobuttons

            if (radioContainer) { // Verifica que el contenedor también existe
                for (let i = 1; i <= totalOptions; i++) {
                    const label = document.createElement('label');
                    label.innerHTML = `${i}<br />`;

                    const input = document.createElement('input');
                    input.type = 'radio';
                    input.name = `myChoice_${currentQuestionId}`; // Agrupa por pregunta
                    input.value = i;
                    input.id = `${currentQuestionId}_choice${i}`; // Asignar id dinámicamente
                    input.className = `${currentQuestionId}_choice${i}`; // Asignar clase dinámicamente

                    label.setAttribute('for', input.id);
                    label.appendChild(input);

                    radioContainer.appendChild(label); // Añadir la etiqueta al contenedor de radiobuttons
                }
            } else {
                console.error(`No se encontró el contenedor TYTradioContainer dentro del div con ID ${currentQuestionId}`);
            }
        } else {
            console.error(`No se encontró el elemento con ID ${currentQuestionId}`);
        }
    }
}
