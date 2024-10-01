const surveyForm = document.getElementById('satisfaction_survey_body');

if (surveyForm) {
    let currentCategory = 'cat_0';
    let currentQuestionIndex = 1;
    const totalQuestions = {
        cat_0: 1,
        cat_1: 4,
        cat_2: 3,
        cat_3: 4,
        cat_4: 3,
        cat_5: 4,
        cat_6: 3,
        cat_7: 4,
    };

    const categories = Object.keys(totalQuestions);

    function updateQuestion() {
        const allQuestions = surveyForm.querySelectorAll('.question');
        allQuestions.forEach(question => question.style.display = 'none');
        allQuestions.forEach(question => {
            const childElements = question.querySelectorAll('*');
            childElements.forEach(child => child.style.display = 'none');
        })

        const currentQuestionId = `${currentCategory}_${currentQuestionIndex}`;
        const currentQuestion = surveyForm.querySelector(`#${currentQuestionId}`);
        if (currentQuestion) {
            currentQuestion.style.display = 'block';
            const childElements = currentQuestion.querySelectorAll('*');
            childElements.forEach(child => child.style.display = 'block');
        }

        const categoryItems = surveyForm.querySelectorAll('.category-item');
        categoryItems.forEach(item => {
            item.classList.remove('active');
            if (item.dataset.category === currentCategory) {
                item.classList.add('active');
            }
        });

        CreateRadioButtons();

        surveyForm.querySelector('#previous').disabled = (currentCategory === 'cat_0' && currentQuestionIndex === 1);
    }

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

    updateQuestion();

    function CreateRadioButtons() {

        const currentQuestionId = `${currentCategory}_${currentQuestionIndex}`;
        const totalOptions = 10;

        const divContainer = document.getElementById(currentQuestionId);

        const QuestionRadioContainer = document.getElementById(`${currentQuestionId}_radioContainer`);

        if (!QuestionRadioContainer) {

            if (divContainer) {
                const radioContainer = divContainer.querySelector('#TYTradioContainer');

                if (radioContainer) {

                    const QuestionRadioContainer = document.createElement('div');
                    QuestionRadioContainer.id = `${currentQuestionId}_radioContainer`;
                    radioContainer.appendChild(QuestionRadioContainer);

                    for (let i = 1; i <= totalOptions; i++) {
                        const label = document.createElement('label');
                        label.innerHTML = `${i}<br/>`;
                        label.className = 'radio-inline';

                        const input = document.createElement('input');
                        input.type = 'radio';
                        input.name = `${currentQuestionId}`;
                        input.value = i;
                        input.id = `${currentQuestionId}_choice${i}`;
                        input.className = `${currentQuestionId}`;

                        label.setAttribute('for', input.id);
                        label.appendChild(input);

                        QuestionRadioContainer.appendChild(label);
                    }
                } else {
                    console.error(`No se encontró el contenedor TYTradioContainer dentro del div con ID ${currentQuestionId}`);
                }
            } else {
                console.error(`No se encontró el elemento con ID ${currentQuestionId}`);
            }
        }
    }
}
